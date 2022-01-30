import rasterio
import os
import matplotlib.pyplot as plt
from datetime import datetime
from bandlength import band_lenght_dict
from config import datafolder_path, band_path, band_name
from raster_loader import b2, b3, b4, b8

class FastSentinel():
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

    def band_info(self, Path:str, band:str):
        print("Band statistics and information:")
        my_band = rasterio.open(os.path.join(Path, band), driver='JP2OpenJPEG')
        my_band_stats = rasterio.open(os.path.join(Path, band), driver='JP2OpenJPEG').read()
        band_name = band.split('_')[2]
        stats_dict = {
            "Band name": band_name,
            "Długość fali dla środka kanału [nm]": band_lenght_dict[band_name],
            "Bounding box": my_band.bounds,
            "Number of raster columns": my_band.width,
            "Number of raster rows": my_band.height,
            "Band CRS": my_band.crs,
            "Band max value": my_band_stats.max(),
            "Band min value": my_band_stats.min(),
            "Band mean value": my_band_stats.mean()
        }
        self.__pretty(stats_dict)

    def data_info(self, my_path:str):
        print('Datapath information:')
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

    def create_truecolor(self, b2, b3, b4):
        truecolor_file = r'truecolor.tiff'
        blue = rasterio.open(b2[0], driver='JP2OpenJPEG')
        green = rasterio.open(b3[0], driver='JP2OpenJPEG')
        red = rasterio.open(b4[0], driver='JP2OpenJPEG')

        truecolor = rasterio.open(truecolor_file, 'w', driver='Gtiff', width=red.width, height=red.height,
                                    count=3, crs=red.crs, transform=red.transform, dtype=red.dtypes[0])
        
        truecolor.write(blue.read(1),3)
        truecolor.write(green.read(1),2) 
        truecolor.write(red.read(1),1) 
        truecolor.close()

    def create_falsecolor(self, b3, b4, b8):
        falsecolor_file = r'falsecolor.tiff'
        blue = rasterio.open(b3[0], driver='JP2OpenJPEG')
        green = rasterio.open(b4[0], driver='JP2OpenJPEG')
        red = rasterio.open(b8[0], driver='JP2OpenJPEG')

        falsecolor = rasterio.open(falsecolor_file, 'w', driver='Gtiff', width=blue.width, height=blue.height,
                                    count=3, crs=blue.crs, transform=blue.transform, dtype='uint16')
        
        falsecolor.write(blue.read(1),3)
        falsecolor.write(green.read(1),2) 
        falsecolor.write(red.read(1),1) 
        print(red.crs)
        falsecolor.close()

a = FastSentinel()
a.create_truecolor(b2,b3,b4)
a.create_falsecolor(b3, b4, b8)