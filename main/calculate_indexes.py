import rasterio

from datetime import datetime
from bandlength import band_lenght_dict
from config import datafolder_path, band_path
from raster_loader import b4, b8

class CalculateIndex():

    def ndvi(self, b4, b8):
        outfile = r'ndvi.tif' 
        with rasterio.open(b4[0], driver='JP2OpenJPEG') as red:
            RED = red.read()
        with rasterio.open(b8[0]) as nir:
            NIR = nir.read()

        ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR+RED)
        
        profile = red.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32))

z = CalculateIndex()
z.ndvi(b4, b8)