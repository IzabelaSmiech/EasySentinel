import os
from datetime import datetime
from pathlib import Path

#pathlib module - searching if folder granule exists and if it is empty or not
inp_path =  Path('data\\S2A_MSIL2A_20200804T110631_N0214_R137_T29SQC_20200804T122403.SAFE') 

def check_dir(inp_path, dir_to_search='GRANULE'):
    return any(
        file.is_dir() and file.name == dir_to_search and len(os.listdir(os.path.join(inp_path, dir_to_search))) != 0
        for file in inp_path.glob('**/*') #Return a possibly-empty list of path names that match pathname
    )

#another possibility:
for dirname, subdir, filename in os.walk(inp_path):
    if 'GRANULE' in subdir and len(os.listdir(os.path.join(inp_path, 'GRANULE'))) != 0:
        print("yes")
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