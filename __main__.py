from mriqa import messages
from mriqa import config
from mriqa.env import parse_console
import subprocess
import pprint
import json 
from os.path import basename as bn

def main():
    from mriqa.utils import reviewer, kill_process

    parse_console()

    print(config.session.mongodb)
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
    
    """Instantiate either dict object or mongodb database to store ratings"""
    config.collector.func_finder()      
    db = reviewer()

    viewer = config.session.viewer
    user = config.session.user
    files = config.session.inputs

    try: 
        for file in files:                        
            if not db.check(img = bn(file)):
              continue
            """Check for previously reviewed files
                move check inside: create list of files not reviewed and present at the end 
                Check each file as it comes through 
            """
            subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            db.review(img = bn(file))
                    
            if config.session.artifacts: 
                db.review_artifacts(user, file, db) 
                    
            kill_process(viewer)        
    except KeyboardInterrupt:
        pass 
    
    config.loggers.cli.log(30, messages.END)

    if not config.session.mongodb:
        with open(str(db.filename), "w") as f:
            json.dump(db.db, f, indent = 4)

    else:
        for doc in db.db.find():
            pprint.pprint(doc)

if __name__ == "__main__":
    main()

