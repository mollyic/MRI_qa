import os 
from mriqa import config, messages
from collections import defaultdict
import json
import re
from dotenv import load_dotenv                          
from pymongo import MongoClient
from mriqa import config
from os.path import basename as bn
from mriqa.utils import verify_input
from datetime import datetime


time_str = datetime.now().strftime("%Y%m%d_%H:%M:%S")   

class reviewer():

    def __init__(self):
        func = config.collector._db
        self.db, self.filename = func()
        self.max_reviews = []
        self.rater_reviewed = []

    def check(self, img):
        func = config.collector._check
        fargs = {'img': img, 'collection': self.db, 'max_reviews': self.max_reviews, 'rater_reviewed':self.rater_reviewed}
        review, self.max_reviews, self.rater_reviewed= func(**fargs)
        return review
    
    def review(self, img):
        func = config.collector._review
        fargs = {'img': img, 'collection': self.db}
        func(**fargs)


def list_collections(collections):
    """Generate list of already recorded results """
    
    if not collections:
        print('No sessions to resume, exiting.')
        quit()

    list_ses = ''
    for i, file in enumerate(collections):
        list_ses +=(f'{i+1}. {file}\n')

    index = verify_input(sessions = list_ses, n = i+1)
    
    return collections[int(index)-1]

def rater(msg, score):
    score = verify_input(msg=msg, score=score)
            
    return {'user': config.session.user, 'rating': score, 
            'date': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"), "viewer": config.session.viewer}

def _artifacts(img):

    rating = {artifact: verify_input(msg = messages.ART_MSG.format(artifact=artifact.upper(), img=img), score=messages.ART_SCORES) 
                for artifact in config.ARTIFACTS}
    return rating

class _JsonDB:
    def _db():
        
        results_dir = config.session.output_dir
        new_review = config.session._new_review

        collections = [item for item in os.listdir(results_dir) if re.match('^MRIqa(.*?.json$)', bn(item))]
        if not new_review and len(collections) >= 1:
            filename = f'{results_dir}/{list_collections(collections = collections)}'
            with open(filename, "r") as file:
                collection = defaultdict(dict, json.load(file))             #returns JSON object as dictionary  
        else: 
            filename = messages.REVIEW_FILE.format(output_dir = results_dir, 
                                                   review_id = config.session.review_id, 
                                                   date =time_str) + '.json'
            collection = defaultdict(dict)

        return collection, filename

    def _check(img, collection, max_reviews, rater_reviewed):        
        if img in collection.keys():
            for d in collection[img]['ratings']:
                if d['user'] == config.session.user:
                    rater_reviewed.append(img) 
            if collection[img].get('review_count') >=3:
                max_reviews.append(img)
           
        review = True if img not in max_reviews + rater_reviewed else False

        return review, max_reviews, rater_reviewed
    
    def _review(collection, img): 
        reviewed = True if img in collection.keys() else False
        rating = rater(msg = messages.OVERALL_MSG.format(img=img), score= messages.SCORES)
        
        if config.session.artifacts: 
            rating.update({'artifact':_artifacts(img)})
        
        if reviewed:
            collection[img]['ratings'].append(rating)
            collection[img]['review_count'] += 1
        else: 
            collection[bn(img)]['ratings'] = [rating]
            collection[bn(img)]['review_count'] = 1


class _MongoDB:

    def _db():
        load_dotenv(config.session.db_settings)                                 #load .env file with mongodb credentials
        client = MongoClient(host="localhost", port=27017, username=os.getenv('MONGO_DB_USRNAME'), password=os.getenv('MONGO_DB_PW'))

        db = client["image_ratings"]
        collections = [collec for collec in db.list_collection_names()]

        new_review = config.session._new_review
        

        if not new_review and len(collections) >= 1:
            review_id = list_collections(collections=collections)
        else:
            review_id = config.session.review_id

        collection = db[review_id]
        return collection, review_id
    


    def _check(img, collection, max_reviews, rater_reviewed):
        global user

        in_dict = collection.find_one({"scan_id": img})
        if in_dict:
            if in_dict["review_count"] >= 3: #scans reviewed >3 times
                max_reviews.append(img)
            if collection.find_one({'ratings.user': user, "scan_id": img}): #scans reviewed >3 times
                rater_reviewed.append(img)

        review = True if img not in max_reviews + rater_reviewed else False
        
        return review, max_reviews, rater_reviewed


    def _review(collection, img): 
        rating = rater(msg = messages.OVERALL_MSG.format(img=img), score= messages.SCORES)
        
        if config.session.artifacts: 
            rating.update({'artifact':_artifacts(img)})

        if collection.find_one({"scan_id": img}):
            collection.update_one({"scan_id": img}, {"$inc": {"review_count": 1}, "$push": {"ratings": rating}})
        else: 
            collection.insert_one({"scan_id": img, "review_count": 1, "ratings": [rating]}) 