import pandas as pd
import os

def exportcsv(road_stats, building_stats, output_folder, prefix="flood_damage"):
    """Save road and building damage stats as CSV."""
    os.makedirs(output_folder, exist_ok=True)
    road_stats.to_csv(os.path.join(output_folder, f"{prefix}_road_stats.csv"), index=False)
    pd.DataFrame([building_stats]).to_csv(os.path.join(output_folder, f"{prefix}_building_stats.csv"), index=False)
    print(f"Reports saved to {output_folder}")
