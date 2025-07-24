from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="floodrisk",  # Package name
    version="0.1.2",  # Increment version
    author="Mahfujur Rahman Joy",
    author_email="mahfujurjoy@example.com",  # Optional, can remove if private
    description="Flood detection and damage assessment using Sentinel-1 SAR and OSM data",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Required for Markdown on PyPI
    url="https://github.com/MeawMan/floodrisk",  # GitHub repo
    project_urls={  # Extra URLs
        "PyPI": "https://pypi.org/project/floodrisk/",
        "GitHub": "https://github.com/MeawMan/floodrisk",
        "DOI": "https://doi.org/10.5281/zenodo.16407193",
    },
    license="MIT",
    packages=find_packages(),  # Automatically finds all packages
    include_package_data=True,
    install_requires=[  # Dependencies
        "geemap",
        "earthengine-api",
        "osmnx",
        "geopandas",
        "rasterio",
        "shapely",
        "pandas",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "floodrisk=floodrisk.floodrisk_cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="flood detection, SAR, Sentinel-1, OSM, geospatial, Google Earth Engine",
)
