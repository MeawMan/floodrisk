import osmnx as ox
import geopandas as gpd
import pandas as pd
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
from shapely.ops import unary_union

ROAD_CATEGORIES = {
    'National Highways': ['motorway', 'trunk', 'primary'],
    'Regional Roads': ['secondary', 'tertiary'],
    'Local Roads': ['residential', 'unclassified', 'track', 'service']
}

def osmdata(aoi_polygon):
    """Download roads and buildings from OSM for a given AOI polygon."""
    print("⏳ Downloading OSM roads and buildings...")
    roads = ox.features_from_polygon(aoi_polygon, tags={'highway': True})
    roads = roads[['geometry', 'highway']].dropna(subset=['geometry'])
    roads['road_type'] = roads['highway'].apply(lambda x: x[0] if isinstance(x, list) else x)
    roads['category'] = roads['road_type'].apply(lambda x: next((k for k,v in ROAD_CATEGORIES.items() if x in v), 'Other'))

    buildings = ox.features_from_polygon(aoi_polygon, tags={'building': True})
    buildings = buildings[['geometry']].dropna(subset=['geometry'])

    roads_metric = roads.to_crs(epsg=3857)
    roads['length_km'] = roads_metric.length / 1000
    print(f"Downloaded {len(roads)} roads and {len(buildings)} buildings.")
    return roads, buildings

def _raster_to_polygons(flood_tif_path):
    """Convert flood raster to polygons."""
    with rasterio.open(flood_tif_path) as src:
        flood_array = src.read(1)
        transform = src.transform
        crs = src.crs
    mask = flood_array > 0
    polygons = [shape(geom) for geom, val in shapes(flood_array, mask=mask, transform=transform) if val > 0]
    return gpd.GeoDataFrame(geometry=polygons, crs=crs)

def damage(roads, buildings, flood_tif_path):
    """Calculate flood damage for roads and buildings."""
    flood_polygons = _raster_to_polygons(flood_tif_path)
    print(f"Flood polygons extracted: {len(flood_polygons)}")
    flood_union = unary_union(flood_polygons.geometry)

    roads = roads.to_crs(flood_polygons.crs)
    buildings = buildings.to_crs(flood_polygons.crs)

    flooded_roads_geom = roads.intersection(flood_union)
    flooded_metric = flooded_roads_geom.to_crs(epsg=3857)
    roads['flooded_length_km'] = flooded_metric.length / 1000

    flooded_buildings = buildings[buildings.intersects(flood_union)]

    road_summary = []
    for category in ROAD_CATEGORIES.keys():
        total_length = roads[roads['category'] == category]['length_km'].sum()
        flooded_length = roads[roads['category'] == category]['flooded_length_km'].sum()
        flooded_percent = (flooded_length / total_length * 100) if total_length > 0 else 0
        road_summary.append({
            'Category': category,
            'Total Length (km)': round(total_length, 2),
            'Flooded Length (km)': round(flooded_length, 2),
            'Flooded %': round(flooded_percent, 2)
        })

    building_stats = {
        'Total Buildings': len(buildings),
        'Flooded Buildings': len(flooded_buildings),
        'Flooded %': round((len(flooded_buildings) / len(buildings) * 100) if len(buildings) > 0 else 0, 2)
    }

    return {
        'road_stats': pd.DataFrame(road_summary),
        'building_stats': building_stats
    }
