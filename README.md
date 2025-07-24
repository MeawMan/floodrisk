# 🌊 FloodRisk

[![PyPI](https://img.shields.io/pypi/v/floodrisk)](https://pypi.org/project/floodrisk/)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16407193.svg)](https://doi.org/10.5281/zenodo.16407193)

---

## 📌 Overview

**FloodRisk** is a Python package for **flood detection and damage assessment** using:

* **Sentinel-1 SAR imagery** (via Google Earth Engine)
* **Otsu thresholding** for flood extent mapping
* **OpenStreetMap (OSM) data** for infrastructure damage analysis
* **CSV & GeoTIFF export**
* **Visualization** of flood extent and results

---

## ✅ Key Features

✔ Flood inundation mapping with Sentinel-1 SAR
✔ Automatic thresholding using Otsu method
✔ Compute inundation percentage and area statistics
✔ Damage assessment for roads and buildings using OSM data
✔ Export results (CSV, GeoTIFF)
✔ Visualization of flood maps

---

## 🔍 Installation

Install from **PyPI**:

```bash
pip install floodrisk
```

From **source**:

```bash
git clone https://github.com/MeawMan/floodrisk.git
cd floodrisk
pip install -e .
```

---

## 🚀 Quick Start

### **1. Initialize Google Earth Engine**

```python
from floodrisk import initialize

# Authenticate GEE
initialize(project_id="your-project-id")
```

---

### **2. Detect Flood (Sentinel-1 via GEE)**

```python
from floodrisk import detect_flood, export_map

# Detect flood inundation
result = detect_flood(
    aoi_name="Feni",
    before_start="2025-01-01", before_end="2025-01-31",
    after_start="2025-07-01", after_end="2025-07-12"
)

print("Flooded Area (ha):", result['Flooded Area (ha)'].getInfo())

# Export flood map to Google Drive
export_map(result['flooded_image'], "Flood_Extent", "GEE_Flood")
```

---

### **3. Damage Assessment**

```python
from shapely.geometry import Polygon
from floodrisk import download_osm_data, compute_flood_damage, export_csv

# Define AOI polygon
aoi_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

# Download OSM roads & buildings
roads, buildings = download_osm_data(aoi_polygon)

# Flood raster (GeoTIFF from GEE export)
flood_tif_path = "Flood_Extent.tif"

# Compute flood damage
damage_result = compute_flood_damage(roads, buildings, flood_tif_path)

print(damage_result['road_stats'])
print(damage_result['building_stats'])

# Export results as CSV
export_csv(damage_result['road_stats'], damage_result['building_stats'], "output/reports")
```

---

### **4. Visualization**

```python
from floodrisk import visualize_map

visualize_map("Flood_Extent.tif", aoi_shapefile="aoi.shp")
```

---

## ✅ Output Example

```
AOI: Feni
Otsu Threshold: 1.21
Total Area: 88,029 ha
Flooded Area: 18,647 ha
Inundation: 21%
```

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

## ✅ CLI Usage

Run from terminal:

```bash
floodrisk --aoi Feni --before_start 2025-01-01 --before_end 2025-01-31 --after_start 2025-07-01 --after_end 2025-07-12 --flood_raster Flood_Extent.tif --output results --visualize
```

---

## 📜 Citation

```
Rahman, M.R. (2025). FloodRisk: A Python Package for Flood Detection and Damage Assessment.
Zenodo. https://doi.org/10.5281/zenodo.16407193
```

---

## ✅ License

## MIT License. See [LICENSE](LICENSE).
