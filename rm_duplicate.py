import pandas as pd
import os 
import subprocess

bids = '/home/mollyi/Projects/raw_data/RADIOqa_aep-main/'
radiol_niis = '/home/mollyi/Projects/raw_data/RADIOL_niis/'
radiol_csv = '/home/mollyi/Projects/repos/RADIOL_qa/data/merge_redcap-iqms/radiolqa_classifier_wide-average_ratings-SusGhostMotQual_20240515.csv'


radiol_df = pd.read_csv(radiol_csv)

aep_ids = set(radiol_df['aep_id'])

print(f'Total ids: {len(aep_ids)}')
print(aep_ids)


drctry = [item.replace('sub-', '') for item in os.listdir(bids) if os.path.isdir(os.path.join(bids, item))]
print(f'Total directories: {len(drctry)}')
print(drctry)

count_dups = []
for d in aep_ids:
    if str(d) in drctry:
        print(f'\nDuplicate: {d}')

        sub_files = [os.path.join(root, file) for root, dir, files in os.walk(f'{bids}/sub-{d}') for file in files if 'nii.gz' in file]
        rqa_files = [os.path.join(root, file) for root, dir, files in os.walk(f'{radiol_niis}/sub-{d}') for file in files if 'nii.gz' in file]

        print(sub_files)
        print(rqa_files)
        count_dups.append(f'sub-{d}')
        command = ['rm', '-rv', f'{bids}/sub-{d}']
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # command = ['itksnap', '-g', sub_files[0]] + ['-o'] + sub_files[1:] + rqa_files
        # viewer = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # in_option= input()
        # viewer.terminate()
        # viewer.wait()
print(f'Total Duplicates: {len(count_dups)}')
print(count_dups)
