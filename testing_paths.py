import os
import json


filename = "12345.json"

# Get absolute path of current working directory
abs_path = os.path.abspath(os.path.curdir)
# Get absolute path for the designated file
abs_filepath = abs_path + os.path.sep + filename

if os.path.exists(abs_filepath):
    with open(abs_filepath) as f_obj:
        print(os.fstat(f_obj.fileno()))
else:
    with open(abs_filepath, 'w+') as f_obj:
        json.dump("MUAHAHAHAHAHA", f_obj)
