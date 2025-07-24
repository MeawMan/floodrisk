from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="floodrisk",  # Package name on PyPI
    version="1.0.0",  # Bumped version for stable release
    author="Mahfujur Rahman Joy",
    author_email="mahfuj2sust@gmail.com",  # You can remove if private
    description="Flood detection and damage assessment using Sentinel-1 SAR and OSM data with Google Earth Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",  # For PyPI Markdown rendering
    url="https://github.com/MeawMan/floodrisk",  # GitHub repository
    project_urls={
        "Documentation": "https://github.com/MeawMan/floodrisk",
        "PyPI": "https://pypi.org/project/floodrisk/",
        "DOI": "https://doi.org/10.5281/zenodo.16407193",
    },
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "geemap>=0.20.6",
        "earthengine-api>=0.1.400",
        "osmnx>=1.8.0",
        "geopandas>=0.12.0",
        "rasterio>=1.3.0",
        "shapely>=2.0.0",
        "pandas>=1.5.0",
        "matplotlib>=3.6.0",
    ],
    entry_points={
        "console_scripts": [
            "floodrisk=floodrisk.floodrisk_cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    keywords="flood detection SAR Sentinel-1 OSM geospatial Google Earth Engine",
)
