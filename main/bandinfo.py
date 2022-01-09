import rasterio
import os 

def band_info(Path:str, band:str):
    my_band = rasterio.open(os.path.join(Path, band), driver='JP2OpenJPEG')
    print("Number of raster columns:", my_band.width)
    print("number of raster rows:", my_band.height)
    print(my_band.crs)
    print("Bounding box:", my_band.bounds)

band_info('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE\\GRANULE\\L2A_T29SQC_A026732_20200804T111447\\IMG_DATA\\R10m', 'T29SQC_20200804T110631_B02_10m.jp2')