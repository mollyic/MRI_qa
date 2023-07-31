import os
import json
from configparser import ConfigParser
from datetime import datetime
import pprint
import re 
import modules.MRIqa_config as configger
import modules.MRIqa_review as reviewer
import getpass
import subprocess
import getpass



config_file = "MRIQA_config.ini"                         
config = ConfigParser()
config.read(config_file)
local   = config['settings']['local'] 

user = getpass.getuser()                                    #user id 
time_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")     #date for output files

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#BEGIN SESSION & SET SEARCH PARAMETERS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('\033c')
print("\n1 - New session \n2 - Resume previous sessions: continue reviewing files\n")
new_sesh = True if input("Selection: ") == '1' else False                #resume session or begin a new session
print("\033c")

db = reviewer.collector(local = local, new = new_sesh, sesh_str=config['settings']['seshid'], results_dir =config['settings']['output'])


print(f"Previous session parameters:\n\n" +
        f"Folder(s) or File(s): {config['settings']['input_params']}\n"+
        #f"Review artifacts: {config['settings']['artifacts']}\n"+
        f"Scan viewer: {config['settings']['viewer']}")

#update config file
update_parameters = True if input("\nUpdate (y) else Enter: ") == 'y' else False
print("\033c")
if update_parameters:
    configger.configupdate()                                          #update config file

subject = reviewer.review_subject()                                  #review all files or single subject 

    
config.read(config_file)                                               #import values from config file
string          = re.compile(config['settings']['re_params'])
input_params    = str(config['settings']['input_params'])
artifacts       = config['settings']['artifacts']
viewer          = config['settings']['viewer']
rootdir         = config['settings']['input_images'] 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PARSE FILES AND REVIEW
try:
    for root, dirs, files in os.walk(rootdir):                        
        for file in files: 
            if subject:
                if not re.compile(f'.*{subject}.*').match(root):  
                    continue
            if input_params == 'anat folder':          
                if not re.compile('.*anat$').match(root): 
                    continue
            if re.match(string, file):
                #print('\033c')
                fileview = subprocess.Popen([viewer, root +'/'+file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                db.review_image(user, file, viewer)
                
                if artifacts: 
                    reviewer.review_artifacts(user, file, db) 
                
                reviewer.kill_process(viewer)
    
    #print('\033c')
    print("All files matching criteria reviewed")

except KeyboardInterrupt:
    #print('\033c')
    pass 

print('\n\n+----------------------------+\n\nSession Ended\n\n+----------------------------+')

# for doc in db.find():
#     pprint.pprint(doc)

if local:
    print('\n\n.json file generated\n\n')
    with open(db.filename, "w") as f:
        json.dump(db.collection, f, indent = 4)

else:
    for doc in db.find():
        pprint.pprint(doc)

# #field name information 
# field_info = ['filepath', 'user', 'rating', 'date', 'susceptibility', 'motion', 'flow']
# # create the csv writer object
# csv_name = json_filename.replace('.json', '.csv')
# with open(csv_name, "w") as f:
#     w = csv.DictWriter(f, field_info)
#     w.writeheader()
#     for k in resultsdic:
#         w.writerow({field: (resultsdic[k].get(field) if field in resultsdic[k].keys() else k) for field in field_info})


