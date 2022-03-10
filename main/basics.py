from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import os 
import rasterio
import numpy as np
import fiona
import random
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from rasterio.windows import Window
from config import datafolder_path, band_name, band_path
from dict_band_length import band_lenght_dict
from main_class import MainClass
from raster_loader import b1, b2, b3, b4, b5, b6, b7, b8, b9, b11, b12

class RasterOperations(MainClass):
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

    def __pretty(self,d, indent=0):
        for key, value in d.items():
            print('*' + '\t' * indent + str(key) + ":")
            if isinstance(value, dict):
                self.__pretty(value, indent+1)
                print('\t' * indent)
            else:
                print('\t' * (indent+1) + str(value))
                print('\t' * indent)
                print('\t' * indent + '---------')

    def band_info(self):
        print("Band statistics and information:")
        self.band = band_name
        self.path = band_path
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
        self.__pretty(stats_dict)

    def data_info(self):
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
        self.__pretty(namingDict)

    def create_truecolor(self):
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

    def mask_band(self, shapefile_path):
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

    def crop_band(self, x_size, y_size):
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

        with rasterio.open(band_input, driver='JP2OpenJPEG') as src:
            xsize, ysize = x_size,  y_size

            xmin, xmax = 0, src.width - xsize
            ymin, ymax = 0, src.height - ysize
            xoff, yoff = random.randint(xmin, xmax), random.randint(ymin, ymax)
 
            window = Window(xoff, yoff, xsize, ysize)
            transform = src.window_transform(window)

            profile = src.profile
            profile.update({
                'height': xsize,
                'width': ysize,
                'transform': transform})

            with rasterio.open('crop_file.tiff', 'w', **profile) as dst:
                dst.write(src.read(window=window))

    def band_histogram(self):
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

        print("Which band do you want to crop?")
        band_input = input("b1 | b2 | b3 | b4 | b5 | b6 | b7 | b8 | b9 | b11 | b12: \n")
        
        if band_input == 'b1':
            band_input = self.b1
        elif band_input == 'b2':
            band_input = self.b2
        elif band_input == 'b3':
            band_input = self.b3
        elif band_input == 'b4':            band_input = self.b4
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



a = RasterOperations(datafolder_path)
#a.data_info()
#a.band_info()
#a.create_truecolor()
#a.create_falsecolor()
#a.mask_band('C:/Users/izka1/OneDrive/Pulpit/maska/maska.shp')
#a.crop_band(512, 512)
#a.band_histogram()
a.sampling([(654530,6052193), (702069,5997353), (662635,6022760)])