import hashlib
import os
import sys
import time
from rest_framework.utils import json

start=time.time()
def md5sum(filename):   #MD5 HASHFUNCTION
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def writeToJSONFile(path, filename, data):  #FUNCTION FOR WRITE DATA INTO JSON
    filePathNameExt='./'+path+'/'+filename+'.json'
    with open(filePathNameExt,'w') as fp:
        json.dump(data, fp)

fileDict = {}
Current_file_Count=0
Current_folder_Count=0
rootdir = sys.argv[1]
#print(sys.argv)
for root, subFolders, files in os.walk(rootdir):
    Current_file_Count+=len(files)
    Current_folder_Count+=len(subFolders)
if os.stat("last_file_count.txt").st_size == 0:
    with open('last_file_count.txt', 'w') as the_file:
        the_file.write(repr(Current_file_Count)+","+repr(Current_folder_Count))
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
else:
    with open('last_file_count.txt', 'r') as the_file:
        c=the_file.read()
        int_lst = [int(x) for x in c.split(",")]
        Last_folder_Count=int_lst[1]
        Last_file_Count=int_lst[0]
        # print(Last_file_Count)
        # print(Last_folder_Count)
    if Last_folder_Count==Current_folder_Count and Last_file_Count==Current_file_Count:
        exit()
    else:
        with open('last_file_count.txt', 'w') as the_file:
            the_file.write(repr(Current_file_Count) + "," + repr(Current_folder_Count))
        with open('last_data_json.json') as json_data:
            d = json.load(json_data)
        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                fileDict[os.path.join(root,file)]=md5sum(os.path.join(root,file))
        print(set(d)^set(fileDict))

path='./'
fileName='last_data_json'
writeToJSONFile(path,fileName,fileDict)
end=time.time()
print(end - start)