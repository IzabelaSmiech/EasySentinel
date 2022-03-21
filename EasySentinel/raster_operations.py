from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from osgeo import gdal
import os 
import rasterio
import numpy as np
import fiona
import random
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from rasterio.windows import Window
from .config import band_name, band_path
from .dict_band_length import band_lenght_dict
from .main_class import MainClass
from .raster_loader import b1, b2, b3, b4, b5, b6, b7, b8, b9, b11, b12

class RasterOperations(MainClass):
    """
    Various operations on raster data from Sentinel-2. Inherits from MainClass(). \n
    ### How to use:
    from EasySentinel.raster_operations import RasterOperations \n
    from EasySentinel.config import datafolder_path \n
    a = RasterOperations(datafolder_path) \n
    a.data_info() \n
    ### Methods: \n
    `data_info()` - providing basic info about the data. Takes one parameter: pretty -> bool. True by default. Prettify parameter styles the returned info. Returns NonType if prettify = True; dict if prettify = False. \n
    `band_info()` - providing basic info about chosen band. Takes one parameter: pretty -> bool. True by default. Prettify parameter styles the returned info. Returns NonType if prettify = True; dict if prettify = False. \n
    `create_truecolor()` - returns a true color image in current working dir. Format: TIFF. Parameters: none. \n
    `create_falsecolor()` -  returns a false color image in current working dir. Format: TIFF. Parameters: none. \n
    `mask_band()` - returs a masked TIFF image. Takes one parameter: shapefile_path - path to chosen shp, must have the same CRS. \n
    `crop_band()` - crops a chosen band. Takes four parameters - coordinates\n
    `band_histogram()` - creates a histogram of band's values. \n
    `sampling()` - extracts raster values at given points. Returns a list object. 
    """

    def __init__(self, datafolder_path):
        super().__init__(datafolder_path)
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
        self.b8 = b8
        self.b9 = b9
        self.b11 = b11
        self.b12 = b12

    def __prettify(self, o, indent = 0):
        for key, value in o.items():
            print('*' + '\t' * indent + str(key) + ":")
            if isinstance(value, dict):
                self.__prettify(value, indent+1)
                print('\t' * indent)
            else:
                print('\t' * (indent+1) + str(value))
                print('\t' * indent)
                print('\t' * indent + '---------')

    def band_info(self, prettify = True):
        """Provides basic info about chosen band. Requires providing file name (band_name) in config. 

        Args:
            prettify (bool, optional): Changes how the info is printed to a prettier display ;). Defaults to True.

        Returns:
            NonType if prettify = True; dict if prettify = False
        """
        print("Band statistics and information:")
        self.band = band_name
        self.path = band_path
        self.pretty = prettify
        my_band = rasterio.open(os.path.join(self.path, self.band), driver='JP2OpenJPEG')
        my_band_stats = rasterio.open(os.path.join(self.path, self.band), driver='JP2OpenJPEG').read()
        self.band_name = self.band.split('_')[2]
        stats_dict = {
            "Band name": self.band_name,
            "Długość fali dla środka kanału [nm]": band_lenght_dict[self.band_name],
            "Bounding box": my_band.bounds,
            "Number of raster columns": my_band.width,
            "Number of raster rows": my_band.height,
            "Band CRS": my_band.crs,
            "Band max value": my_band_stats.max(),
            "Band min value": my_band_stats.min(),
            "Band mean value": my_band_stats.mean()
        }
        if self.pretty == True:
            self.__prettify(stats_dict)
        else: 
            print(stats_dict)
            return stats_dict

    def data_info(self, prettify = True):
        """Provides basic info about the data. Extracted from file name. 

        Args:
            prettify (bool, optional): Changes how the info is printed to a prettier display ;). Defaults to True.

        Returns:
            NonType if prettify = True; dict if prettify = False
        """
        self.pretty = prettify
        print('Datapath information:')
        my_path=self.datafolder_path
        filename = os.path.basename(my_path)
        date = filename[-54:-46]
        time = filename[-45:-39]
        fulldate = datetime.strptime(date + time, '%Y%m%d%H%M%S')
        date2 = filename[-20:-12]
        time2 = filename[-11:-5]
        fulldate2 = datetime.strptime(date2 + time2, '%Y%m%d%H%M%S')
        lastElement = os.path.basename(os.path.normpath(my_path))
        values = lastElement.split('_')
        keys = ['Mission ID', 'Product level', 'Datatake sensing time',
                    'PDGS Processing Baseline number', 'Relative Orbit number', 'Tile Number and format', 
                    'Product Discriminator']
        namingDict = dict(zip(keys, values))
        namingDict['Datatake sensing time'] = fulldate
        namingDict['Product Discriminator'] = fulldate2

        if self.pretty == True:
            self.__prettify(namingDict)
        else:
            print(namingDict)
            return namingDict

    def create_truecolor(self):
        """Returns a true color image in current working dir. Format: TIFF.
        """
        truecolor_file = r'truecolor.tiff'
        blue = rasterio.open(self.b2, driver='JP2OpenJPEG')
        green = rasterio.open(self.b3, driver='JP2OpenJPEG')
        red = rasterio.open(self.b4, driver='JP2OpenJPEG')

        truecolor = rasterio.open(truecolor_file, 'w', driver='Gtiff', width=red.width, height=red.height,
                                    count=3, crs=red.crs, transform=red.transform, dtype=red.dtypes[0])
        
        truecolor.write(blue.read(1),3)
        truecolor.write(green.read(1),2) 
        truecolor.write(red.read(1),1) 
        truecolor.close()

    def create_falsecolor(self):
        """Returns a false color image in current working dir. Format: TIFF.
        """
        falsecolor_file = r'falsecolor.tiff'
        blue = rasterio.open(self.b3, driver='JP2OpenJPEG')
        green = rasterio.open(self.b4, driver='JP2OpenJPEG')
        red = rasterio.open(self.b8, driver='JP2OpenJPEG')

        falsecolor = rasterio.open(falsecolor_file, 'w', driver='Gtiff', width=blue.width, height=blue.height,
                                    count=3, crs=blue.crs, transform=blue.transform, dtype='uint16')
        
        falsecolor.write(blue.read(1),3)
        falsecolor.write(green.read(1),2) 
        falsecolor.write(red.read(1),1) 
        falsecolor.close()

    def mask_band(self, shapefile_path:str):
        """Returns a masked image in current working dir. Format: TIFF. 

        Args:
            shapefile_path (str): a path to chosen shapefile. shp must have the same CRS and must overlay a file 
            user wants to mask. Example: `C:Users/myName/Documents/Folder/mask.shp`

        """

        with fiona.open(shapefile_path, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]

        print("Which band do you want to mask?")
        band_input = input("b1 | b2 | b3 | b4 | b5 | b6 | b7 | b8 | b9 | b11 | b12: \n")

        if band_input == 'b1':
            with rasterio.open(self.b1, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b2':
            with rasterio.open(self.b2, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b3':
            with rasterio.open(self.b3, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b4':
            with rasterio.open(self.b4, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b5':
            with rasterio.open(self.b5, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b6':
            with rasterio.open(self.b6, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b7':
            with rasterio.open(self.b7, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b8':
            with rasterio.open(self.b8, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b9':
            with rasterio.open(self.b9, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b11':
            with rasterio.open(self.b11, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        elif band_input == 'b12':
            with rasterio.open(self.b12, driver='JP2OpenJPEG') as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
        else:
            print(f'No such band as {band_input}')
            
        out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

        with rasterio.open("masked_file.tif", "w", **out_meta) as dest:
            dest.write(out_image)

    def crop_band(self, max_x:float, max_y:float, min_x:float, min_y:float):
        """Crops a selected band to a bbox provided as the arguments.

        Args:
            max_x (float): maximum x value
            max_y (float): maximum y value
            min_x (float): minimum x value
            min_y (float): minimum y value
        """

        print("Which band do you want to crop?")
        band_input = input("b1 | b2 | b3 | b4 | b5 | b6 | b7 | b8 | b9 | b11 | b12: \n")
        
        if band_input == 'b1':
            band_input = self.b1
        elif band_input == 'b2':
            band_input = self.b2
        elif band_input == 'b3':
            band_input = self.b3
        elif band_input == 'b4':
            band_input = self.b4
        elif band_input == 'b5':
            band_input = self.b5
        elif band_input == 'b6':
            band_input = self.b6
        elif band_input == 'b7':
            band_input = self.b7
        elif band_input == 'b8':
            band_input = self.b8
        elif band_input == 'b9':
            band_input = self.b9
        elif band_input == 'b11':
            band_input = self.b11
        elif band_input == 'b12':
            band_input = self.b12

        window = (max_x, max_y, min_x, min_y)
        open_band = gdal.Open(band_input)
        gdal.Translate('crop_raster.tif', open_band, projWin = window)

    def band_histogram(self):
        """Plots a histogram of values for selected band. 
        """
        print("Which bands' histogram do you want to print out?")
        band_input = input("b1 | b2 | b3 | b4 | b5 | b6 | b7 | b8 | b9 | b11 | b12: \n")
        band_title = band_input
        
        if band_input == 'b1':
            band_input = self.b1
        elif band_input == 'b2':
            band_input = self.b2
        elif band_input == 'b3':
            band_input = self.b3
        elif band_input == 'b4':
            band_input = self.b4
        elif band_input == 'b5':
            band_input = self.b5
        elif band_input == 'b6':
            band_input = self.b6
        elif band_input == 'b7':
            band_input = self.b7
        elif band_input == 'b8':
            band_input = self.b8
        elif band_input == 'b9':
            band_input = self.b9
        elif band_input == 'b11':
            band_input = self.b11
        elif band_input == 'b12':
            band_input = self.b12

        src = rasterio.open(band_input, driver='JP2OpenJPEG')
        values_array = src.read(1)
        values_array = [item for sublist in values_array for item in sublist]

        sns.set()
        sns.set_theme(style="ticks")
        ax = sns.histplot(values_array, kde=True, bins=60)
        ax.set_xlabel("Values", fontsize = 14)
        ax.set_ylabel("Frequency (count)", fontsize = 14)
        ax.set_title(f"Histogram of the {band_title}")
        plt.show()

    def sampling(self, list_of_coords:list) -> list:
        """Extracts raster values at given points. 

        Args:
            list_of_coords (list): point(s) coordinates. Must be in the same coordinate system as given raster.
            arg example: `list_of_coords = [(654530,6052193), (702069,5997353), (662635,2137)]`

        Returns:
            a list object containing raster values in the same order as coords were in `list_of_coords`
        """

        print("Which band values do you want to sample?")
        band_input = input("b1 | b2 | b3 | b4 | b5 | b6 | b7 | b8 | b9 | b11 | b12: \n")
        
        if band_input == 'b1':
            band_input = self.b1
        elif band_input == 'b2':
            band_input = self.b2
        elif band_input == 'b3':
            band_input = self.b3
        elif band_input == 'b4':
            band_input = self.b4
        elif band_input == 'b5':
            band_input = self.b5
        elif band_input == 'b6':
            band_input = self.b6
        elif band_input == 'b7':
            band_input = self.b7
        elif band_input == 'b8':
            band_input = self.b8
        elif band_input == 'b9':
            band_input = self.b9
        elif band_input == 'b11':
            band_input = self.b11
        elif band_input == 'b12':
            band_input = self.b12

        raster = rasterio.open(band_input, driver='JP2OpenJPEG')
        sample = np.array(list(rasterio.sample.sample_gen(raster, list_of_coords))).flatten()
        polygon = Polygon([(raster.bounds.left, raster.bounds.bottom),
                           (raster.bounds.left, raster.bounds.top),
                           (raster.bounds.right, raster.bounds.top),
                           (raster.bounds.right, raster.bounds.bottom)])

        for idx, i in enumerate(range(len(list_of_coords))):
            point = Point(list_of_coords[i])
            if polygon.contains(point) == False:
                print(f"coords {list_of_coords[idx]} are out of raster bounds - {raster.bounds[0:5]}") #or print function
        print(sample)
        return sample 