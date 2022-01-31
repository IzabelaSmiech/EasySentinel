import rasterio
import math
from main_class import MainClass
from raster_loader import b3, b4, b5, b6, b7, b8, b11
from config import datafolder_path

class CalculateIndex(MainClass):
    def __init__(self, datafolder_path):
        super().__init__(datafolder_path)
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
        self.b8 = b8
        self.b11 = b11

    def ndvi(self):
        outfile = r'ndvi.tif' 
        with rasterio.open(self.b4, driver='JP2OpenJPEG') as red:
            RED = red.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR+RED)
        
        profile = red.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32))

    def gndvi(self):
        outfile = r'gndvi.tif' 
        with rasterio.open(self.b3, driver='JP2OpenJPEG') as green:
            GREEN = green.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        gndvi = (NIR.astype(float) - GREEN.astype(float)) / (NIR+GREEN)
        
        profile = green.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(gndvi.astype(rasterio.float32))

    def ndmi(self):
        outfile = r'ndmi.tif' 
        with rasterio.open(self.b11, driver='JP2OpenJPEG') as swir:
            SWIR = swir.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        ndmi = (NIR.astype(float) - SWIR.astype(float)) / (NIR+SWIR)
        
        profile = swir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndmi.astype(rasterio.float32))

    def ndsi(self):
        outfile = r'ndsi.tif' 
        with rasterio.open(self.b3, driver='JP2OpenJPEG') as green:
            GREEN = green.read()
        with rasterio.open(self.b11) as swir:
            SWIR = swir.read()

        ndsi = (GREEN.astype(float) - SWIR.astype(float)) / (GREEN+SWIR)
        
        profile = swir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndsi.astype(rasterio.float32))

    def ireci(self):
        outfile = r'ireci.tif' 
        with rasterio.open(self.b4, driver='JP2OpenJPEG') as red:
            RED = red.read()
        with rasterio.open(self.b5) as red2:
            RED2 = red2.read()
        with rasterio.open(self.b6) as red3:
            RED3 = red3.read()
        with rasterio.open(self.b7) as red4:
            RED4 = red4.read()

        ireci = (RED4.astype(float) - RED.astype(float)) / (RED2.astype(float) / RED3.astype(float))
        
        profile = red.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ireci.astype(rasterio.float32))

z = CalculateIndex(datafolder_path)
z.ndvi()
