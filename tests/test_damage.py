import pytest
from shapely.geometry import Polygon
from floodrisk import osmdata, damage

@pytest.fixture
def sample_polygon():
    return Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

def test_osmdata_download(sample_polygon):
    """Check OSM data download."""
    roads, buildings = osmdata(sample_polygon)
    assert not roads.empty
    assert not buildings.empty

def test_damage_calculation(sample_polygon):
    """Check damage calculation on sample raster."""
    roads, buildings = osmdata(sample_polygon)
    result = damage(roads, buildings, "tests/Flood_Extent.tif")
    assert "road_stats" in result
    assert "building_stats" in result
