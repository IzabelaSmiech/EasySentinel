from multiprocessing.spawn import import_main_path
import rasterio
from main_class import MainClass
from raster_loader import b1, b2, b3, b4, b5, b6, b7, b8, b9, b11, b12
from config import datafolder_path
import matplotlib.pyplot as plt
import numpy as np

class CalculateIndex(MainClass):
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

    def ndvi(self, plot = True, colormap = 'YlGn'):
        self.plot = plot
        self.cmap = colormap
        outfile = r'ndvi.tif'

        with rasterio.open(self.b4, driver='JP2OpenJPEG') as red:
            RED = red.read()
        with rasterio.open(self.b8, driver='JP2OpenJPEG') as nir:
            NIR = nir.read()

        ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR.astype(float) + RED.astype(float))
        
        print('\nMin NDVI: {m}'.format(m=np.nanmin(ndvi)))
        print('Max NDVI: {m}'.format(m=np.nanmax(ndvi)))
        print('Mean NDVI: {m}'.format(m=np.nanmean(ndvi)))
        print('Median NDVI: {m}'.format(m=np.nanmedian(ndvi)))

        if self.plot == True:
            plt.imshow(np.squeeze(ndvi), cmap=self.cmap)
            plt.title('NDVI')
            plt.colorbar()
            plt.show()
        else:
            pass

        profile = red.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32))

    def gndvi(self, plot = True, colormap = 'YlGn'):
        self.plot = plot
        self.cmap = colormap
        outfile = r'gndvi.tif' 
        with rasterio.open(self.b3, driver='JP2OpenJPEG') as green:
            GREEN = green.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        gndvi = (NIR.astype(float) - GREEN.astype(float)) / (NIR.astype(float) + GREEN.astype(float))
        
        print('\nMin GNDVI: {m}'.format(m=np.nanmin(gndvi)))
        print('Max GNDVI: {m}'.format(m=np.nanmax(gndvi)))
        print('Mean GNDVI: {m}'.format(m=np.nanmean(gndvi)))
        print('Median GNDVI: {m}'.format(m=np.nanmedian(gndvi)))

        if self.plot == True:
            plt.imshow(np.squeeze(gndvi), cmap=self.cmap)
            plt.title('GNDVI')
            plt.colorbar()
            plt.show()
        else:
            pass 

        profile = green.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(gndvi.astype(rasterio.float32))

    def savi(self, L = 0.5, plot = True, colormap = 'YlOrBr'):
        self.plot = plot
        self.cmap = colormap
        self.l = L
        outfile = r'savi.tif' 
        with rasterio.open(self.b4, driver='JP2OpenJPEG') as red:
            RED = red.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        savi = (NIR.astype(float) - RED.astype(float)) / (NIR.astype(float) + RED.astype(float) + self.l) * (1 + self.l)
        
        print('\nMin SAVI: {m}'.format(m=np.nanmin(savi)))
        print('Max SAVI: {m}'.format(m=np.nanmax(savi)))
        print('Mean SAVI: {m}'.format(m=np.nanmean(savi)))
        print('Median SAVI: {m}'.format(m=np.nanmedian(savi)))

        if self.plot == True:
            plt.imshow(np.squeeze(savi), cmap=self.cmap)
            plt.title('SAVI')
            plt.colorbar()
            plt.show()
        else:
            pass 

        profile = red.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(savi.astype(rasterio.float32))

    def ndmi(self, plot = True, colormap = 'RdYlBu'):
        self.plot = plot
        self.cmap = colormap
        outfile = r'ndmi.tif' 
        with rasterio.open(self.b11, driver='JP2OpenJPEG') as swir:
            SWIR = swir.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        ndmi = (NIR.astype(float) - SWIR.astype(float)) / (NIR.astype(float) + SWIR.astype(float))
        
        print('\nMin NDMI: {m}'.format(m=np.nanmin(ndmi)))
        print('Max NDMI: {m}'.format(m=np.nanmax(ndmi)))
        print('Mean NDMI: {m}'.format(m=np.nanmean(ndmi)))
        print('Median NDMI: {m}'.format(m=np.nanmedian(ndmi)))

        if self.plot == True:
            plt.imshow(np.squeeze(ndmi), cmap=self.cmap)
            plt.title('NDMI')
            plt.colorbar()
            plt.show()
        else:
            pass 

        profile = swir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndmi.astype(rasterio.float32))

    def ndwi(self, plot = True, colormap = 'Blues'):
        self.plot = plot
        self.cmap = colormap
        outfile = r'ndwi.tif' 
        with rasterio.open(self.b3, driver='JP2OpenJPEG') as green:
            GREEN = green.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        ndwi = (GREEN.astype(float) - NIR.astype(float)) / (GREEN.astype(float) + NIR.astype(float))
        
        print('\nMin NDWI: {m}'.format(m=np.nanmin(ndwi)))
        print('Max NDWI: {m}'.format(m=np.nanmax(ndwi)))
        print('Mean NDWI: {m}'.format(m=np.nanmean(ndwi)))
        print('Median NDWI: {m}'.format(m=np.nanmedian(ndwi)))

        if self.plot == True:
            plt.imshow(np.squeeze(ndwi), cmap=self.cmap)
            plt.title('NDWI')
            plt.colorbar()
            plt.show()
        else:
            pass 

        profile = nir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndwi.astype(rasterio.float32))

    def nbr(self, plot = True, colormap = 'RdYlGn'):
        self.plot = plot
        self.cmap = colormap
        outfile = r'nbr.tif'

        with rasterio.open(self.b12, driver='JP2OpenJPEG') as swir:
            SWIR = swir.read()
        with rasterio.open(self.b8) as nir:
            NIR = nir.read()

        nbr = (NIR.astype(float) - SWIR.astype(float)) / ((NIR.astype(float) + SWIR.astype(float)))
        
        print('\nMin NBR: {m}'.format(m=np.nanmin(nbr)))
        print('Max NBR: {m}'.format(m=np.nanmax(nbr)))
        print('Mean NBR: {m}'.format(m=np.nanmean(nbr)))
        print('Median NBR: {m}'.format(m=np.nanmedian(nbr)))

        if self.plot == True:
            plt.imshow(np.squeeze(nbr), cmap=self.cmap)
            plt.title('NBR')
            plt.colorbar()
            plt.show()
        else:
            pass

        profile = swir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(nbr.astype(rasterio.float32))

z = CalculateIndex(datafolder_path)
z.ndvi()
