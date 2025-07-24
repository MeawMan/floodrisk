import pytest
from floodrisk import detect_flood

def test_detect_flood_function_exists():
    """Check if detect_flood function is callable."""
    assert callable(detect_flood), "detect_flood should be callable."

@pytest.mark.skip(reason="Requires GEE authentication and internet")
def test_detect_flood_execution():
    """
    Integration test with Google Earth Engine.
    This test is skipped by default because it needs:
    - GEE authentication
    - Internet connectivity
    Run manually if needed.
    """
    result = detect_flood(
        aoi_name="Feni",
        before_start="2025-01-01", before_end="2025-01-31",
        after_start="2025-07-01", after_end="2025-07-12"
    )
    
    assert "Flooded Area (ha)" in result, "Result should contain flooded area."
    assert "Inundation %" in result, "Result should contain inundation percentage."
