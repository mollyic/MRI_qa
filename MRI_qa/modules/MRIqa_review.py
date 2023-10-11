import os 
import signal
from pymongo import MongoClient
from dotenv import load_dotenv                          
from datetime import datetime
import re 
from collections import defaultdict
import json


#GLOBAL VARS --------------------------------------------------
time_str = datetime.now().strftime("%d%m%Y_%H%M")     #date for output files
ERR_STRING = "Invalid entry, enter a number from 1-5\n--------------------------------------"

class collector:
    def __init__(self, results_dir, local, new, sesh_str = f'MRIrate_{time_str}'):
        
        self.new = new
        self.sesh_str = sesh_str
        self.local = local

        if local:
            if not os.path.exists("MRI_rating_record/"):
                os.mkdir("MRI_rating_record/")
                print("\n\nDirectory 'MRI_rating_record' created! Your ratings will be stored here. \n\n")

            
            self.results_dir = results_dir
            self.db = defaultdict
            if not new:
                self.filename = f'MRI_rating_record/{self.list_collections()}'
                with open(self.filename, "r") as file:
                    self.collection = defaultdict(dict, json.load(file))             #returns JSON object as dictionary  
            else: 
                self.filename = f'MRI_rating_record/{sesh_str}_{time_str}.json'
                self.collection = defaultdict(dict)



        else:
            load_dotenv('settings.env')                                 #load .env file with mongodb credentials
            client = MongoClient(host="10.101.98.10", port=27017, username=os.getenv('MONGO_DB_USRNAME'), password=os.getenv('MONGO_DB_PW'))
            self.db = client["image_ratings"]
            if not new:
                self.collection = self.db[self.list_collections()] 
            else:
                self.collection = self.db[sesh_str]
    
    def list_collections(self):
        
        """
        
        Generate list of already recorded results 
        
        """
        if self.local:
            collections = [item for item in os.listdir(self.results_dir) if re.match('(.*?.json$)', item)]
        else:
            # for i in db.list_collection_names():
            #     print(i)
                #db.drop_collection(i)
            collections = [collec for collec in self.db.list_collection_names() if re.match(f"{self.sesh_str}.*", collec)]
        
        while True:
            try:
                if not collections:
                    input('No sessions to resume, exiting.')
                    quit()
                for i,file in enumerate(collections):
                    print(f'{i+1}. {file}')
                index = int(input("Enter session number to resume: ")) -1
                print("\033c")
                if not index in range(0, len(collections)): 
                    raise ValueError
                break
        
            except ValueError:
                print("\033c")
                print("\nInvalid session, try again:\n")
        
        return collections[index]

    def review_image(self, username, image_id, viewer):
        """
        
        Enter rating for image into database
        
        """
        reviewed = False
        allreviewed = False
        user_reviewed = False
        if self.local:
            if image_id in self.collection.keys():
                reviewed = True
                if self.collection[image_id]['review_count'] >= 3:
                    allreviewed = True
                for dic in self.collection[image_id]['ratings']:
                    print(dic)
                    if dic['user'] == username:
                       user_reviewed = True
        else:
            existing_image = self.db.find_one({"scan_id": image_id})
            if existing_image:
                reviewed = True
                if existing_image.get("review_count", 0) >= 3:
                    allreviewed = True
            existing_rating = self.collection.find_one({'ratings.username': username, "scan_id": image_id})
            if existing_rating:
                user_reviewed = True
        
        if allreviewed:
            print(f"Image {image_id} has already been reviewed 3 times and will not be reviewed again.")
            return
        if user_reviewed:
            print(f"{username} has already reviewed the image {image_id} and cannot review it again.")
            return

        while True: 
            print("--------------------------------------------------")
            print(f'\nImage: {image_id}\n\nOverall image quality rating:')
            print('1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent\n\n')
            img_rating = (input(f"{username}, enter rating (1 - 5): \n\n"))
            if img_rating.isdigit(): 
                if int(img_rating) in range(1,6):
                    self.save_review(username = username, image_id=image_id, viewer=viewer, img_rating=img_rating, reviewed = reviewed)
                    return img_rating
                else:
                    print('\033c')
                    print(ERR_STRING)
            else: 
                print('\033c')
                print(ERR_STRING)
    
    def save_review(self, username, image_id, viewer, img_rating, reviewed = False):
        ratings = {'user': username, 'rating': img_rating, 'date':time_str, "viewer": viewer}
        if self.local:
            if reviewed:
                self.collection[image_id]['ratings'].append(ratings)
                self.collection[image_id]['review_count'] += 1
            else: 
                self.collection[image_id]['ratings'] = [ratings]
                self.collection[image_id]['review_count'] = 1

        else: #$inc: increment a rating by provided value (1) ; $push: appends value to array (ratings)
            if reviewed:
                self.collection.update_one({"scan_id": image_id}, {"$inc": {"review_count": 1}, "$push": {ratings}})
            else: 
                self.collection.insert_one({"scan_id": image_id, "review_count": 1, "ratings": [{ratings}]})    



def kill_process(viewer):
    """
    Kill image viewer following review
    """    
    if viewer == 'itksnap':
        viewer = 'itk-snap'
    
    for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"):   # view the open applications with 'ps ax'
        pid = line.split()[0]                                           #process ID is the first column (0), isolate this item
        os.kill(int(pid), signal.SIGKILL)                               #kill process with PID, sigkill() terminates program



def review_artifacts(username, image_id, collection):
    
    """
    
    Record artifact rating for image 
    
    """
    
    artifact_list = ['susceptibility', 'motion', 'flow_ghosting']       #define possible artifacts 
    for artifact in artifact_list:                                      
        existing_rating = collection.find_one({'ratings.username': username, "scan_id": image_id, 
                                                f'ratings.{artifact}':{"$exists": True}})
        if existing_rating:                                             #check if rater has reviewed the artifacts 
            print(f"{username} has already reviewed {artifact} for image: {image_id}")
            continue
        while True: 
            valid_rating = False
            print(f"\nImage: {image_id}\n" )
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
        
    
    """
    
    Choice of reviewing either subject-wise or all subjects
    
    """
    

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
