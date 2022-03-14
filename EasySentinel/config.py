import os

datafolder_path = '' # please put here the path to the SAFE folder

for dirname, subdir, filename in os.walk(datafolder_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(datafolder_path, 'GRANULE'))) != 0: #does folder GRANULE exists and is it empty
        band_path = os.listdir(os.path.join(datafolder_path, 'GRANULE'))
        band_path = band_path[0]
        break # to prevent checking more paths

band_path = datafolder_path + '/GRANULE/' + band_path + '/IMG_DATA/R60m/'
band_name = '' #please put here chosen band (file_name) - only for band_info function!
