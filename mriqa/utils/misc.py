import signal
from mriqa import config
from mriqa import messages as mg

import os
import sys
import re 
from dictionary.check_rating import check_radiologists

def verify_input(sessions = None, n = 5, msg=None, score= None, rate_type = 'image_quality', sequence = False):

    msg = msg if not sessions else sessions
    score = score if not sessions else ''
    error = mg.RATE_ERR if not sessions else mg.SES_ERR
    choice = mg.PICK_SCORE if not sessions else mg.PICK_SES
    
    if sequence:
        get_dict = input(f'\n--------------------------------------------------\nGet 📜 for {sequence} {rate_type}?\n-------------------------------------------------\n')
        if get_dict != '0':
            prediction = check_radiologists(dic_seq=config.session.dict_radiologists, 
                                            rtype=rate_type, 
                                            seq=sequence)
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

    os.kill(config.session._pid, signal.SIGKILL)
    #get pid from subprocess 
    
    #for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"):   # view the open applications with 'ps ax'
        #pid = line.split()[0]                                           #process ID is the first column (0), isolate this item
        #os.kill(int(pid), signal.SIGKILL)                               #kill process with PID, sigkill() terminates program


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
    

    with open(out_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        
        row_names = ['scan', 'review_count', 'voxels', 'scan_dims', 'user', 'path', 'date', 'viewer', 'rating']
        if config.session.artifacts:
            row_names.extend(['motion', 'susceptibility', 'flow_ghosting', 'inu', 'wrap_around']) #'gibbs', 
                             #'wrap_around', 'zipper', 'central_point', 'herringbone'])
        #header
        csv_writer.writerow(row_names)
        
        # Iterate over each scan in the JSON data
        for scan, scan_data in data.items():
            review_count = scan_data['review_count']
            voxels = ', '.join(scan_data['voxels'])
            scan_dims = ', '.join(scan_data['scan_dims'])

            # Iterate over each rating in the scan
            for rating in scan_data['ratings']:
                row_values = [scan, review_count, voxels, scan_dims,
                              rating['user'], rating['path'], rating['date'],rating['viewer'], rating['rating']]
            
                if config.session.artifacts:
                    row_values.extend([rating['artifact']['motion'],
                                       rating['artifact']['susceptibility'],
                                       rating['artifact']['flow_ghosting'], 
                                       rating['artifact']['inu'], 
                                       rating['artifact']['wrap_around']
                                       #rating['artifact']['gibbs'],
                                       #rating['artifact']['zipper'], 
                                       #rating['artifact']['central_point'],
                                       #rating['artifact']['herringbone']
                                       ])
                csv_writer.writerow(row_values)

        config.loggers.cli.log(20, f'\n{mg.BREAK}\nConverted .json to .csv:\n     * {os.path.basename(out_file)}\n{mg.BREAK}\n')



