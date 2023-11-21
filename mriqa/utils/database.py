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


user = config.session.user

class reviewer():

    def __init__(self):
        func = config.collector._db
        self.db, self.filename = func()
        self.max_reviews = []
        self.rater_reviewed = []

    def check(self):
        func = config.collector._check
        fargs = {'collection': self.db, 'max_reviews': self.max_reviews, 'rater_reviewed':self.rater_reviewed}
        review, self.max_reviews, self.rater_reviewed= func(**fargs)
        return review
    
    def review(self, img):
        func = config.collector._review
        fargs = {'img': img, 'collection': self.db}
        func(**fargs)

    def artifacts(self):
        func = config.collector._artifacts
        fargs = {'sigma': self.sigma, 'truncate': self.sdlen, 'mode': 'reflect'}

        func(collections = self.db, **fargs)



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

def rater(img):
    from mriqa import messages
    from datetime import datetime
    config.loggers.cli.log(30, f'{messages.BREAK}\n\nImage: {bn(img)}\n\nOverall image quality rating:\n')
    score = verify_input()
            
    return {'user': config.session.user, 'rating': score, 
            'date': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"), "viewer": config.session.viewer}

class _JsonDB:
    def _db():
        
        results_dir = config.session.output_dir
        review_id = config.session.review_id + '.json'
        new_review = config.session._new_review

        collections = [item for item in os.listdir(results_dir) if re.match('(.*?.json$)', item)]
        if not new_review and len(collections) >= 1:
            filename = f'{results_dir}/{list_collections(collections = collections)}'
            with open(filename, "r") as file:
                collection = defaultdict(dict, json.load(file))             #returns JSON object as dictionary  
        else: 
            filename = messages.REVIEW_FILE.format(output_dir = results_dir, review_id = review_id)
            collection = defaultdict(dict)

        return collection, filename

    def _check(img, collection, max_reviews, rater_reviewed):
        global user
        
        max_reviews = (max_reviews.append(img) if collection[img]['review_count'] >= 3 else max_reviews) #scans reviewed >3 times
        rater_reviewed = (rater_reviewed.append(img) if collection[img]['review_count']['user'] == user else rater_reviewed) #scans reviewed >3 times
        review = True if img not in max_reviews + rater_reviewed else False

        return review, max_reviews, rater_reviewed
    
    def _review(collection, img): 
        """Move check function internally:
            check each file instantaneously
            """
        rating = rater(img)
        reviewed = True if bn(img) in collection.keys() else False

        if reviewed:
            collection[bn(img)]['ratings'].append(rating)
            collection[bn(img)]['review_count'] += 1
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
        review_id = config.session.review_id

        if not new_review and len(collections) >= 1:
            collection = db[list_collections(collections=collections)] 
        else:
            collection = db[review_id]
        
        return collection, str(collection)
    


    def _check(img, collection, max_reviews, rater_reviewed):
        global user

        max_reviews = (max_reviews.append(img) if collection.find_one({"scan_id": img}).get("review_count", 0) >= 3 else max_reviews) #scans reviewed >3 times
        rater_reviewed = (rater_reviewed.append(img) if collection.find_one({'ratings.username': user, "scan_id": img}) else rater_reviewed) #scans reviewed >3 times
        review = True if img not in max_reviews + rater_reviewed else False
        
        return review, max_reviews, rater_reviewed

    def _review(collection, img): 
        rating = rater(img)

        if collection.find_one({"scan_id": img}):
            collection.update_one({"scan_id": img}, {"$inc": {"review_count": 1}, "$push": {"ratings": rating}})
        else: 
            collection.insert_one({"scan_id": img, "review_count": 1, "ratings": [rating]})    
