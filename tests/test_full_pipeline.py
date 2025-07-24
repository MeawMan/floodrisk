import os
from shapely.geometry import Polygon
from floodrisk import download_osm_data, compute_flood_damage, export_csv

def test_full_pipeline(tmp_path):
    """
    End-to-end test:
    1. Download OSM data
    2. Compute flood damage
    3. Export results as CSV
    """
    # Step 1: Define sample AOI polygon
    aoi_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

    # Step 2: Download OSM roads and buildings
    roads, buildings = download_osm_data(aoi_polygon)

    # Step 3: Compute damage using sample raster
    result = compute_flood_damage(roads, buildings, "tests/Flood_Extent.tif")

    # Step 4: Export results to CSV
    output_dir = tmp_path / "results"
    road_file, building_file = export_csv(result['road_stats'], result['building_stats'], str(output_dir))

    # Step 5: Verify files exist
    assert os.path.exists(road_file), f"Road stats file not found at {road_file}"
    assert os.path.exists(building_file), f"Building stats file not found at {building_file}"
