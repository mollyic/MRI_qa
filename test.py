import signal
from mriqa import messages, config
import os
import sys

def convert_csv(json_data):
    print("Converting to .csv...")
    import json
    import csv

    config.loggers.cli.log(30, f'Converting file to .csv:\n{os.path.basename(json_data)}\n')

    if config.session.mongodb:
        json_data = f"{config.session.output_dir}/monog-import_{json_data}"

    out_file = f"{config.session.output_dir}/{os.path.basename(json_data).replace('.json', '.csv')}"

    try:
        with open(json_data, 'r') as j:
            data = json.loads(j.read())
    except FileNotFoundError:
        config.loggers.cli.log(30, f'File not in path:\n{os.path.dirname(json_data)}\n')
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


f ='/home/unimelb.edu.au/mollyi/Documents/Projects/Repos/MRIQA_tool/code/mriqa/output/MRIqa_SUDMEX_20231123_13:11:14 copy.json'

convert_csv(f)