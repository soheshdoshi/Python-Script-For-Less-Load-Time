import hashlib
import sys
import os
import json
import time

start=time.time()
def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

cmd_args=sys.argv[1:]
#print(cmd_args)
file_dict={}
for i in os.listdir(cmd_args[0]):
    if os.path.isfile(os.path.join(cmd_args[0],i)):
        file_dict[md5sum(os.path.join(cmd_args[0],i))]=i
    elif os.path.isdir(os.path.join(cmd_args[0],i)):
        #print("d-",i)
        for j in os.listdir(os.path.join(cmd_args[0],i)):
            if os.path.isfile(os.path.join(cmd_args[0],i,j)):
                file_dict[md5sum(os.path.join(cmd_args[0],i,j))]=j

dumps_json=json.dumps(file_dict)
json_obj=json.loads(dumps_json)
print(json_obj)
end=time.time()
print(end -start)

