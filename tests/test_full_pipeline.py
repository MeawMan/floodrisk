import os
from shapely.geometry import Polygon
from floodrisk import osmdata, damage, exportcsv

def test_full_pipeline(tmp_path):
    """End-to-end test: OSM → Damage → Export."""
    aoi_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])
    roads, buildings = osmdata(aoi_polygon)
    result = damage(roads, buildings, "tests/Flood_Extent.tif")
    
    output_dir = tmp_path / "results"
    exportcsv(result['road_stats'], result['building_stats'], output_dir)
    
    # Check if files exist
    road_file = output_dir / "flood_damage_road_stats.csv"
    building_file = output_dir / "flood_damage_building_stats.csv"
    
    assert road_file.exists()
    assert building_file.exists()
