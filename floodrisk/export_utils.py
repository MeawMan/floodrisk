import pandas as pd
import os

def export_csv(road_stats: pd.DataFrame, building_stats: dict, output_folder: str, prefix: str = "flood_damage"):
    """
    Export road and building flood damage statistics to CSV files.

    Parameters
    ----------
    road_stats : pandas.DataFrame
        DataFrame containing road flood damage statistics.
    building_stats : dict
        Dictionary containing building flood damage statistics.
    output_folder : str
        Path to folder where CSV files will be saved.
    prefix : str, optional
        File name prefix for the CSV files (default is 'flood_damage').

    Returns
    -------
    tuple
        Paths of the saved CSV files (road_stats_path, building_stats_path).
    
    Usage
    -----
    >>> from floodrisk import export_csv
    >>> export_csv(road_stats, building_stats, "output/reports")
    """
    try:
        os.makedirs(output_folder, exist_ok=True)

        # File paths
        road_file = os.path.join(output_folder, f"{prefix}_road_stats.csv")
        building_file = os.path.join(output_folder, f"{prefix}_building_stats.csv")

        # Export CSVs
        road_stats.to_csv(road_file, index=False)
        pd.DataFrame([building_stats]).to_csv(building_file, index=False)

        print(f"✅ Reports saved:\n- {road_file}\n- {building_file}")
        return road_file, building_file

    except Exception as e:
        print(f"Error exporting CSV files: {e}")
        return None, None
