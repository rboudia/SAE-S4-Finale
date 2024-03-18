from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.rayan


collections = db.list_collection_names()


for collection in collections:
    print(collection)


joueurs = db.joueurs


docTest = {
    "_id": "TEST", "titre": "Test"
    }

resultat = joueurs.find_one({}, {"Categorie.age": True})
print(resultat)
# departements.insert_one(docTest)
# departements.delete_one({"titre":"Test"})

if resultat:
    age = resultat["Categorie"]["age"]
    print("L'âge du joueur est:", age)
else:
    print("Aucun joueur trouvé.")

test = joueurs.find_one({"nom": "boudia"})
print(test)

ok = test["nom"]
print(ok)

j1 = {
      "_id": "1", "nom": "Jou1", "prenom": "jj1", "Categorie": {
          "age": "10",
          "niveau": "Débutant"
          }
      }
