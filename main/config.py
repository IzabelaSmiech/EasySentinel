import os

datafolder_path = 'C:/Users/izka1/OneDrive/Pulpit/WODACHECK/S2A_MSIL2A_20211010T100941_N0301_R022_T33UXA_20211010T115015.SAFE'

for dirname, subdir, filename in os.walk(datafolder_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(datafolder_path, 'GRANULE'))) != 0:
        band_path = os.listdir(os.path.join(datafolder_path, 'GRANULE'))
        band_path = band_path[0]
        break # to prevent checking more paths

band_path = datafolder_path + '/GRANULE/' + band_path + '/IMG_DATA/R60m/'
band_name = 'T33UXA_20211010T100941_B01_60m.jp2'