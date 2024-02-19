import signal
from mriqa import config
from mriqa import messages as mg

import os
import sys

def input_cmnt():
    config.loggers.cli.log(20,  mg.CMNT_MSG)
    answer = input("Comment:")
    return answer

def verify_input(sessions = None, n = 5, msg=None, score= None):

    msg = msg if not sessions else sessions
    score = score if not sessions else ''
    error = mg.RATE_ERR if not sessions else mg.SES_ERR
    choice = mg.PICK_SCORE if not sessions else mg.PICK_SES

    while True:
        config.loggers.cli.log(20,  msg)
        config.loggers.cli.log(20,  score)

        answer = input(choice)
        if answer.isdigit(): 
            if int(answer) in range(1, n + 1):
                break
        config.loggers.cli.log(20, error)
    config.loggers.cli.log(10, f"{choice}: {answer}")
    return int(answer)

def kill_process(viewer):
    """
    Kill image viewer following review
    """    
    viewer = 'itk-snap' if viewer == 'itksnap' else viewer
    os.kill(config.session._pid, signal.SIGTERM)



def convert_csv(db_name, new_db):
    import json
    import csv

    if new_db:
        config.loggers.cli.log(20, msg = f'\n{mg.BREAK}\nNo stored review databases, exiting.\n{mg.BREAK}\n')
        quit()

    if config.session.mongodb:
        db_name = f"{config.session.output_dir}/mongodb-import_{db_name}.json"

    out_file = f"{db_name.replace('.json', '.csv')}"

    try:
        with open(db_name, 'r') as j:
            data = json.loads(j.read())
    except FileNotFoundError:
        config.loggers.cli.log(20, f'\n{mg.BREAK}\nFile not in path:\n     * {db_name}\n{mg.BREAK}\n')

        sys.exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    

    comment =any('comment' in key for scan in data.keys() for key in data[scan]['ratings'])
    artifacts =any('artifact' in key for scan in data.keys() for key in data[scan]['ratings'])

    with open(out_file, 'w', newline='') as file:
        fieldnames = ['scan', 'review_count', 'voxels', 'scan_dims', 'user', 'path', 'date', 'viewer', 'rating']

        if comment:
            fieldnames.append('comment')
        if artifacts:
            fieldnames.extend(['susceptibility', 'motion', 'flow_ghosting'])        
        

        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        # Iterate over each scan in the JSON data
        for scan, scan_data in data.items():
            # Common data for all ratings
            common_data = {
                'scan': scan,
                'review_count': scan_data['review_count'],
                'voxels': ', '.join(scan_data['voxels']),
                'scan_dims': ', '.join(scan_data['scan_dims']),
            }

            # Iterate over each rating in the scan
            for rating in scan_data['ratings']:
                row_data = {
                    **common_data,
                    'user': rating['user'],
                    'path': rating['path'],
                    'date': rating['date'],
                    'viewer': rating['viewer'],
                    'rating': rating['rating']
                }
                if comment and 'comment' in rating:
                    row_data['comment'] = rating['comment']
                
                if artifacts and 'artifact' in rating:
                    row_data['susceptibility'] = rating['artifact']['susceptibility']
                    row_data['motion'] = rating['artifact']['motion']
                    row_data['flow_ghosting'] = rating['artifact']['flow_ghosting']
                
                csv_writer.writerow(row_data)

        config.loggers.cli.log(20, f'\n{mg.BREAK}\nConverted .json to .csv:\n     * {os.path.basename(out_file)}\n{mg.BREAK}\n')
