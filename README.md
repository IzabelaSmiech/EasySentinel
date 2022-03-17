# EasySentinel
![alt text](https://i.ibb.co/ZNKpbwv/bs5.png)

<!-- badges: start -->
<img src="https://img.shields.io/github/license/IzabelaSmiech/EasySentinel.svg" />
<!-- badges: end -->

## Table of contents
* [Introduction](#introduction)
  * [Supported data](#supported-data)
  * [Requirements](#requirements)
* [How to use](#how-to-use)
* [Examples of use](#examples-of-use)
* [Project status](#project-status)


## Introduction
EasySentinel is a module written for working with Sentinel-2 data. It enables calculating 8 idcides: NDVI, GNDVI, SAVI, NDMI, NDWI, NDSI, NBR, EVI2; masking; cropping; sampling; generating true color and false color; getting info about data and creating histograms for band's values. It is a graduation project for geoinformation engeenering studies (2018-2022).

### Supported data

This very module works only for sentinel-2 data products generated after 6 December 2016, downloaded in SAFE format without changing folder and file names. Any changes to naming structure or folder structure may cause issues. The best way to get the data is to download it through [Copernicus Open Access Hub](https://scihub.copernicus.eu/dhus/#/home). In order do to so, create an account (free) and log in. Switch from navigation mode to area mode and select an area. Select in advanced search "Mission: Sentinel-2" and if you will, select other parameters like cloud cover. For more detailed tutorial on how to download the data head to Youtube tutorial posted by [Stephen Barry](https://www.youtube.com/watch?v=sMax7wkUrlI) (available: 5.03.2022).

### Requirements
Before using this very module, user must already have installed:
- Python version >= 3.8.1
- Rasterio version >= 1.1.8
- Numpy version >= 1.22.2
- Shapely version >= 1.7.0
- Matplotlib version >= 3.5.1
- Seaborn version >= 0.11.0
- Fiona version >= 1.8.18

Please note that many libraries have their own dependencies. For example, Rasterio has one and it is GDAL version >= 1.11. 

## How to use

Clone or download the source code e.g. download ZIP and unpack files. Open files in desired IDE or code editor. Provide path to your data in *config.py* and if you plan on using band_info functionality, provide filename of chosen band. File *testing_env.py* holds examples showcasing how to use the module.

import desired class (either CalculateIndex for indices or RasterOperations for other) and datafolder_path:

```python
from EasySentinel.calculate_index import CalculateIndex
from EasySentinel.raster_operations import RasterOperations
from EasySentinel.config import datafolder_path
```
Create instance of class:

```python
a = RasterOperations(datafolder_path)
b = CalculateIndex(datafolder_path)
```
The only thing left to do is to use whatever method you want :) To find out what the possibilities are see: examples of use.

## Examples of use

Getting info about the data:

```python
#Informations about the data (mission ID, product level, datatake sensing time, PDGS Processing Baseline number, Relative Orbit number, tile number and format, Product Discriminator)

a.data_info()

#for output to be dictionary:
a.data_info(prettify = False)
```

Generating true color and false color tiff:

```python
#generating true color
a.create_truecolor()

#generating false color
a.create_falsecolor()
```

Calculating indicies:

```python
#Normalized Difference Moisture Index
b.ndmi()

#Normalized Difference Vegetation Index with color palette changed to Greens (defaults to RdYlGn)
b.ndvi(colormap = 'Greens')

#Soil Adjusted Vegetation Index without plotting the image and with changing soil brightness correction factor (defaults to 0.5)
b.savi(plot = False, L = 0.48)
```

Masking:
```python
a.mask_band('C:/Users/name/Documents/folder/mask.shp')
```

Vegetation indices plots example:
![alt text](https://i.ibb.co/NC9qb27/indices-example.png)

## Project status
This project is complete as it is a graduation project. Changes improving code are considered for the future after graduating as a different side project, not to be mistaken with continuation of this very project.

