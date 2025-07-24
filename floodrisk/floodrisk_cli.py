import argparse
from shapely.geometry import Polygon
from floodrisk import initialize, detect_flood, export_map, download_osm_data, compute_flood_damage, export_csv, visualize_map

def main():
    parser = argparse.ArgumentParser(description="FloodRisk: Flood Detection & Damage Assessment Tool")

    # Main arguments
    parser.add_argument("--project", type=str, help="Google Cloud Project ID for GEE")
    parser.add_argument("--aoi", type=str, help="AOI name (ADM2 in Bangladesh) or WKT polygon", required=True)
    parser.add_argument("--before_start", type=str, help="Before flood start date (YYYY-MM-DD)")
    parser.add_argument("--before_end", type=str, help="Before flood end date (YYYY-MM-DD)")
    parser.add_argument("--after_start", type=str, help="After flood start date (YYYY-MM-DD)")
    parser.add_argument("--after_end", type=str, help="After flood end date (YYYY-MM-DD)")
    parser.add_argument("--flood_raster", type=str, help="Path to flood raster for damage calculation")
    parser.add_argument("--output", type=str, help="Output folder for reports", default="results")
    parser.add_argument("--visualize", action="store_true", help="Show inundation map")
    args = parser.parse_args()

    # Step 1: Initialize GEE
    if args.project:
        initialize(args.project)

    # Step 2: Flood detection
    if args.before_start and args.before_end and args.after_start and args.after_end:
        print("📡 Running GEE-based flood detection...")
        result = detect_flood(args.aoi, args.before_start, args.before_end, args.after_start, args.after_end)

        print("\n✅ Inundation Stats:")
        print(f"AOI: {result['AOI']}")
        print(f"Otsu Threshold: {result['Otsu Threshold']}")
        print(f"Total Area (ha): {result['Total Area (ha)'].getInfo()}")
        print(f"Flooded Area (ha): {result['Flooded Area (ha)'].getInfo()}")
        print(f"Inundation %: {result['Inundation %'].getInfo()}")

        export_map(result['flooded_image'], f"{args.aoi}_flood_map", args.output, result['aoi'])

    # Step 3: Damage assessment
    if args.flood_raster:
        print("\n📊 Running damage assessment...")

        # For CLI simplicity: sample polygon (future: allow shapefile or coordinates)
        example_polygon = Polygon([(91.15, 23.40), (91.20, 23.40), (91.20, 23.45), (91.15, 23.45)])

        roads, buildings = download_osm_data(example_polygon)
        damage_result = compute_flood_damage(roads, buildings, args.flood_raster)

        print("\n✅ Road Damage Summary:")
        print(damage_result['road_stats'])
        print("\n✅ Building Damage Summary:")
        print(damage_result['building_stats'])

        export_csv(damage_result['road_stats'], damage_result['building_stats'], args.output)

    # Step 4: Visualization
    if args.visualize and args.flood_raster:
        visualize_map(args.flood_raster)

if __name__ == "__main__":
    main()
