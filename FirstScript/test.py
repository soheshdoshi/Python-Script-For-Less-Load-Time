import os
import sys
from firstscript import md5sum,writeToJSONFile

fileList = {}
rootdir = sys.argv[1]
for root, subFolders, files in os.walk(rootdir):
    for file in files:
        fileList[md5sum(os.path.join(root,file))]=os.path.join(root,file)
print (fileList)
path='./'
fileName='test_json'
writeToJSONFile(path,fileName,fileList)