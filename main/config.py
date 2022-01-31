import os

datafolder_path = 'dat/S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE'

for dirname, subdir, filename in os.walk(datafolder_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(datafolder_path, 'GRANULE'))) != 0:
        band_path = os.listdir(os.path.join(datafolder_path, 'GRANULE'))
        band_path = band_path[0]
        break # to prevent checking more paths

band_path = datafolder_path + '/GRANULE/' + band_path + '/IMG_DATA/R20m/'
band_name = 'T29SQC_20200804T110631_B02_20m.jp2'