from setuptools import setup, find_packages

setup(
    name='floodrisk',
    version='0.1.1',
    description='Flood inundation detection and damage assessment using Google Earth Engine and OSM data',
    author='Mahfujur Rahman Joy',
    author_email='mahfuj2sust@gmail.com',
    packages=find_packages(),
    install_requires=[
        'geemap',              
        'earthengine-api',    
        'osmnx',              
        'geopandas',          
        'rasterio',           
        'shapely',            
        'pandas',             
        'matplotlib'          
    ],
    entry_points={
        "console_scripts": [
            "floodrisk=floodrisk.floodrisk_cli:main",  
        ],
    },
    python_requires='>=3.8',
)
