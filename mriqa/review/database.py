import os 
from mriqa import config, messages
from collections import defaultdict
import json
import re
from mriqa.review import list_collections
from dotenv import load_dotenv                          
from pymongo import MongoClient

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

    def _check(collection):
        from mriqa import messages
        from os.path import basename as bn

        user = config.session.user
        in_files = config.session.inputs
        
        ids = [bn(file) for file in in_files if bn(file) in collection.keys()]          #ids already in dict                     
        maxxed = [id for id in ids if collection[id]['review_count'] >= 3]              #scans reviewed >3 times
        ratered = [id for id in ids for dic in collection[id]['ratings'] if dic['user'] == user] #scans reviewed by user
        
        if maxxed:
            config.loggers.cli.log(30, msg = messages.MAX_RATED.format(img_list = maxxed))
        if ratered:
            config.loggers.cli.log(30, msg = messages.RATER_RATED.format(img_list = ratered, username=user))
        
        review = list([item for item in in_files if bn(item) not in maxxed + ratered])
        return review
    
    def _review(collection, img): 
        from mriqa import messages
        from datetime import datetime
        from os.path import basename as bn
        
        reviewed = True if bn(img) in collection.keys() else False
        rating = input(f'{messages.BREAK}\n\nImage: {bn(img)}\n\nOverall image quality rating:\n{messages.SCORES}')
                
        ratings = {'user': config.session.user, 'rating': rating, 
                   'date': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"), "viewer": config.session.viewer}

        if reviewed:
            collection[bn(img)]['ratings'].append(ratings)
            collection[bn(img)]['review_count'] += 1
        else: 
            collection[bn(img)]['ratings'] = [ratings]
            collection[bn(img)]['review_count'] = 1


class _MongoDB:

    def _db():
        load_dotenv(config.session.db_settings)                                 #load .env file with mongodb credentials
        client = MongoClient(host="10.101.98.10", port=27017, username=os.getenv('MONGO_DB_USRNAME'), password=os.getenv('MONGO_DB_PW'))
        db = client["image_ratings"]
        collections = [collec for collec in db.list_collection_names()]

        new_review = config.session._new_review
        review_id = config.session.review_id

        if not new_review:
            collection = db[list_collections(collections=collections)] 
        else:
            collection = db[review_id]
        
        return collection
    


    def _check(image_id, username, collection):
        
        ALL_REVIEWD = f"Image {image_id} has already been reviewed 3 times and will not be reviewed again."
        YOU_REVIEWD = f"{username} has already reviewed the image {image_id} and cannot review it again."
        reviewed = False
        MSG = None


        #previous code:         existing_image = db.find_one({"scan_id": image_id})
        existing_image = collection.find_one({"scan_id": image_id})
        
        if existing_image:
            reviewed = True
            if existing_image.get("review_count", 0) >= 3:
                MSG = ALL_REVIEWD
        existing_rating = collection.find_one({'ratings.username': username, "scan_id": image_id})
        if existing_rating:
            MSG = YOU_REVIEWD
        
        return MSG, reviewed

    def _review(reviewed, collection, image_id, ratings): 

        if reviewed:
            collection.update_one({"scan_id": image_id}, {"$inc": {"review_count": 1}, "$push": {ratings}})
        else: 
            collection.insert_one({"scan_id": image_id, "review_count": 1, "ratings": [{ratings}]})    
