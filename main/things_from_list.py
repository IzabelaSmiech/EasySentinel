import os
from datetime import datetime
from pathlib import Path
from pickle import FALSE, TRUE


#pathlib module - searching if folder granule exists and if it is empty or not
inp_path =  Path('C:/Users/izka1/OneDrive/Pulpit/geoinformacja/praca_inzynierska/data/S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE') 

def check_dir(inp_path, dir_to_search='GRANULE'):
    return any(
        file.is_dir() and file.name == dir_to_search and len(os.listdir(os.path.join(inp_path, dir_to_search))) != 0
        for file in inp_path.glob('**/*') #Return a possibly-empty list of path names that match pathname
    )

last = os.path.basename(os.path.normpath(inp_path))
print(len(str(last)))

if len(str(last)) == 65 and last.endswith('.SAFE') == True:
    print('zgadza sie mordeczko')
else:
    print('nie zgadza sie mordeczko')

#another possibility:
for dirname, subdir, filename in os.walk(inp_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(inp_path, 'GRANULE'))) != 0:
        print(os.listdir(os.path.join(inp_path, 'GRANULE')))
        break # to prevent checking more paths
else:
    print("no")

#everything in directory:
with os.scandir(inp_path) as entries:
    for entry in entries:
        print(entry.name)


myDict = {}
#.jp2 files in directory:
for root, dirs, files in os.walk(inp_path):
	for file in files:
		if (file.endswith(".jp2") & file.startswith("MSK")):
			myDict["mask"] = file
    

print(myDict)

#get date and time
def date_time(path) -> str:
    filename = os.path.basename(path)
    date = filename[-54:-46]
    time = filename[-45:-39]
    fulldate = datetime.strptime(date + time, '%Y%m%d%H%M%S')
    print(fulldate)
    return fulldate

date_time(inp_path)