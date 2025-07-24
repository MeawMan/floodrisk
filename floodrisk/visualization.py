import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd

def visualize_map(flood_tif_path: str, aoi_shapefile: str = None, cmap: str = 'Blues'):
    """
    Visualize flood inundation raster with optional AOI boundary overlay.

    Parameters
    ----------
    flood_tif_path : str
        Path to flood inundation GeoTIFF file.
    aoi_shapefile : str, optional
        Path to AOI shapefile for boundary overlay. Default is None.
    cmap : str, optional
        Colormap for flood visualization (default is 'Blues').

    Returns
    -------
    None
        Displays a matplotlib figure of the flood inundation map.

    Usage
    -----
    >>> from floodrisk import visualize_map
    >>> visualize_map("output/flood_map.tif", "data/aoi.shp")
    """
    try:
        with rasterio.open(flood_tif_path) as src:
            flood_array = src.read(1)

            fig, ax = plt.subplots(figsize=(10, 10))
            show(flood_array, transform=src.transform, cmap=cmap, ax=ax)

            if aoi_shapefile:
                try:
                    gpd.read_file(aoi_shapefile).boundary.plot(ax=ax, edgecolor='black', linewidth=1.5)
                except Exception as e:
                    print(f"⚠ Warning: Unable to load AOI shapefile: {e}")

            plt.title("Flood Inundation Map", fontsize=16)
            plt.axis('off')
            plt.show()

    except FileNotFoundError:
        print(f"Error: File not found - {flood_tif_path}")
    except Exception as e:
        print(f"Error visualizing map: {e}")
