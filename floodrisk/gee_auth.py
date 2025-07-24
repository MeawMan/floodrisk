import ee

def initialize(project_id=None):
    """
    Authenticate and initialize Google Earth Engine.
    Args:
        project_id (str): Google Cloud Project ID.
    """
    print("Authenticating with Google Earth Engine...")
    ee.Authenticate()
    ee.Initialize(project=project_id)
    print("Earth Engine initialized successfully.")
