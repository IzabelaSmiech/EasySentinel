import os
from datetime import datetime
import pandas as pd

def data_info(my_path:str):
    filename = os.path.basename(my_path)
    date = filename[-54:-46]
    time = filename[-45:-39]
    fulldate = datetime.strptime(date + time, '%Y%m%d%H%M%S')
    print(fulldate)
    lastElement = os.path.basename(os.path.normpath(my_path))
    values = lastElement.split('_')
    keys = ['Mission ID', 'Product level', 'Datatake sensing time',
                'PDGS Processing Baseline number', 'Relative Orbit number', 'Tile Number and format', 
                'Product Discriminator']
    
    namingDict = dict(zip(keys, values))
    namingDict['Datatake sensing time'] 
    print(namingDict)

data_info('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE')