import os
from datetime import datetime
from pathlib import Path

inp_path =  Path('C:/Users/izka1/OneDrive/Pulpit/geoinformacja/praca_inzynierska/data/S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE') 

list_of_keys = []
for root, dirs, files in os.walk(inp_path):
	for file in files:
		if (file.endswith("20m.jp2")):
			list_of_keys.append(file[-11:-8])

list_of_values = []
#.jp2 files in directory:
for root, dirs, files in os.walk(inp_path):
	for file in files:
		if (file.endswith("20m.jp2")):
			list_of_values.append(file)


band_dict = dict(zip(list_of_keys, list_of_values))
print(band_dict)
