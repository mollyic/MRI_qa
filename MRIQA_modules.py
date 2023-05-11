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

def kill_process(viewer):
    if viewer == 'itksnap':
        viewer = 'itk-snap'
    # view the open applications with 'ps ax' then pipe results into grep
    for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"): # exclude grep search using '-v'
        pid = line.split()[0] #process ID is the first column (0), isolate this item
        os.kill(int(pid), signal.SIGKILL) #kill process by providing the PID, sigkill() terminates program


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


def update_rating(username, image_id, collection, viewer):
    existing_image = collection.find_one({"scan_id": image_id})
    if existing_image:                                                  #check if image exists in db 
        if existing_image.get("review_count", 0) >= 3:                  #check image has been reviewed less than 3 times
            print(f"Image {image_id} has already been reviewed 3 times and will not be reviewed again.")
            return

        #check if rater has reviewed image
        existing_rating = collection.find_one({'ratings.username': username, "scan_id": image_id})
        if existing_rating:
            print(f"{username} has already reviewed the image {image_id} and cannot review it again.")
            return

        rating = review_image(username, image_id)                       #if conditions not met: proceed with rating
        #$inc: increment a rating by provided value (1)
        #$push: appends value to array (ratings)
        collection.update_one({"scan_id": image_id}, {"$inc": {"review_count": 1}, "$push": {"ratings": {"username": username, "rating": rating, "viewer": viewer}}})
    
    else:                                                               #if the image does not exist create a new entry
        rating = review_image(username, image_id)
        collection.insert_one({"scan_id": image_id, "review_count": 1, "ratings": [{"username": username, "rating": rating, "viewer": viewer}]})



def review_image(username, image_id):
    while True: 
        print('Image: ' + image_id)
        print('\nOverall image quality rating')
        print('1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent\n')
        img_rating = (input(f"{username}, enter rating (1 - 5): "))
        if img_rating.isdigit(): 
            if int(img_rating) in range(1,6):
                return img_rating
            else:
                print('\033c')
                print(ERR_STRING)
        else: 
            print('\033c')
            print(ERR_STRING)
    
    
def review_artifacts(username, image_id, collection):
    artifact_list = ['susceptibility', 'motion', 'flow_ghosting']       #define possible artifacts 
    for artifact in artifact_list:                                      
        existing_rating = collection.find_one({'ratings.username': username, "scan_id": image_id, 
                                                f'ratings.{artifact}':{"$exists": True}})
        if existing_rating:                                             #check if rater has reviewed the artifacts 
            print(f"{username} has already reviewed {artifact} for image: {image_id}")
            continue
        while True: 
            valid_rating = False
            print(f"Image: {image_id}\n" )
            print(f"Rating for {artifact.upper()} artifact ")
            print('1 - Severe       2 - Moderately Severe       3 - Moderate        4 - Mild        5 - None\n')
            rating = input(f"{username}, enter rating (1 to 5): ")
            if rating.isdigit():  
                valid_rating = True if int(rating) in range(1,6) else False
            if rating == '': valid_rating = True 
            if valid_rating: 
                collection.update_one({'ratings.username': username, "scan_id": image_id},[{"$set": {"ratings": {artifact: rating}}}])
                print("\033c")
                break 
            else:
                print("\033c" + ERR_STRING +'\n')

def review_subject():
    print('\033c')
    while True:
        print("Review: \n\n1 - All subjects \n2 - Single subject")
        review = input("\nSelection: ")
        if review.isdigit(): 
            if int(review) in range(1,3):
                break
            else:
                print("\033c" + ERR_STRING.replace('5', '2'))
        else: 
            print("\033c" + ERR_STRING.replace('5', '2'))
    if int(review) == 2:
        print("\033c")
        return input("Enter subject ID: ")

class fileexts:
    def __init__(self, filename) -> None:
        self.name = filename.split('/')[-1].split('.',1)[0]             #no dirs or file ext
