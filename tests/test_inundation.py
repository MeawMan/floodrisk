import pytest
from floodrisk import inundation

def test_inundation_function_exists():
    """Check if inundation function is callable."""
    assert callable(inundation)

@pytest.mark.skip(reason="Requires GEE authentication and internet")
def test_inundation_execution():
    """Integration test with GEE (run manually)."""
    result = inundation(
        aoi_name="Feni",
        before_start="2025-01-01", before_end="2025-01-31",
        after_start="2025-07-01", after_end="2025-07-12"
    )
    assert "Flooded Area (ha)" in result
    assert "Inundation %" in result
