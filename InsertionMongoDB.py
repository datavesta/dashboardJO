import json
from pymongo import MongoClient

client = MongoClient("localhost", 27017)

database = client["sportsdb"]

collection1 = database["athletes"]
collection2 = database["disciplines"]
collection3 = database["editions"]
requesting = []

with open("files/athletes_with_results.json","r") as f:
    data= json.load(f)
    collection1.insert_many(data)
   
print(f"Nombre d'eléments collections athletes : {collection1.count_documents({})}")

with open("files/disciplines_with_results.json","r") as f:
    data= json.load(f)
    collection2.insert_many(data)
   
print(f"Nombre d'eléments collections disciplines : {collection2.count_documents({})}")

with open("files/editions_with_results.json","r") as f:
    data= json.load(f)
    collection3.insert_many(data)
   
print(f"Nombre d'eléments collections editions : {collection3.count_documents({})}")

client.close()