import ee

def initialize(project_id: str = None):
    """
    Authenticate and initialize Google Earth Engine (GEE).

    Parameters
    ----------
    project_id : str, optional
        Google Cloud Project ID (required for GEE quota and advanced features).
        If None, uses default credentials.

    Usage
    -----
    >>> from floodrisk import initialize
    >>> initialize(project_id="your-gcp-project-id")
    """
    try:
        print("🔐 Authenticating with Google Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project=project_id)
        print("Earth Engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
