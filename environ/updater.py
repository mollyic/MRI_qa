from configparser import ConfigParser
import config
import re 
from messages import VIEWERS, MSGS
from pathlib import Path
import os

wrong_int = config.ERR_STRING
config_file = config.session.user_env
parse = ConfigParser()
parse.read(config_file)


def configupdate():
    config_qs = [str("Enter image viewer index:\n1 - ITK-SNAP\n2 - MRView\n3 - FSLeyes\n"), (f"{MSGS['choice_note']}\n\nFolders to review:\n1 - ANAT folder\n2 - All folders\n\n")] 
    
    string = []
    input_params = str()
    answers = []
    for q in config_qs: 
        print("\033c")
        while True:
            print(str(q))
            review = input("Selection: ")
            print("\033c")
            if review.isdigit(): 
                if int(review) in range(1,4):
                    answers.append(review)
                    break
            print(f"\033c{wrong_int.replace('5', '2')}")
        
    viewer = VIEWERS[int(answers[0])-1] 

    while True:
        input_images = input("Input nifti file directory: ")
        if os.path.isdir(Path(input_images).absolute()):
            break
        print(f'\033c{Path(input_images).absolute()} is not a valid directory.\n')
    print('\033c')
    while True: 
        print(f"{MSGS['choice_note']}\n\nFiles to review:\n1 - All \n2 - By modality (T1w, T2w or FLAIR)\n3 - By user-inputted string\n",)
        file_choice = input("Selection: ")
        if file_choice.isdigit(): 
            if int(file_choice) in range(1,4):
                break
        print("\033c" + wrong_int.replace('5', '3'))
        
    if file_choice == '1':
        """All files"""                    
        string = '(?i).*(.*nii$|.*nii.gz$)'
        input_params = ' all files '

    elif file_choice == '2':
        """By modality"""                    
        seqs = ['T1w', 'T2w', 'FLAIR'] 
        while True:
            print(f"Enter sequence index(es):\n1 - {seqs[0]}    2 - {seqs[1]}    3 - {seqs[2]}")
            select_bids = input("\nSelection: ")
            all_nums = re.findall(r'\d+', select_bids)
            seq_list = [x for x in all_nums if int(x) in range(1, len(seqs)+1)]
            if len(seq_list) == 0:
                print("\033c")
                print("No valid sequences selected.\n")
                continue        
            break

        for seq in seq_list:
            input_params += f' {seqs[int(seq)-1]} '
            string += [f'(^sub-.*{seqs[int(seq)-1].lower()}(.*nii$|.*nii.gz$))']
        string = "|".join(string)
        string = '(?i)'+ string

    elif file_choice == '3':
        """By string"""
        print("Enter unique identifiers separated by whitespace\n\nExample: dwi ses-01 swi\n\n")
        uniqueID = input("Selection: ")
        print("\033c")
        for id in uniqueID.split(' '):
            string += [f'(.*{str(id)}(.*nii$|.*nii.gz$))']
            input_params += f' {id} '
        string = "|".join(string)
        string = '(?i)'+string

    if answers[1] == '1':
        input_params = 'anat folder,' + input_params

    seshid = input("\033cInput new session ID used to name .csv and database outputs.\n\nID: ")
    print("\033c")
    print(f"Reviewing sequences: {input_params}")


    print(input_params)
    print(input_params)
    parse['settings']['input_images'] = input_images 
    parse['settings']['re_params'] = string 
    parse['settings']['input_params'] = str(input_params)
    parse['settings']['viewer'] = viewer
    parse['settings']['seshid'] = seshid 

    
    with open(config_file, 'w') as rewrite:    # save
        parse.write(rewrite)

