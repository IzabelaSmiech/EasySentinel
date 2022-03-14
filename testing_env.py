from EasySentinel.calculate_index import CalculateIndex
from EasySentinel.raster_operations import RasterOperations
from EasySentinel.config import datafolder_path

a = RasterOperations(datafolder_path)
b = CalculateIndex(datafolder_path)
#a.data_info()
#a.data_info(prettify=False) 
#a.create_falsecolor()
#a.create_truecolor()
#a.crop_band()
#a.mask_band('here path to the mask in shp')
#b.ndvi()
#b.gndvi(plot = False)
