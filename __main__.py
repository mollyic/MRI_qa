from mriqa import messages
from mriqa import config
import re
from mriqa.environ import parse_console
import os 
import subprocess
import pprint
import json 
from mriqa.review import reviewer
import logging

def main():
    from mriqa.review import kill_process
    
    parse_console()

    # Make sure loggers are started
    config.loggers.init()

    config.to_filename(config.session.config_file)
    config.load(config.session.config_file)

    start_message = messages.START.format(
        bids_dir=config.session.bids_dir,
        output_dir=config.session.output_dir,
        viewer=config.session.viewer,
        review_id=config.session.review_id,)

    for k,v in messages.SEARCH_BIDS.items():
        if config.session.__dict__[v] is not None:
            start_message += (f'       * {k}: {config.session.__dict__[v]}\n')
            

    config.loggers.cli.log(30, msg = start_message)
    """
    Instantiate either dict object or mongodb database to store ratings
    """
    config.collector.func_finder()      #assign appropriate functions to class
    db = reviewer()

    """
    PARSE FILES AND REVIEW
    """
    viewer = config.session.viewer
    user = config.session.user
    
    files = db.check()

    try: 
        if files:
            for file in files:                        
                #subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                db.review(img = file)
                        
                if config.session.artifacts: 
                    db.review_artifacts(user, file, db) 
                        
                kill_process(viewer)        
    except KeyboardInterrupt:
        pass 
    
    print(messages.END)

    if not config.session.mongodb:
        print('\n\n.json file generated\n\n')
        with open(str(db.filename), "w") as f:
            json.dump(db.db, f, indent = 4)

    else:
        for doc in db.find():
            pprint.pprint(doc)

if __name__ == "__main__":
    main()

