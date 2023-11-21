from collections import defaultdict
import json
from bson.json_util import dumps
import json

def import_mongo(collection, output_dir, review_id):

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
