import os
from pymongo import MongoClient
import pprint
from configparser import ConfigParser
from datetime import datetime
import re 
import MRIQA_modules as markerFunc
import getpass
import subprocess
from dotenv import load_dotenv                          

import getpass

load_dotenv('settings.env')                                 #load .env file with mongodb credentials

#connect to mongodb docker container 
client = MongoClient(host="localhost", port=27017, username=os.getenv('MONGO_DB_USRNAME'), password=os.getenv('MONGO_DB_PW'))

db = client["image_ratings"]
#db.ratings.drop()
#collection = db.ratings


config_file = "MRIQA_config.ini"                           #config file with file paths and review parameters 
config = ConfigParser()
config.read(config_file)

user = getpass.getuser()                                    #user id 
time_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")     #date for output files

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#How to reinstate artifact review 
#line 74: f"Review artifacts: {config['settings']['artifacts']}\n"+
#objects line 77: artifacts = 'True' if input("Rate severity of artifacts for each scan? (Motion, susceptibility, flow/ghosting)\n\nSelection (y/n): ") == 'y' else 'False'
#objects line 82: config['settings']['artifacts'] = str(artifacts)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#TROUBLESHOOTING
for i in db.list_collection_names():
    print(i)
    #db.drop_collection(i)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#BEGIN SESSION & SET SEARCH PARAMETERS--------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('\033c')
print("\n1 - New session \n2 - Resume previous sessions: continue reviewing files\n")
new_sesh = True if input("Selection: ") == '1' else False                #resume session or begin a new session
print("\033c")


update_parameters = True                                                 # if true prompt user to create review params  
if new_sesh:                                                             #check if new session to be started 
    sesh_str = f'MR_rating_record_{time_str}'                           
    collection = db[sesh_str]                                            #instantiate new mongoDB collection
else:                                                                    #check if previous session to be reviewed
    while True: 
        try:
            collection_list = []
            for collec in db.list_collection_names():
                if re.match('MR_rating.*', collec):
                    collection_list.append(collec)

            if len(collection_list) == 0:
                input('No sessions to resume. Enter to quit')
                quit()
            
            for count, item in enumerate(collection_list):
                print(str(count +1) +". " + item)
            
            index = int(input("Enter session number to resume: ")) -1
            print("\033c")
            if not index in range(0, len(collection_list)): 
                raise ValueError
            
            server = collection_list[index]
            collection = db[server]                                     #connect to previous mongoDB collection 
            break
        
        except ValueError:
            print("\033c")
            print("\nInvalid session, try again:\n")
        #
    print(f"Previous session parameters:\n\n" +
            f"Folder(s) or File(s): {config['settings']['input_params']}\n"+
            #f"Review artifacts: {config['settings']['artifacts']}\n"+
            f"Scan viewer: {config['settings']['viewer']}")

    update_parameters = True if input("\nUpdate (y) else Enter: ") == 'y' else False
    print("\033c")


if update_parameters:
    markerFunc.configupdate()                                          #update config file

subject = markerFunc.review_subject()                                  #review all files or single subject 


    
config.read(config_file)                                               #import values from config file
string          = config['settings']['re_params']
input_params    = str(config['settings']['input_params'])
artifacts       = config['settings']['artifacts']
viewer          = config['settings']['viewer']
rootdir         = config['settings']['input_images'] 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PARSE FILES AND REVIEW--------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
filesearch = re.compile(string)                                     #regex expression 
user = "oscar"                                                     #test user

try:
    for root, dirs, files in os.walk(rootdir):                        
        for file in files: 
            if subject:
                if re.compile(f'.*{subject}.*').match(root): pass
                else: continue
            if input_params == 'anat folder':          
                if re.compile('.*anat$').match(root): pass          #check if root dir contains anat folder
                else: continue
            if filesearch.match(file):
                #print('\033c')
                fileview = subprocess.Popen([viewer, root +'/'+file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                markerFunc.update_rating(user, file, collection, viewer)
                if eval(artifacts): #eval(): compiles config string to bytecode and evaluates as py expression (boolean)
                    markerFunc.review_artifacts(user, file, collection) 
                markerFunc.kill_process(viewer)
    print('\033c')
    print("All files matching criteria reviewed")

except KeyboardInterrupt:
    print('\033c')
    pass 

print('\n\n+----------------------------+\n\nSession Ended\n\n+----------------------------+')

for doc in collection.find():
    pprint.pprint(doc)
