import hashlib
import os
import sys
import json
import time
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

def checkJsonFile(path,filename):
    filePathNameExt='./'+path+'/'+filename+'.json'
    if os.path.isfile(filePathNameExt):
        pass
    else:
        with open(filePathNameExt,'w') as fp:
            fp.close()

if len(sys.argv) == 2:
    def file_Changes():
        fileDict = {}
        rootdir = sys.argv[1]
        path='./'
        fileName='last_data_json'
        data={}
        checkJsonFile(path,fileName)
        if os.stat("last_data_json.json").st_size == 0:
            for root, subFolders, files in os.walk(rootdir):
                for file in files:
                    fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
            writeToJSONFile(path, fileName, fileDict)
        else:
            with open('last_data_json.json') as json_data:
                last_json = json.load(json_data)
            for root, subFolders, files in os.walk(rootdir):
                for file in files:
                    fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
            data['created']=list(set(fileDict)-set(last_json))
            data['deleted']=list(set(last_json)-set(fileDict))
            writeToJSONFile(path,fileName,fileDict)
            return data

else:
    print('''Please Enter Valid Path Like 
    'Ex. python abc.py C:/Document/Desktop' ''')
st=time.time()
print(file_Changes())
et=time.time()
print(et-st)