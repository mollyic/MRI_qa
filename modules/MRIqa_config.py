import os 
import signal
from configparser import ConfigParser
import re
#config file with file paths 
config_file = "MRIQA_config.ini"
config = ConfigParser()
config.read(config_file)

#GLOBAL VARS --------------------------------------------------
ERR_STRING = "Invalid entry, enter a number from 1-5\n--------------------------------------"

#UPDATE CONFIG FILE --------------------------------------------------
#if participant has no config settings or wishes to update them  
#this function saves the details to the config file for future use 
def configupdate():
    config_qs = ["Enter image viewer index:\n1 - ITK-SNAP\n2 - MRView\n3 - FSLeyes\n", 
                    "Folders to review:\n1 - ANAT folder\n2 - All folders\n\n"] 
    viewers = ['itksnap', 'mrview', 'fsleyes'] 
    string = []
    input_params = [] 
    for count, q in enumerate(config_qs): 
        print("\033c")
        while True:
            print(q)
            review = input("Selection: ")
            print("\033c")
            if review.isdigit(): 
                if int(review) in range(1,3):
                    break
                else:
                    print("\033c" + ERR_STRING.replace('5', '2'))
            else: 
                print("\033c" + ERR_STRING.replace('5', '2'))
        
        if count == 0:                                  #count 0 = Q1 viewer types
            viewer = viewers[int(review)-1] 
        
        if count == 1:                                  #count 1 = Q2 folder type
            if review == '1':
                string = '(.*nii$|.*nii.gz$)'
                input_params = 'anat folder'
            elif review == '2':
                while True: 
                    print("Files to review:\n1 - All files\n2 - By sequence (e.g. T1 & T2)\n3 - Filenames match user-inputted string\n",)
                    files = input("Selection: ")
                    if files.isdigit(): 
                        if int(files) in range(1,4):
                            break
                        else:
                            print("\033c" + ERR_STRING.replace('5', '3'))
                    else: 
                        print("\033c" + ERR_STRING.replace('5', '3'))
                if files == '1':
                    string = '(.*nii$|.*nii.gz$)'
                    input_params = 'all files'

                elif files == '2':
                    seqs = ['T1', 'T2', 'FLAIR', 'DWI'] 
                    while True:
                        print(f"Enter sequence index(es):\n1 - {seqs[0]}    2 - {seqs[1]}    3 - {seqs[2]}    4 - {seqs[3]} ")
                        select_bids = input("\nSelection: ")
                        all_nums = re.findall(r'\d+', select_bids)
                        seq_list = [x for x in all_nums if int(x) in range(1, len(seqs)+1)]
                        if len(seq_list) == 0:
                            print("\033c")
                            print("No valid sequences selected.\n")
                            continue        
                        else:
                            break

                    for seq in seq_list:
                        input_params += [f'{seqs[int(seq)-1]}']
                        string += [f'(^sub-.*{seqs[int(seq)-1].lower()}.*.nii*)']
                    string = "|".join(string)
                    string = '(?i)'+ string
                    print(f"Reviewing sequences: {input_params}")

                elif files == '3':
                    print("Enter unique identifiers separated by whitespace\n\nExample: dwi ses-01 swi\n\n")
                    uniqueID = input("Selection: ")
                    print("\033c")
                    for id in uniqueID.split(' '):
                        string += [f'(.*{str(id)}.*.nii*)']
                        input_params += [id]
                    string = "|".join(string)
                    string = '(?i)'+string

    print("\033c")
    #artifacts = 'True' if input("Rate severity of artifacts for each scan? (Motion, susceptibility, flow/ghosting)\n\nSelection (y/n): ") == 'y' else 'False'
    print("\033c")

    config['settings']['re_params'] = string 
    config['settings']['input_params'] = str(input_params)
    #config['settings']['artifacts'] = str(artifacts)
    config['settings']['viewer'] = viewer

    with open(config_file, 'w') as rewrite:    # save
        config.write(rewrite)

