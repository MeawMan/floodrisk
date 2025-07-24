import ee
import time

def inundation(aoi_name, before_start, before_end, after_start, after_end, polarization="VV", pass_direction="ASCENDING"):
    """
    Calculate flood inundation using Sentinel-1 SAR and Otsu threshold.
    Returns dict: Flood stats and GEE image objects.
    """
    adm2 = ee.FeatureCollection("FAO/GAUL/2015/level2")
    aoi = adm2.filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh')).filter(ee.Filter.eq('ADM2_NAME', aoi_name))

    collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', polarization)) \
        .filter(ee.Filter.eq('orbitProperties_pass', pass_direction)) \
        .filterBounds(aoi) \
        .select(polarization)

    before = collection.filterDate(before_start, before_end).mosaic().clip(aoi)
    after = collection.filterDate(after_start, after_end).mosaic().clip(aoi)

    before_filtered = before.focal_mean(50, 'circle', 'meters')
    after_filtered = after.focal_mean(50, 'circle', 'meters')
    difference = after_filtered.divide(before_filtered).clamp(0.5, 2.0)

    # Otsu threshold
    hist = difference.reduceRegion(ee.Reducer.histogram(), aoi.geometry(), scale=10, bestEffort=True).get(polarization)

    def otsu(hist_dict):
        hist_dict = ee.Dictionary(hist_dict)
        counts = ee.Array(hist_dict.get('histogram'))
        means = ee.Array(hist_dict.get('bucketMeans'))
        total = counts.reduce('sum', [0]).get([0])
        seq = ee.List.sequence(1, counts.length().get([0]))
        def compute(i):
            i = ee.Number(i)
            bgCounts = counts.slice(0, 0, i)
            bgMeans = means.slice(0, 0, i)
            fgCounts = counts.slice(0, i)
            fgMeans = means.slice(0, i)
            wBg = bgCounts.reduce('sum', [0]).get([0]).divide(total)
            wFg = fgCounts.reduce('sum', [0]).get([0]).divide(total)
            mBg = bgMeans.multiply(bgCounts).reduce('sum', [0]).get([0]).divide(bgCounts.reduce('sum', [0]).get([0]))
            mFg = fgMeans.multiply(fgCounts).reduce('sum', [0]).get([0]).divide(fgCounts.reduce('sum', [0]).get([0]))
            return wBg.multiply(wFg).multiply(mBg.subtract(mFg).pow(2))
        between = seq.map(compute)
        maxVar = ee.Number(ee.Array(between).reduce('max', [0]).get([0]))
        thresholdIndex = ee.Number(ee.List(between).indexOf(maxVar))
        return means.get([thresholdIndex])

    otsu_threshold = ee.Algorithms.If(hist, otsu(hist), 1.15)

    flooded = difference.gt(ee.Number(otsu_threshold))
    swater = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality')
    flooded = flooded.where(swater.gte(10), 0).updateMask(flooded).updateMask(flooded.connectedPixelCount().gte(8))
    slope = ee.Algorithms.Terrain(ee.Image('WWF/HydroSHEDS/03VFDEM')).select('slope')
    flooded = flooded.updateMask(slope.lt(5))

    flood_pixelarea = flooded.select(polarization).multiply(ee.Image.pixelArea())
    flood_stats = flood_pixelarea.reduceRegion(ee.Reducer.sum(), aoi.geometry(), scale=10, bestEffort=True)
    flood_area_ha = ee.Number(flood_stats.get(polarization)).divide(10000)
    total_area_ha = ee.Number(ee.Image.pixelArea().clip(aoi).reduceRegion(ee.Reducer.sum(), aoi.geometry(), scale=10, bestEffort=True).get('area')).divide(10000)
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

def exportmap(image, description, output_folder, aoi, scale=10):
    """Export flood map to Google Drive and monitor status."""
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
