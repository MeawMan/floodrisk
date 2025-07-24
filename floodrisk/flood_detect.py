import ee
import time

def detect_flood(aoi_name: str, before_start: str, before_end: str,
                 after_start: str, after_end: str,
                 polarization: str = "VV", pass_direction: str = "ASCENDING") -> dict:
    """
    Detect flood inundation using Sentinel-1 SAR and Otsu thresholding.

    Parameters
    ----------
    aoi_name : str
        Name of the district (ADM2) in Bangladesh (e.g., 'Feni').
    before_start : str
        Start date for pre-flood period (e.g., '2022-05-01').
    before_end : str
        End date for pre-flood period (e.g., '2022-05-15').
    after_start : str
        Start date for post-flood period (e.g., '2022-06-01').
    after_end : str
        End date for post-flood period (e.g., '2022-06-15').
    polarization : str, optional
        Sentinel-1 polarization band ('VV' or 'VH'). Default is 'VV'.
    pass_direction : str, optional
        Orbit pass direction ('ASCENDING' or 'DESCENDING'). Default is 'ASCENDING'.

    Returns
    -------
    dict
        A dictionary with:
        - AOI name
        - Otsu Threshold
        - Total Area (ha)
        - Flooded Area (ha)
        - Inundation %
        - GEE Image objects: before_image, after_image, flooded_image, aoi
    """

    # Load AOI (Bangladesh ADM2 level)
    adm2 = ee.FeatureCollection("FAO/GAUL/2015/level2")
    aoi = adm2.filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh')) \
              .filter(ee.Filter.eq('ADM2_NAME', aoi_name))

    # Sentinel-1 ImageCollection filtering
    collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
                  .filter(ee.Filter.eq('instrumentMode', 'IW'))
                  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', polarization))
                  .filter(ee.Filter.eq('orbitProperties_pass', pass_direction))
                  .filterBounds(aoi)
                  .select(polarization))

    # Before and after mosaics
    before = collection.filterDate(before_start, before_end).mosaic().clip(aoi)
    after = collection.filterDate(after_start, after_end).mosaic().clip(aoi)

    # Apply smoothing
    before_filtered = before.focal_mean(50, 'circle', 'meters')
    after_filtered = after.focal_mean(50, 'circle', 'meters')

    # Compute ratio difference
    difference = after_filtered.divide(before_filtered).clamp(0.5, 2.0)

    # Compute histogram for Otsu
    hist = difference.reduceRegion(ee.Reducer.histogram(), aoi.geometry(), scale=10, bestEffort=True).get(polarization)

    def otsu(hist_dict):
        hist_dict = ee.Dictionary(hist_dict)
        counts = ee.Array(hist_dict.get('histogram'))
        means = ee.Array(hist_dict.get('bucketMeans'))
        total = counts.reduce('sum', [0]).get([0])
        seq = ee.List.sequence(1, counts.length().get([0]))

        def compute(i):
            i = ee.Number(i)
            bg_counts = counts.slice(0, 0, i)
            bg_means = means.slice(0, 0, i)
            fg_counts = counts.slice(0, i)
            fg_means = means.slice(0, i)
            w_bg = bg_counts.reduce('sum', [0]).get([0]).divide(total)
            w_fg = fg_counts.reduce('sum', [0]).get([0]).divide(total)
            m_bg = bg_means.multiply(bg_counts).reduce('sum', [0]).get([0]).divide(bg_counts.reduce('sum', [0]).get([0]))
            m_fg = fg_means.multiply(fg_counts).reduce('sum', [0]).get([0]).divide(fg_counts.reduce('sum', [0]).get([0]))
            return w_bg.multiply(w_fg).multiply(m_bg.subtract(m_fg).pow(2))

        between = seq.map(compute)
        max_var = ee.Number(ee.Array(between).reduce('max', [0]).get([0]))
        threshold_index = ee.Number(ee.List(between).indexOf(max_var))
        return means.get([threshold_index])

    otsu_threshold = ee.Algorithms.If(hist, otsu(hist), 1.15)

    # Flood mask
    flooded = difference.gt(ee.Number(otsu_threshold))

    # Remove permanent water and steep slopes
    swater = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality')
    flooded = flooded.where(swater.gte(10), 0) \
                     .updateMask(flooded) \
                     .updateMask(flooded.connectedPixelCount().gte(8))
    slope = ee.Algorithms.Terrain(ee.Image('WWF/HydroSHEDS/03VFDEM')).select('slope')
    flooded = flooded.updateMask(slope.lt(5))

    # Calculate flooded area (ha)
    flood_pixel_area = flooded.multiply(ee.Image.pixelArea())
    flood_stats = flood_pixel_area.reduceRegion(ee.Reducer.sum(), aoi.geometry(), scale=10, bestEffort=True)
    flood_area_ha = ee.Number(flood_stats.values().get(0)).divide(10000)

    total_area_ha = ee.Number(ee.Image.pixelArea()
                               .clip(aoi)
                               .reduceRegion(ee.Reducer.sum(), aoi.geometry(), scale=10, bestEffort=True)
                               .get('area')).divide(10000)

    inundation_percent = flood_area_ha.divide(total_area_ha).multiply(100)

    return {
        'AOI': aoi_name,
        'Otsu Threshold': otsu_threshold,
        'Total Area (ha)': total_area_ha,
        'Flooded Area (ha)': flood_area_ha,
        'Inundation %': inundation_percent,
        'before_image': before_filtered,
        'after_image': after_filtered,
        'flooded_image': flooded,
        'aoi': aoi
    }


def export_map(image, description: str, output_folder: str, aoi, scale: int = 10):
    """
    Export a flood map to Google Drive and monitor task progress.

    Parameters
    ----------
    image : ee.Image
        Image to export.
    description : str
        Name for the export task.
    output_folder : str
        Google Drive folder name.
    aoi : ee.FeatureCollection
        Area of interest.
    scale : int, optional
        Export scale in meters (default is 10).
    """
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=description,
        folder=output_folder,
        fileNamePrefix=description,
        region=aoi.geometry(),
        scale=scale,
        maxPixels=1e10
    )
    task.start()
    print(f"Export started: {description}. Tracking progress...")

    while True:
        status = task.status()
        state = status.get('state')
        print(f"Current status: {state}")
        if state in ['COMPLETED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(10)

    print(f"Final status: {state}")
