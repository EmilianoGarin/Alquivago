import requests
import pymongo
import json

# Connect to the MongoDB Atlas database
atlas_uri = "mongodb+srv://alquivago:alquivago123@cluster0.hhicxbc.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(atlas_uri)
db = client["alquivago"]

# URLs of the JSON files on GitHub
property_types_url = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/dev/mongodb/property_types.json"
zonas_montevideo_url = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/dev/mongodb/zonas_montevideo.json"

# Define the names of the MongoDB collections
property_types_col = db["property_types_col"]
zonas_mvd_col = db["zonas_mvd_col"]

# Function to download and insert JSON data into a MongoDB collection
def insert_json_into_mongo(url, collection):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        collection.insert_one(data)
        print(f"Data from {url} inserted into MongoDB collection: {collection.name}")
    else:
        print(f"Failed to retrieve data from {url}")

# Insert property_types.json into the property_types_col collection
insert_json_into_mongo(property_types_url, property_types_col)

# Insert zonas_montevideo.json into the zonas_mvd_col collection
insert_json_into_mongo(zonas_montevideo_url, zonas_mvd_col)
