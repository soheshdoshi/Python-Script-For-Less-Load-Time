import hashlib
import os
import sys
import json
import logging

def md5sum(filename):
    """

    Parameters
    ----------
    filename:str

    Returns
    -------
        md5.hexdigest() is returned string containing only hexadecimal digits.
    """
    logging.info('Enter into md5sum.')
    md5 = hashlib.md5()
    logging.info('MD5 Object Create.')
    with open(filename, 'rb') as f:
        logging.info('Open File %s',filename)
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
        logging.info('Generating Hash.')
        logging.info('Exit Md5.')
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
    logging.info('Enter into writeToJson.')
    filePathNameExt='./'+path+'/'+filename
    logging.info('filePathNameExt %s',filePathNameExt)
    with open(filePathNameExt,'w') as fp:
        json.dump(data, fp)
    logging.info('writeToJson Exit.')


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
    logging.info('Enter into checkJsonFile.')
    filePathNameExt='./'+path+'/'+filename
    if os.path.isfile(filePathNameExt):
        logging.info('Pass.')
        pass
    else:
        with open(filePathNameExt,'w') as fp:
            logging.info('%s File Created',filePathNameExt)
            fp.close()
    logging.info('checkJson Complete.')

def file_Changes(argv_one):
    """
    Returns
    -------
    data:dict
        if any changes in file function return that data in dict
    Examples:
        {'created': [C:\\Users\\xyz.txt], 'deleted': [C:\\Users\\abc.txt], 'rename': [C:\\Users\\ex.txt]}
    """
    logging.info('Enter Into file_Changes.')
    logging.info('%s [folder path]:-',argv_one)
    fileDict = {}
    rootdir = argv_one
    path='./'
    fileName='last_data_json'
    suffix='.json'
    data={}
    checkJsonFile(path,fileName+suffix)
    if os.stat(os.path.join(path,fileName+suffix)).st_size == 0:
        logging.info('Filesize 0 Found.')
        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
        writeToJSONFile(path, fileName+suffix, fileDict)
    else:
        file_Change_list=[]
        logging.info('file_Change_List Generate.')
        with open(os.path.join(path,fileName+suffix)) as json_data:
            last_json_dict = json.load(json_data)
            logging.info('last_json_dict created.')
        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                fileDict[os.path.join(root, file)] = md5sum(os.path.join(root, file))
        data['created']=list(set(fileDict)-set(last_json_dict))
        logging.info('File Created Found.')
        data['deleted']=list(set(last_json_dict)-set(fileDict))
        logging.info('File Deleted Found.')
        inv_map_fileDict = {v: k for k, v in fileDict.items()}
        logging.info('Inverse fileDict.')
        inv_map_json = {v: k for k, v in last_json_dict.items()}
        logging.info('Inverse JsonDict.')
        #result = set(inv_map_fileDict) - set(inv_map_json)
        for i in set(inv_map_fileDict) - set(inv_map_json):
            file_Change_list.append(inv_map_fileDict[i])
        data['file_changes'] = file_Change_list
        logging.info('File_changes Detected.')
        writeToJSONFile(path,fileName+suffix, fileDict)
        return json.dumps(data)




if len(sys.argv) == 2:
    argv_one=sys.argv[1]
    file_Changes(argv_one)
elif len(sys.argv) == 3 and sys.argv[2]=='-d':
    argv_one=sys.argv[1]
    logging.basicConfig(filename='exmple.log',filemode='w',level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M')
    logging.info('Start')
    file_Changes(argv_one)
    logging.info('End')
else:
    print('''USAGE
    'Ex. python script.py [Folder_Name]' or
    Show Details Of Each Steps 
    'python script.py [Folder_Name] -d' ''')
