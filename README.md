# EasySentinel
![alt text](https://i.ibb.co/ZNKpbwv/bs5.png)

<!-- badges: start -->
<img src="https://img.shields.io/github/license/IzabelaSmiech/EasySentinel.svg" />
<!-- badges: end -->

## Table of contents
* [Introduction](#introduction)
  * [Supported data](#supported-data)
  * [Requirements](#requirements)
  * [Structure](#structure)
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
- Matplotlib version >= 3.5.1

Please note that many libraries have their own dependencies. For example, Rasterio has one and it is GDAL version >= 1.11. 

### Structure

## How to use

## Examples of use

Getting info about the data:

Generating true color and false color tiff:

Calculating indicies:

```python
# 
#
z = CalculateIndex(datafolder_path)
z.ndsi()
# 
z = CalculateIndex(datafolder_path)
z.ndvi(colormap = 'Greens')
# 
z = CalculateIndex(datafolder_path)
z.savi(plot = False, L = 0.48)
```
Sampling:

Masking, cropping:

Histograms:


Vegetation indices example:
![alt text](https://i.ibb.co/NC9qb27/indices-example.png)

## Project status

