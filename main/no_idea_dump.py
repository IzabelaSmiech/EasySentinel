from osgeo import gdal,ogr,osr
import rasterio
from rasterio import plot
import os 
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import warnings
import matplotlib.pyplot as plt
from rasterio.plot import show
from zipfile import ZipFile
import convert_coords
import random
from convert_coords import listarray
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

def GetExtent(ds):
    """ Return list of corner coordinates from a gdal Dataset """
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)

def ReprojectCoords(coords,src_srs,tgt_srs):
    """ Reproject a list of x,y coordinates. """
    trans_coords=[]
    transform = osr.CoordinateTransformation( src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords

imagePath = 'data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE\\GRANULE\\L2A_T29SQC_A026732_20200804T111447\\IMG_DATA\\R10m\\T29SQC_20200804T110631_B02_10m.jp2'

#import bands as separate 1 band raster

#band2 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B02_10m.jp2'), driver='JP2OpenJPEG') #blue

ds=gdal.Open(imagePath)

ext=GetExtent(ds)

src_srs=osr.SpatialReference()
src_srs.ImportFromWkt(ds.GetProjection())
#tgt_srs=osr.SpatialReference()
#tgt_srs.ImportFromEPSG(4326)
tgt_srs = src_srs.CloneGeogCS()

geo_ext=ReprojectCoords(ext, src_srs, tgt_srs)

####another

imagePath = 'data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE\\GRANULE\\L2A_T29SQC_A026732_20200804T111447\\IMG_DATA\\R10m'

#import bands as separate 1 band raster

band2 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B02_10m.jp2'), driver='JP2OpenJPEG') #blue
band3 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B03_10m.jp2'), driver='JP2OpenJPEG') #green
band4 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B04_10m.jp2'), driver='JP2OpenJPEG') #red
band8 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B08_10m.jp2'), driver='JP2OpenJPEG') #nir


my_result = [(B5 - B4) - 0.2 * (B5 - B3)] * (B5 - B4)

array1 = band2.read(1)
plot.show(band4)
flatarray = array1.flatten()
listarray = flatarray.tolist()

plt.hist(listarray, bins=60)
plt.show()

a = [(754.6,4248548.6), (754222.6,4248548.6), (54.6,4248548.6)]
sample = np.array(list(rasterio.sample.sample_gen(band2, a))).flatten()

class sample:
    def __init__(self, raster:str, list_of_coords:list):
        self.raster = raster
        self.coords = list_of_coords


    def get_value(self) -> list:
        sample = np.array(list(rasterio.sample.sample_gen(self.raster, self.coords))).flatten()
        polygon = Polygon([(self.raster.bounds.left, self.raster.bounds.bottom),
                           (self.raster.bounds.left, self.raster.bounds.top),
                           (self.raster.bounds.right, self.raster.bounds.top),
                           (self.raster.bounds.right, self.raster.bounds.bottom)])

        for idx, i in enumerate(range(len(self.coords))):
            point = Point(self.coords[i])
            if polygon.contains(point) == False:
                warnings.warn(f"coords {self.coords[idx]} are out of raster bounds - {self.raster.bounds[0:5]}") #or print function
        print(sample)
        '''
        for idx, element in enumerate(sample):
            if element == 0:
            print(f"coords {a[idx]} out of raster")     
                '''
a = [(75,42485), (754222.6,4248548.6), (54.6,4248548.6)]
sample(band2, a).get_value()

####another

def check_path(my_path) -> bool:
        if my_path[-3:] == 'zip':
            print("zip to jest, zaraz otworze")
        archive = ZipFile(my_path)
        for file in archive.namelist():
            if file.startswith('GRANULE'):
                archive.extract(file, 'destination_path')
        else: 
            print("nie jest to zip debilu")


check_path('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE')
check_path('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE.zip')

####another

imagePath = 'data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE\\GRANULE\\L2A_T29SQC_A026732_20200804T111447\\IMG_DATA\\R10m'

#import bands as separate 1 band raster

band2 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B02_10m.jp2'), driver='JP2OpenJPEG') #blue
band3 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B03_10m.jp2'), driver='JP2OpenJPEG') #green
band4 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B04_10m.jp2'), driver='JP2OpenJPEG') #red
band8 = rasterio.open(os.path.join(imagePath, 'T29SQC_20200804T110631_B08_10m.jp2'), driver='JP2OpenJPEG') #nir

print('raster bands: ', band4.count) #number of raster bands
print('columns: ', band4.width) #number of raster columns
print('rows: ', band4.height) #number of raster rows

print(type(band4))
#show(band4)
#show(band2)
#show(band8)

print(band4.dtypes[0]) #type of raster byte
print(band4.crs) #raster sytem of reference - epsg
print(band4.transform) #raster transform parameters
print(band4.read(1)) #raster values as matrix array
print('---------------------------------')


class sample:
    def __init__(self, my_raster:str, pairs_of_coords:list): #czy użytkownik podaje band czy my wybieramy? 
        self.my_raster = my_raster
        self.coords = pairs_of_coords 

    def get_sample(self) -> list:
        sample = np.array(list(rasterio.sample.sample_gen(self.my_raster, self.coords))).flatten()
        return sample

sample(band2, ['754707','4248548']).get_sample()


### another

mypath = 'data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE'

print('abs path:',os.path.abspath(mypath))
print(os.path.basename(mypath))

print('dirname:', os.path.dirname(mypath))

print(os.path.exists(mypath))
print(os.path.lexists(mypath))

path2 = 'sentinel_2\\S2B_MSIL1C_20210331T205019_N0300_R057_T17XNL_20210406T182916.SAFE'

os.path.basename(path2)
notreal = os.path.abspath(path2) #not a real path!!!
print(os.path.exists(notreal))


#####another

class sample:
    def __init__(self, raster:str, list_of_coords:list):
        self.raster = raster
        self.coords = list_of_coords


    def get_value(self) -> list:
        sample = np.array(list(rasterio.sample.sample_gen(self.raster, self.coords))).flatten()
        polygon = Polygon([(self.raster.bounds.left, self.raster.bounds.bottom),
                           (self.raster.bounds.left, self.raster.bounds.top),
                           (self.raster.bounds.right, self.raster.bounds.top),
                           (self.raster.bounds.right, self.raster.bounds.bottom)])

        for idx, i in enumerate(range(len(self.coords))):
            point = Point(self.coords[i])
            if polygon.contains(point) == False:
                warnings.warn(f"coords {self.coords[idx]} are out of raster bounds - {self.raster.bounds[0:5]}") #or print function
        print(sample)

'''
example:

raster = raster image here
my_points = [(75,42), (95,11), (54.6,41)]
sample(raster, my_points).get_value()
'''

#####another


coordinates = np.random.randint(0, 100, size=(30, 10, 2))
#stworzenie random 3d array
data = np.random.random(size=(3, 1, 3)) + 10
x=2

#stworzenie random wartości (lista)

randomlist = random.sample(range(1, 10000), 100)
print(randomlist)

random_values = np.random.choice(listarray, size=(10, 2, 2))
print(random_values)

#plot

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
z, x, y = random_values.nonzero()
ax.scatter(x, y, z, c=z, alpha=1)
plt.show()