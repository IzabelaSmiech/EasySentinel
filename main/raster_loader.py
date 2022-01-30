import glob

from datetime import datetime
from bandlength import band_lenght_dict
from config import datafolder_path, band_path

b4 = glob.glob(band_path + '**B04_20m.jp2')
b8 = glob.glob(band_path + '**B8A_20m.jp2')
b2 = glob.glob(band_path + '**B02_20m.jp2')
b3 = glob.glob(band_path + '**B03_20m.jp2')
