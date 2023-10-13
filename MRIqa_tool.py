from messages import MSGS
from review import collector, review_subject, review_artifacts, kill_process
from environ import configupdate
import config
import re
from environ import parse_console, parse_usrenv
import os 
import subprocess
import pprint
import json 

def main():
    
    """
    Get arguments from user.ini file and terminal arguments
    """
    parse_console()
    parse_usrenv()
    """
    Confirm the user if happy with these settings 
    """
    print(MSGS['session'])
    new_sesh = True if input("Selection: ") == '1' else False               
    print("\033c")

    """
    Instantiate either dict object or mongodb database to store ratings
    """
    db = collector(new = new_sesh)


    """
    Option to update config file settings
    """
    print(f"Previous session parameters:\n\n" +
        f"File or folder search parameter:      {config.preferences.input_params}\n"+
        f"Input directory:                      {config.preferences.input_images}\n"+
        f"Review session ID:                    {config.preferences.seshid}\n"+
        f"Scan viewer:                          {config.preferences.viewer}")
    update_parameters = True if input("\nUpdate (y) else Enter: ") == 'y' else False
    print("\033c")
    if update_parameters:
        configupdate() 
        parse_usrenv()
    
    subject = review_subject()                                  #review all files or single subject 



    """
    PARSE FILES AND REVIEW
    """
    string          = re.compile(config.preferences.re_params)
    input_params    = config.preferences.input_params
    artifacts       = config.preferences.artifacts
    viewer          = config.preferences.viewer
    rootdir         = config.preferences.input_images
    user            = config.session.user
    artifacts       = config.preferences.artifacts

    try:
        for root, dirs, files in os.walk(rootdir):                        
            for file in files: 
                if subject:
                    if not re.compile(f'.*{subject}.*').match(root):  
                        continue
                if 'anat folder' in input_params:          
                    if not re.compile('.*anat$').match(root): 
                        continue
                if re.match(string, file):
                    fileview = subprocess.Popen([viewer, root +'/'+file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                    db.review_image(user, file, viewer)
                    
                    if artifacts: 
                        review_artifacts(user, file, db) 
                    
                    kill_process(viewer)
        
    except KeyboardInterrupt:
        pass 

    print(MSGS['end'])

    if not config.preferences.mongodb:
        print('\n\n.json file generated\n\n')
        with open(str(db.filename), "w") as f:
            json.dump(db.collection, f, indent = 4)

    else:
        for doc in db.find():
            pprint.pprint(doc)

main()