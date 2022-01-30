import os
from datetime import datetime
import pandas as pd

class dataInfo():
    def __pretty(self,d, indent=0):
        for key, value in d.items():
            print('*' + '\t' * indent + str(key) + ":")
            if isinstance(value, dict):
                self.__pretty(value, indent+1)
                print('\t' * indent)
            else:
                print('\t' * (indent+1) + str(value))
                print('\t' * indent)
                print('\t' * indent + '---------')

    def data_info(self, my_path:str):
        print('Datapath information:')
        filename = os.path.basename(my_path)
        date = filename[-54:-46]
        time = filename[-45:-39]
        fulldate = datetime.strptime(date + time, '%Y%m%d%H%M%S')
        date2 = filename[-20:-12]
        time2 = filename[-11:-5]
        fulldate2 = datetime.strptime(date2 + time2, '%Y%m%d%H%M%S')
        lastElement = os.path.basename(os.path.normpath(my_path))
        values = lastElement.split('_')
        keys = ['Mission ID', 'Product level', 'Datatake sensing time',
                    'PDGS Processing Baseline number', 'Relative Orbit number', 'Tile Number and format', 
                    'Product Discriminator']
        
        namingDict = dict(zip(keys, values))
        namingDict['Datatake sensing time'] = fulldate
        #namingDict["Product Discriminator"] = namingDict["Product Discriminator"].split('.')[0]
        namingDict['Product Discriminator'] = fulldate2
        self.__pretty(namingDict)

a = dataInfo()
a.data_info('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE')