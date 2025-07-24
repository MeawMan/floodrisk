"""
FloodRisk Package
==================
Provides tools for:
- Flood detection using Sentinel-1 SAR & Google Earth Engine
- Flood damage assessment for roads and buildings
- Data export and visualization

Main Functions:
    initialize()            - Authenticate and initialize GEE
    detect_flood()          - Detect flood inundation
    export_map()            - Export flood maps to Google Drive
    download_osm_data()     - Download OSM data (roads & buildings)
    compute_flood_damage()  - Calculate flood damage statistics
    export_csv()            - Save reports as CSV
    visualize_map()         - Visualize flood inundation map
"""

from .gee_auth import initialize
from .flood_detect import detect_flood, export_map
from .damage_assess import download_osm_data, compute_flood_damage
from .export_utils import export_csv
from .visualization import visualize_map

__all__ = [
    "initialize",
    "detect_flood",
    "export_map",
    "download_osm_data",
    "compute_flood_damage",
    "export_csv",
    "visualize_map"
]
