from mriqa import messages
from mriqa import config
from mriqa.env import parse_console
import subprocess
import pprint
import json 
from os.path import basename as bn
from mriqa.utils import import_mongo
def main():
    from mriqa.utils import reviewer, kill_process

    parse_console()

    # Make sure loggers are started
    config.loggers.init()

    config.to_filename(config.session.config_file)
    config.load(config.session.config_file)

    viewer = config.session.viewer
    output_dir = config.session.output_dir
    files = config.session.inputs
    review_id = config.session.review_id
    
    start_message = messages.START.format(
        bids_dir=config.session.bids_dir,
        output_dir=output_dir,
        viewer=viewer,
        review_id=review_id)

    for k,v in messages.SEARCH_BIDS.items():
        if config.session.__dict__[v] is not None:
            start_message += (f'       * {k}: {config.session.__dict__[v]}\n')
            

    config.loggers.cli.log(30, msg = start_message)
    
    """Instantiate either dict object or mongodb database to store ratings"""
    config.collector.func_finder()      
    db = reviewer()



    try: 
        for file in files:                        
            if not db.check(img = bn(file)):
              continue

            subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            db.review(img = bn(file))
                    
            kill_process(viewer)        
    except KeyboardInterrupt:
        pass 
    
    config.loggers.cli.log(30, messages.END)

    if not config.session.mongodb:
        with open(db.filename, "w") as f:
            json.dump(db.db, f, indent = 4)

    else:
        import_mongo(db.db, output_dir, db.filename)
        #for doc in db.db.find():    
        #    pprint.pprint(doc)

if __name__ == "__main__":
    main()

