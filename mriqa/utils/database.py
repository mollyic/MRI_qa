import os 
from mriqa import config, messages
from collections import defaultdict
import json
import re
from dotenv import load_dotenv                          
from pymongo import MongoClient
from mriqa import config
from os.path import basename as bn
from mriqa.utils import verify_input, input_cmnt
from datetime import datetime


time_str = datetime.now().strftime("%Y%m%d_%H:%M:%S")   

class reviewer():

    def __init__(self):
        func = config.collector._db
        self.db, self.filename, self.new_db = func()
        self.max_reviews = []
        self.rater_reviewed = []

    def check(self, img):
        func = config.collector._check
        fargs = {'img': img, 'collection': self.db, 'max_reviews': self.max_reviews, 'rater_reviewed':self.rater_reviewed}
        review, self.max_reviews, self.rater_reviewed= func(**fargs)
        return review
    
    def review(self, file):
        func = config.collector._review
        img = bn(file)
        fargs = {'img': img, 'collection': self.db, 'filepath' :file}
        func(**fargs)


def list_collections(collections):
    """Generate list of already recorded results """
    
    if not collections:
        config.loggers.cli.log(20, msg = 'No stored review databases, exiting')
        quit()

    list_ses = ''
    for i, file in enumerate(collections):
        list_ses +=(f'{i+1}. {file}\n')

    index = verify_input(sessions = list_ses, n = i+1)
    
    return collections[int(index)-1]

def rater(path, msg, score):
    score = verify_input(msg=msg, score=score)      

    return {'user': config.session.user, 'rating': score, 'path': path, #'masked': masked,
            'date': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"), "viewer": config.session.viewer}

def _artifacts(img):

    rating = {artifact: verify_input(msg = messages.ART_MSG.format(artifact=artifact.upper(), img=img), score=messages.ART_SCORES) 
                for artifact in config.ARTIFACTS}
    return rating

def _get_dims(file):
    import nibabel as nib
    img_ar = nib.load(file)
    vox = list(img_ar.header.get_zooms())
    dims = list(img_ar.shape)
    return [str(d) for d in dims], [str(v) for v in vox]

class _JsonDB:
    
    def _db():
        results_dir = config.session.output_dir
        new_review = config.session._new_review
        new_db = False
        collections = [item for item in os.listdir(results_dir) if re.match('^MRIqa(.*?.json$)', bn(item))]

        if not new_review and len(collections) >= 1:
            filename = f'{results_dir}/{list_collections(collections = collections)}'
            with open(filename, "r") as file:
                collection = defaultdict(dict, json.load(file))             #returns JSON object as dictionary  
        else: 
            filename = f"{results_dir}/{messages.REVIEW_FILE.format(review_id = config.session.review_id, date =time_str)}.json"
            collection = defaultdict(dict)
            new_db = True
        
        return collection, filename, new_db

    def _check(img, collection, max_reviews, rater_reviewed):        
        if img in collection.keys():
            for d in collection[img]['ratings']:
                if d['user'] == config.session.user:
                    rater_reviewed.append(img) 
            if collection[img].get('review_count') >=3:
                max_reviews.append(img)
           
        review = True if img not in max_reviews + rater_reviewed else False

        return review, max_reviews, rater_reviewed
    
    def _review(collection, filepath, img): 

        rating = rater(msg = messages.OVERALL_MSG.format(img=img), score= messages.SCORES, path = filepath)
        if config.session.artifacts: 
            #review artifacts if option enabled
            rating.update({'artifact':_artifacts(img)})
        if config.session.comment: 
            #add comment if option enabled
            rating.update({'comment':input_cmnt()})

        if not img in collection.keys():
            dims, vox = _get_dims(filepath)
            collection[img] = {'ratings': [rating], 'review_count': 1, 'voxels': vox, 'scan_dims': dims}
        else:
            collection[img]['ratings'].append(rating)
            collection[img]['review_count'] += 1
        return False

class _MongoDB:

    def _db():
        from mriqa.utils import create_mongo_env
        new_db = False

        if not config.session.db_settings.exists():
            print('No settings file found. Provide MongoDB details to save to settings.env files.')
            create_mongo_env()

        load_dotenv(config.session.db_settings)                                 #load .env file with mongodb credentials
        
        client = MongoClient(host=os.getenv('MONGODB_HOST'), 
                             port=int(os.getenv('MONGODB_PORT')), 
                             username=os.getenv('MONGODB_USRNAME'), 
                             password=os.getenv('MONGODB_PW'))
        db = client["db_test"]

        # TROUBLESHOOTING: drop mongodbs
        # for d in db.list_collection_names():
        #     db[d].drop()

        collections = [collec for collec in db.list_collection_names()]
        if not config.session._new_review and len(collections) >= 1:
            db_name = list_collections(collections=collections)
        else:
            db_name = f"{messages.REVIEW_FILE.format(review_id = config.session.review_id, date =time_str)}"
            new_db = True
        collection = db[db_name]
        return collection, db_name, new_db
    


    def _check(img, collection, max_reviews, rater_reviewed):

        in_dict = collection.find_one({"scan_id": img})
        if in_dict:
            if in_dict["review_count"] >= 3: #scans reviewed >3 times
                max_reviews.append(img)
            if collection.find_one({'ratings.user': config.session.user, "scan_id": img}): #scans reviewed >3 times
                rater_reviewed.append(img)

        review = True if img not in max_reviews + rater_reviewed else False
        
        return review, max_reviews, rater_reviewed


    def _review(collection, filepath, img): 

        rating = rater(msg = messages.OVERALL_MSG.format(img=img), score= messages.SCORES, path =filepath)
        
        if config.session.artifacts: 
            #review artifacts if option enabled
            rating.update({'artifact':_artifacts(img)})
        if config.session.comment: 
            #add comment if option enabled
            rating.update({'comment':input_cmnt()})

        if collection.find_one({"scan_id": img}):
            collection.update_one({"scan_id": img}, {"$inc": {"review_count": 1}, "$push": {"ratings": rating}})
        else: 
            dims, vox = _get_dims(filepath)
            collection.insert_one({"scan_id": img, "review_count": 1, "voxels": vox, "scan_dims": dims, "ratings": [rating]}) 
        
        return False