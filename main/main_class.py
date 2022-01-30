from parse import *
from pathlib import Path
import os
from zipfile import ZipFile


class sentinel:
    def __init__(self, my_path:str):
        self.my_path = my_path 
        self.change_path(my_path)

    def change_path(self, my_path:str) -> None:
        if self._check_path(my_path):
            os.chdir(my_path)

    def _check_path(self, my_path, dir_to_search='GRANULE') -> bool: 
        if my_path[-3:] == 'zip':
        # opening the zip file in READ mode
            with ZipFile(os.path.basename(my_path), 'r') as zip:
            # printing all the contents of the zip file
                zip.printdir()
                zip.extractall()
        else:        
            inp_path =  Path(self.my_path)
            return any(
            file.is_dir() and file.name == dir_to_search and len(os.listdir(os.path.join(self.my_path, dir_to_search))) != 0
            for file in inp_path.glob('**/*'))

    def naming_convention(self) -> dict:
        lastElement = os.path.basename(os.path.normpath(self.my_path))
        values = lastElement.split('_')
        keys = ['Mission ID', 'Product level', 'Datatake sensing time (YYYYMMDDHHMMSS)',
                'PDGS Processing Baseline number', 'Relative Orbit number', 'Tile Number and format', 
                'Product Discriminator']
        namingDict = dict(zip(keys, values))
        print(namingDict)

    def get_data(self):
        if self._check_path(self.my_path):
            for root, dirs, files in os.walk(self.my_path):
                for file in files:
                    if(file.endswith(".jp2")):
                        print(os.path.join(root,file))


#NIE DZIAŁA
sentinel('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE').naming_convention()
sentinel('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE').get_data()
sentinel('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE')._check_path()
