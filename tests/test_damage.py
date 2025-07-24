import pytest
from shapely.geometry import Polygon
from floodrisk import download_osm_data, compute_flood_damage

@pytest.fixture
def sample_polygon():
    """Sample AOI polygon for OSM data tests."""
    return Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

def test_osm_data_download(sample_polygon):
    """Check if OSM roads and buildings are downloaded successfully."""
    roads, buildings = download_osm_data(sample_polygon)
    assert not roads.empty, "Roads data should not be empty."
    assert not buildings.empty, "Buildings data should not be empty."

def test_flood_damage_calculation(sample_polygon):
    """Check flood damage calculation using sample flood raster."""
    roads, buildings = download_osm_data(sample_polygon)
    result = compute_flood_damage(roads, buildings, "tests/Flood_Extent.tif")
    
    assert "road_stats" in result, "Result should contain 'road_stats'."
    assert "building_stats" in result, "Result should contain 'building_stats'."
    assert isinstance(result["road_stats"].shape[0], int), "Road stats should be a DataFrame."
    assert isinstance(result["building_stats"], dict), "Building stats should be a dictionary."
