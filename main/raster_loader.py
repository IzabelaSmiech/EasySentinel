import os

from dict_band_length import band_lenght_dict
from config import datafolder_path, band_path

list_of_keys = []
for root, dirs, files in os.walk(datafolder_path):
	for file in files:
		if (file.endswith("60m.jp2")):
			list_of_keys.append(file[-11:-8])

list_of_values = []
#.jp2 files in directory:
for root, dirs, files in os.walk(datafolder_path):
	for file in files:
		if (file.endswith("60m.jp2")):
			list_of_values.append(file)

band_dict = dict(zip(list_of_keys, list_of_values))

aot = band_path + band_dict["AOT"]
b1 = band_path + band_dict["B01"]
b2 = band_path + band_dict["B02"]
b3 = band_path + band_dict["B03"]
b4 = band_path + band_dict["B04"]
b5 = band_path + band_dict["B05"]
b6 = band_path + band_dict["B06"]
b7 = band_path + band_dict["B07"]
b9 = band_path + band_dict["B09"]
b11 = band_path + band_dict["B11"]
b12 = band_path + band_dict["B12"]
b8 = band_path + band_dict["B8A"]
scl = band_path + band_dict["SCL"]
tci = band_path + band_dict["TCI"]
wvp = band_path + band_dict["WVP"]