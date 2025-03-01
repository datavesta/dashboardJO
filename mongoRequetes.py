import json
from pymongo import MongoClient

client = MongoClient("localhost", 27017)

database = client["sportsdb"]

collection1 = database["athletes"]
collection2 = database["disciplines"]



#results=collection2.find({"event":"Handball, Men"},{"id":1,"medals_by_country":1})

results = collection2.aggregate([
  { "$unwind": "$results" },  
  {
    "$group": { 
      "_id": "$discipline",  
      "distinct_athletes": { "$addToSet": "$results.athlete_id" } ,
      "nb_participants": { "$first": "$nb_participants" }
    }
  },
  { 
    "$project": { 
      "nb_participants": 1,
      "nb_athletes": { "$size": "$distinct_athletes" } 
  
    }
  }])

results2 = collection1.count_documents({"sex":"Female", "results.year":{"$lte":2000}})

results3 = collection1.aggregate([
    {"$unwind":"$results"},
    {"$group": {"_id" : {"sport":"$results.sport","event":"$results.event", "year":"$results.year"},"nb": 
                {"$addToSet":"$results.athlete_id"}}},

    {"$project":{
        "_id":1,
        "nb": {"$size":"$nb"}
    }}
])

results3 = collection1.aggregate([
    {"$unwind": "$results"},
    {"$group": {
        "_id": {
            "sport": "$results.sport",
            "event": "$results.event",
            "year": "$results.year"
        },
        "nb_athletes": {"$addToSet": "$_id"}  # Correction ici
    }},
    {"$project": {
        "_id": 1,
        "nb_athletes": {"$size": "$nb_athletes"}  # Correction ici
    }}
])


results4 = collection1.aggregate([
    {"$unwind": "$results"},
    {"$group": {
        "_id": {
            "sex": "$sex",
            "country": "$country",
        },
        "nb_athletes": {"$addToSet": "$_id"}  # Correction ici
    }},
    {"$project": {
        "_id": 1,
        "nb_athletes": {"$size": "$nb_athletes"}  # Correction ici
    }}
])


results5 = collection2.aggregate([
    {"$unwind": "$results"},
    {"$group": {
        "_id": {
            "discipline": "$discipline",
        },
        "time_held": {"$first":"$time_held"},
        "nb_editions": {"$addToSet": "$results.edition_id"}  # Correction ici
    }},
    {"$project": {
        "_id": 1,
        "time_held":1,
        "nb_editions": {"$size": "$nb_editions"}  # Correction ici
    }},{"$match":{"nb_editions":{"$lte":10}}}
])


results6 = collection1.aggregate([
    {"$unwind": "$results"},  # Décompose les résultats en plusieurs documents
    {"$match": {"results.medal": {"$ne": None}}},  # Filtrer les résultats avec une médaille
    {"$group": {
        "_id": "$_id",  # Grouper par ID de l'athlète
        "athlete": {"$first": "$name"},  # Garder le nom de l'athlète
        "nb_medals": {"$sum": 1}  # Compter le nombre de médailles
    }},
    {"$sort": {"nb_medals": -1}},  # Trier par nombre de médailles décroissant
    {"$limit": 1}  # Prendre le premier (l'athlète avec le plus de médailles)
])


results7 = collection1.aggregate([
    {"$unwind": "$results"},  # Étape 1 : Décomposer le tableau de résultats
    {"$match": {"results.medal": {"$ne": None}}},  # Étape 2 : Garder uniquement les médailles gagnées
    {"$group": {  # Étape 3 : Compter les médailles par athlète et par discipline
        "_id": {"discipline": "$results.discipline", "athlete_id": "$_id"},
        "athlete_name": {"$first": "$name"},
        "nb_medals": {"$sum": 1}
    }},
    {"$sort": {"_id.discipline": 1, "nb_medals": -1}},  # Étape 4 : Trier par discipline et nb de médailles décroissant
    {"$group": {  # Étape 5 : Regrouper par discipline et conserver les meilleurs athlètes
        "_id": "$_id.discipline",
        "max_medals": {"$first": "$nb_medals"},  # Stocker le max de médailles dans cette discipline
        "top_athletes": {
            "$push": {
                "athlete_id": "$_id.athlete_id",
                "athlete_name": "$athlete_name",
                "nb_medals": "$nb_medals"
            }
        }
    }},
    {"$addFields": {  # Étape 6 : Filtrer les athlètes ayant le max de médailles
        "top_athletes": {
            "$filter": {
                "input": "$top_athletes",
                "as": "athlete",
                "cond": {"$eq": ["$$athlete.nb_medals", "$max_medals"]}
            }
        }
    }},
    {"$project": {  # Étape 7 : Projeter les résultats finaux
        "_id": 1,
        "top_athletes": 1
    }}
])




print(results2)
for result in results7:
    print(result)

