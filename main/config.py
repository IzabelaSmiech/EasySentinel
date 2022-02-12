import os

datafolder_path = 'C:/Users/izka1/OneDrive/Pulpit/WODACHECK/fire/S2A_MSIL2A_20210828T031541_N0301_R118_T51VWJ_20210828T061932.SAFE'

for dirname, subdir, filename in os.walk(datafolder_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(datafolder_path, 'GRANULE'))) != 0:
        band_path = os.listdir(os.path.join(datafolder_path, 'GRANULE'))
        band_path = band_path[0]
        break # to prevent checking more paths

band_path = datafolder_path + '/GRANULE/' + band_path + '/IMG_DATA/R60m/'
band_name = 'T29SQC_20200804T110631_B02_20m.jp2'