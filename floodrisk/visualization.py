import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd

def visualize(flood_tif_path, aoi_shapefile=None):
    """Visualize flood inundation raster with optional AOI boundary."""
    with rasterio.open(flood_tif_path) as src:
        flood_array = src.read(1)
        fig, ax = plt.subplots(figsize=(10, 10))
        show(flood_array, transform=src.transform, cmap='Blues', ax=ax)
        if aoi_shapefile:
            gpd.read_file(aoi_shapefile).boundary.plot(ax=ax, edgecolor='black', linewidth=1.5)
        plt.title("Flood Inundation Map", fontsize=16)
        plt.axis('off')
        plt.show()
