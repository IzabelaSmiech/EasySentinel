import os
from datetime import datetime
from pathlib import Path

inp_path =  Path('C:/Users/izka1/OneDrive/Pulpit/geoinformacja/praca_inzynierska/data/S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE') 

#wzięcie nazwy folderu, ostatni element ścieżki
last = os.path.basename(os.path.normpath(inp_path))

#sprawdzenie czy zawiera końcówkę safe i 65 znaków
if len(str(last)) == 65 and last.endswith('.SAFE') == True:
    print('correct')
else:
    print('incorrect')

#wyprintowanie nazwy tego folderu między granule a imgdata (jako lista)
for dirname, subdir, filename in os.walk(inp_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(inp_path, 'GRANULE'))) != 0:
        print(os.listdir(os.path.join(inp_path, 'GRANULE')))
        break # to prevent checking more paths
    