# **FloodRisk**

*Flood detection and damage assessment using Sentinel-1 SAR and OpenStreetMap (OSM) data.*

[![PyPI version](https://img.shields.io/pypi/v/floodrisk.svg)](https://pypi.org/project/floodrisk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.xxxx/zenodo.xxxxx.svg)](https://doi.org/10.xxxx/zenodo.xxxxx)

---

## **Overview**

`floodrisk` is a Python package designed for:

* **Flood inundation mapping** using Sentinel-1 SAR imagery
* **Otsu threshold-based detection**
* **Damage assessment** for roads and buildings using OSM data
* **Export of results** (CSV, GeoTIFF)
* **Supports GEE integration for large-scale flood detection**

---

## **Key Features**

✔ Detect flood extent using **Sentinel-1 SAR**
✔ Automatic thresholding using **Otsu method**
✔ Compute inundation percentage and area statistics
✔ Assess damage to **roads (by category)** and **buildings** using OSM data
✔ Export results in CSV and raster format
✔ Works with **Google Earth Engine** for large-scale AOIs

---

## **Installation**

```bash
pip install floodrisk
```

### **From source**

```bash
git clone https://github.com/your-username/floodrisk.git
cd floodrisk
pip install -e .
```

---

## **Basic Usage**

### **1. Detect Flood (GEE)**

```python
from floodrisk.inundation import detect_flood
from floodrisk.exportcsv import export_flood_map
from floodrisk.geeauth import initialize

# Authenticate GEE
initialize(project_id='your-project-id')

# Detect flood
result = detect_flood(
    aoi_name='Feni',
    before_start='2025-01-01', before_end='2025-01-31',
    after_start='2025-07-01', after_end='2025-07-12'
)

print("Flooded Area (ha):", result['Flooded Area (ha)'].getInfo())

# Export to Google Drive
export_flood_map(result['flooded_image'], 'Flood_Extent', 'GEE_Flood')
```

---

### **2. Damage Assessment**

```python
from shapely.geometry import Polygon
from floodrisk.damage import get_osm_data, compute_flood_damage_fast

# AOI polygon (example)
aoi_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

# Download roads & buildings
roads, buildings = get_osm_data(aoi_polygon)

# Flood raster path (GeoTIFF exported from GEE)
flood_tif_path = "Flood_Extent.tif"

# Compute damage
result = compute_flood_damage_fast(roads, buildings, flood_tif_path)

print(result['road_stats'])
print(result['building_stats'])
```

---

## **Output Example**

✔ **Flood Stats:**

```
AOI: Feni
Otsu Threshold: 1.21
Total Area: 88,029 ha
Flooded Area: 18,647 ha
Inundation: 21%
```

✔ **Damage Summary:**

```
Road Damage Summary:
Category           Total Length (km)  Flooded Length (km)  Flooded %
National Highways             207.05                 4.03       1.94
Regional Roads                322.97                14.40       4.46
Local Roads                  1909.71               111.38       5.83

Building Damage Summary:
{'Total Buildings': 161204, 'Flooded Buildings': 5242, 'Flooded %': 3.25}
```

---

## **Citation**

If you use this package in your research, please cite:

```
Rahman, M.R. (2025). FloodRisk: A Python Package for Flood Detection and Damage Assessment.
Zenodo. DOI: https://doi.org/10.xxxx/zenodo.xxxxx
```

---

## **License**

[MIT License](LICENSE)
