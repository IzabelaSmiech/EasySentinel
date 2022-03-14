import rasterio
import numpy as np
import matplotlib.pyplot as plt
from .main_class import MainClass
from .raster_loader import b1, b2, b3, b4, b5, b6, b7, b8, b9, b11, b12


class CalculateIndex(MainClass):
    """
    Calculating 8 indicies: NDVI, GNDVI, SAVI, NDMI, NDWI, NDSI, NBR, EVI2. Inherits from MainClass(). \n
    ### How to use:
    from EasySentinel.calculate_index import CalculateIndex \n
    from EasySentinel.config import datafolder_path \n
    a = CalculateIndex(datafolder_path) \n
    a.ndvi() \n
    ### Methods: \n
    All methods have two optional parameters: `plot` for if one wants to plot an image and `colormap` for changing color scheme of the plot.
    `ndvi()` - calculating NDVI. Returns TIFF image in current working dir. \n
    `gndvi()` - calculating GNDVI. Returns TIFF image in current working dir. \n
    `savi()` - calculating SAVI. Returns TIFF image in current working dir. Takes one additional optional argument: `L`. It describes soil brightness correction factor. \n
    `ndmi()` - calculating NDMI. Returns TIFF image in current working dir. \n
    `ndwi()` - calculating NDWI. Returns TIFF image in current working dir. \n
    `ndsi()` - calculating NDSI. Returns TIFF image in current working dir. \n
    `nbr()` - calculating NBR. Returns TIFF image in current working dir. \n
    `evi2()` - calculating EVI2. Returns TIFF image in current working dir. 

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

    def ndvi(self, plot = True, colormap = 'RdYlGn'):
        """NDVI stands for Normalized Difference Vegetation Index. Often used to analyze vegetation.
        Values range from -1 to 1. The higher the value, the healthier vegetation. It uses the red and 
        near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlGn'.
        """
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

    def gndvi(self, plot = True, colormap = 'RdYlGn'):
        """GNDVI stands for Green Normalized Difference Vegetation Index. Often used to analyze vegetation.
        It is a modified version of NDVI. This variant is more sensitive to the chlorophyll content in 
        the flora. Values range from -1 to 1. The higher the value, the healthier vegetation. It uses the 
        green and near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlGn'.
        """
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

    def savi(self, L = 0.5, plot = True, colormap = 'RdYlGn'):
        """SAVI stands for Soil Adjusted Vegetation Index. Often used to analyze vegetation, soil and agriculture.
        Enables to correct NDVI for the influence of soil brightness in areas where vegetative cover is low.
        Values range from -1 to 1. It uses the red, near-infrared spectral bands and soil brightness correction 
        factor (L) default to 0.5 to accommodate most land cover types.


        Args:
            L (float, optional): soil brightness correction factor. Defaults to 0.5.
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlGn'.
        """
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
        """NDMI stands for Normalized Difference Moisture Index. Often used to analyze vegetation.
        It is used to determine vegetation water content. Values range from -1 to 1. 
        It uses the short-wave infrared and near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlBu'.
        """
        
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
        """NDWI stands for Normalized Difference Water Index. Often used to analyze vegetation and to highlight
        open water features in a satellite image, allowing a water body to “stand out” against the soil and vegetation.
        Values range from -1 to 1. It uses the green and near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'Blues'.
        """
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

    def ndsi(self, plot = True, colormap = 'Blues'):
        """NDSI stands for Normalized Difference Snow Index. It is commonly used in snow/ice cover mapping application as well 
        as glacier monitoring. It can difference well snow from clouds. It does not difference snow from water on
        it's own. Values range from -1 to 1. Values around 1 usually represent snow. It uses the green and short-wave infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'Blues'.
        """
        
        self.plot = plot
        self.cmap = colormap
        outfile = r'ndsi.tif'

        with rasterio.open(self.b3, driver='JP2OpenJPEG') as green:
            GREEN = green.read()
        with rasterio.open(self.b11, driver='JP2OpenJPEG') as swir:
            SWIR = swir.read()

        ndsi = (GREEN.astype(float) - SWIR.astype(float)) / (GREEN.astype(float) + SWIR.astype(float))
        
        print('\nMin NDSI: {m}'.format(m=np.nanmin(ndsi)))
        print('Max NDSI: {m}'.format(m=np.nanmax(ndsi)))
        print('Mean NDSI: {m}'.format(m=np.nanmean(ndsi)))
        print('Median NDSI: {m}'.format(m=np.nanmedian(ndsi)))

        if self.plot == True:
            plt.imshow(np.squeeze(ndsi), cmap=self.cmap)
            plt.title('NDSI')
            plt.colorbar()
            plt.show()
        else:
            pass 

        profile = green.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(ndsi.astype(rasterio.float32))

    def nbr(self, plot = True, colormap = 'RdYlGn'):
        """NBR stands for Normalized Burned Ratio Index. Used to detect burned areas. 
        Values range from -1 to 1. It uses the short-wave infrared and near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlGn'.
        """
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
 
    def evi2(self, plot = True, colormap = 'RdYlGn'):
        """EVI2 stands for Enhanced Vegetation Index 2. It is simplified version of the original EVI. 
        Similar to NDVI, it is also used to monitor vegetation, the higher the value, the healthier the vegetation.
        As it is not a normalized index, values range is wider than -1 to 1. It is hard to pin point exact 
        range. It uses the red and near-infrared spectral bands.

        Args:
            plot (bool, optional): Enables plotting an image of calculated index. Defaults to True.
            colormap (str, optional): A color scheme. Defaults to 'RdYlGn'.
        """
        self.plot = plot
        self.cmap = colormap
        outfile = r'evi2.tif'

        with rasterio.open(self.b9, driver='JP2OpenJPEG') as nir:
            NIR = nir.read()
        with rasterio.open(self.b5, driver='JP2OpenJPEG') as red:
            RED = red.read()


        evi = 2.4 * ((NIR.astype(float) - RED.astype(float)) / (NIR.astype(float) + RED.astype(float) + 1))
        
        print('\nMin EVI2: {m}'.format(m=np.nanmin(evi)))
        print('Max EVI2: {m}'.format(m=np.nanmax(evi)))
        print('Mean EVI2: {m}'.format(m=np.nanmean(evi)))
        print('Median EVI2: {m}'.format(m=np.nanmedian(evi)))

        if self.plot == True:
            plt.imshow(np.squeeze(evi), cmap=self.cmap)
            plt.title('EVI2')
            plt.colorbar()
            plt.show()
        else:
            pass

        profile = nir.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open(outfile, 'w', **profile) as dst:
            dst.write(evi.astype(rasterio.float32))