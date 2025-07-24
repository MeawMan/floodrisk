import argparse
from shapely.geometry import Polygon
from floodrisk import inundation, exportmap, osmdata, damage, exportcsv, visualize

def main():
    parser = argparse.ArgumentParser(description="Flood Inundation and Damage Assessment")
    
    # Arguments
    parser.add_argument("--aoi", type=str, help="AOI name for GEE inundation or polygon coordinates", required=True)
    parser.add_argument("--before_start", type=str, help="Before flood start date (YYYY-MM-DD)")
    parser.add_argument("--before_end", type=str, help="Before flood end date (YYYY-MM-DD)")
    parser.add_argument("--after_start", type=str, help="After flood start date (YYYY-MM-DD)")
    parser.add_argument("--after_end", type=str, help="After flood end date (YYYY-MM-DD)")
    parser.add_argument("--flood_raster", type=str, help="Path to flood raster for damage calculation")
    parser.add_argument("--output", type=str, help="Output folder for reports", default="results")
    parser.add_argument("--visualize", action="store_true", help="Show inundation map")
    
    args = parser.parse_args()

    # If dates provided, calculate inundation using GEE
    if args.before_start and args.before_end and args.after_start and args.after_end:
        print("📡 Running GEE-based flood detection...")
        result = inundation(args.aoi, args.before_start, args.before_end, args.after_start, args.after_end)
        print("\n✅ Inundation Stats:")
        print(f"AOI: {result['AOI']}")
        print(f"Otsu Threshold: {result['Otsu Threshold']}")
        print(f"Total Area (ha): {result['Total Area (ha)'].getInfo()}")
        print(f"Flooded Area (ha): {result['Flooded Area (ha)'].getInfo()}")
        print(f"Inundation %: {result['Inundation %'].getInfo()}")
        
        # Export flood map
        exportmap(result['flooded_image'], f"{args.aoi}_flood_map", args.output, result['aoi'])

    # If raster provided, run damage assessment
    if args.flood_raster:
        print("\n📊 Running damage assessment...")
        
        # Example AOI polygon for OSM (for CLI simplicity, use a fixed AOI)
        # TODO: Replace with actual user AOI from shapefile or coordinates if needed
        example_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])
        
        roads, buildings = osmdata(example_polygon)
        damage_result = damage(roads, buildings, args.flood_raster)
        
        print("\n✅ Road Damage Summary:")
        print(damage_result['road_stats'])
        print("\n✅ Building Damage Summary:")
        print(damage_result['building_stats'])
        
        exportcsv(damage_result['road_stats'], damage_result['building_stats'], args.output)

    # Visualization
    if args.visualize and args.flood_raster:
        visualize(args.flood_raster)

if __name__ == "__main__":
    main()
