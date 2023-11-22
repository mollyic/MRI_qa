from collections import defaultdict
import json
from bson.json_util import dumps
import json
from mriqa import config

def create_mongo_env():
    """
    Create a settings.env file for mongoDB instance
    """
    username = input("Enter MongoDB username:")        
    password = input("Enter MongoDB password:")        
    host =     input("Enter MongoDB hostname (hit enter for default localhost):")    
    
    settings = {
        "MONGODB_USRNAME": username,
        "MONGODB_PW": password, 
        "MONGODB_HOST": host if len(host) >= 1 else 'localhost'}
    
    with open(config.session.db_settings, "w") as file:
        for key, value in settings.items():
            file.write(f"{key} = \"{value}\"\n")


def import_mongo(collection, output_dir, review_id):
    """
    Import mongoDB results into .json file
    """
    data = collection.find()                                        #convert collection to python dictionary 
    json_docs = [dumps(doc, default = str) for doc in data]         #convert each doc to json string 

    dct = defaultdict()
    for doc in json_docs:
        res = json.loads(doc)
        del res["_id"]
        dct[res["scan_id"]] = res
            #file.write(doc + ",\n")

    json_object = json.dumps(dct, indent = 4) 

    # Writing to sample.json
    filename =f"{output_dir}/mongodb-import_{review_id}.json"
    with open(filename, "w") as outfile:
        outfile.write(json_object)
