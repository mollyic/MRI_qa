import signal
from mriqa import config
from mriqa import messages as mg

import os
import sys

def verify_input(sessions = None, n = 5, msg=None, score= None):

    msg = msg if not sessions else sessions
    score = score if not sessions else ''
    error = mg.RATE_ERR if not sessions else mg.SES_ERR
    choice = mg.PICK_SCORE if not sessions else mg.PICK_SES

    while True:
        config.loggers.cli.log(30,  msg)
        config.loggers.cli.log(30,  score)

        answer = input(choice)
        if answer.isdigit(): 
            if int(answer) in range(1, n + 1):
                break
        config.loggers.cli.log(30, error)
    return int(answer)

def kill_process(viewer):
    """
    Kill image viewer following review
    """    
    viewer = 'itk-snap' if viewer == 'itksnap' else viewer
    
    for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"):   # view the open applications with 'ps ax'
        pid = line.split()[0]                                           #process ID is the first column (0), isolate this item
        os.kill(int(pid), signal.SIGKILL)                               #kill process with PID, sigkill() terminates program


def convert_csv(db_name, new_db):
    import json
    import csv
    from mriqa.utils import list_collections

    if new_db:
        config.loggers.cli.log(30, msg = f'\n{mg.BREAK}\nNo stored review databases, exiting.\n{mg.BREAK}\n')
        quit()

    if config.session.mongodb:
        db_name = f"{config.session.output_dir}/mongodb-import_{db_name}.json"

    out_file = f"{db_name.replace('.json', '.csv')}"

    try:
        with open(db_name, 'r') as j:
            data = json.loads(j.read())
    except FileNotFoundError:
        config.loggers.cli.log(30, f'\n{mg.BREAK}\nFile not in path:\n     * {db_name}\n{mg.BREAK}\n')

        sys.exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    

    with open(out_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        
        #header
        csv_writer.writerow(['scan', 'review_count', 'voxels', 'scan_dims', 'user', 'path', 'date', 'viewer', 'rating'])
        
        # Iterate over each scan in the JSON data
        for scan, scan_data in data.items():
            review_count = scan_data['review_count']
            voxels = ', '.join(scan_data['voxels'])
            scan_dims = ', '.join(scan_data['scan_dims'])

            # Iterate over each rating in the scan
            for rating in scan_data['ratings']:
                csv_writer.writerow([
                    scan,
                    review_count,
                    voxels,
                    scan_dims,
                    rating['user'],
                    rating['path'],
                    rating['date'],
                    rating['viewer'],
                    rating['rating']
                ])
        config.loggers.cli.log(30, f'\n{mg.BREAK}\nConverted .json to .csv:\n     * {os.path.basename(out_file)}\n{mg.BREAK}\n')
