import hashlib
import os
import sys
import json
import time
"""
How to run this python script:-
Example:
    $ python first_script.py C:/Desktop/Folder1
    """
def md5sum(filename):
    """

    Parameters
    ----------
    filename:str

    Returns
    -------
        md5.hexdigest() is returned string containing only hexadecimal digits.
    """
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

#FUNCTION FOR WRITE DATA INTO JSONFile By Default Path is Current Path & Filename:- last_data_json.json.

def writeToJSONFile(path, filename, data):
    """

    Parameters
    ----------
    path:str
        Examples:
                ./ for current path
    filename:str
        Examples:
                last_data_json.json
    data:dict
    Returns
    -------
        No Returns Only write JsonData in file

    """
    filePathNameExt='./'+path+'/'+filename
    with open(filePathNameExt,'w') as fp:
        json.dump(data, fp)

#Function For Check Json File is Exists or Not if File is Not Present It Create Automatically.

def checkJsonFile(path, filename):
    """

    Parameters
    ----------
    path:str
        Examples:
            ./ for current path
    filename:str
         Examples:
                last_data_json.json
    Returns
    -------
        Only Checks FileExists If Not then Create It.

    """
    filePathNameExt='./'+path+'/'+filename
    if os.path.isfile(filePathNameExt):
        pass
    else:
        with open(filePathNameExt,'w') as fp:
            fp.close()


#If command line argument is Not 2 raise error

if len(sys.argv) == 2:
    def file_Changes():
        """
        Returns
        -------
        data:dict
            if any changes in file function return that data in dict
        Examples:
            {'created': [], 'deleted': [], 'rename': []}
        """
        fileDict = {}
        rootdir = sys.argv[1]
        path='./'
        fileName='last_data_json'
        suffix='.json'
        data={}
        checkJsonFile(path,fileName+suffix)
        if os.stat(os.path.join(path,fileName+suffix)).st_size == 0:
            for root, subFolders, files in os.walk(rootdir):
                for file in files:
                    fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
            writeToJSONFile(path, fileName+suffix, fileDict)
        else:
            file_Change_list=[]
            with open(os.path.join(path,fileName+suffix)) as json_data:
                last_json_dict = json.load(json_data)
            for root, subFolders, files in os.walk(rootdir):
                for file in files:
                    fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
            data['created']=list(set(fileDict)-set(last_json_dict))
            data['deleted']=list(set(last_json_dict)-set(fileDict))
            inv_map_fileDict = {v: k for k, v in fileDict.items()}
            inv_map_json = {v: k for k, v in last_json_dict.items()}
            #result = set(inv_map_fileDict) - set(inv_map_json)
            for i in set(inv_map_fileDict) - set(inv_map_json):
                file_Change_list.append(inv_map_fileDict[i])
            data['file_changes'] = file_Change_list
            writeToJSONFile(path,fileName+suffix, fileDict)
            return data

else:
    print('''Please Enter Valid Path Like
    'Ex. python abc.py C:/Document/Desktop' ''')
st=time.time()
print(file_Changes())
et=time.time()
print(et-st)