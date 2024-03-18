from flask import Blueprint
from pymongo import MongoClient

collections_bp = Blueprint('collections', __name__)


class Client2Mongo:
    def __init__(self, nom_bd):
        self.client = MongoClient()
        self.bd = self.client[nom_bd]

    def liste_des_collections(self):
        return self.bd.list_collection_names()

    def get_collection(self, coll):
        return self.bd[coll]

    def find_one(self, collection_name):
        return self.bd[collection_name].find_one()

    def find(self, collection_name):
        return self.bd[collection_name].find()

    def insertion_tournoi(self, tournoi):
        tournois = self.get_collection("tournois")

        nom = tournoi.nom
        date = tournoi.date
        format = tournoi.format
        age = tournoi.categorie[0]
        niveau = tournoi.categorie[1]

        doc = {"nom": nom, "date": {"debut": date, "fin": date}, "format": format,
               "categorie": {"age": str(age[0])+"-"+str(age[1]), "niveau": niveau}, "status": "Prevu"}
        tournois.insert_one(doc)

    def modif_tournoi(self, old_nom_tourn, new_nom_tourn):
        tournois = self.get_collection("tournois")
        tournoi = tournois.find_one({"nom": old_nom_tourn})

        if tournoi is None:
            print("Aucun tournoi n'a été trouvé avec ce nom : ", old_nom_tourn)
        else:
            filtre = {"nom": old_nom_tourn}
            nouvelles_valeurs = {"$set": {"nom": new_nom_tourn}}
            tournois.update_one(filtre, nouvelles_valeurs)

    def affiche_tournois(self):
        tournois = self.get_collection("tournois")
        for tournoi in tournois.find():
            print(tournoi)

    def affiche_tournoi(self, nom_tournoi):
        tournois = self.get_collection("tournois")
        tournoi = tournois.find_one({"nom": nom_tournoi})

        if tournoi is None:
            print("Aucun tournoi n'a été trouvé avec ce nom : ", nom_tournoi)
        else:
            print(tournoi)

    def suppresion_tournoi(self, nom_tournoi):
        tournois = self.get_collection("tournois")
        tournoi = tournois.find_one({"nom": nom_tournoi})
        if tournoi is None:
            print("Aucun tournoi n'a été trouvé avec ce nom : ", nom_tournoi)
        else:
            print("Supression du tournoi : ", nom_tournoi)
            tournois.delete_one({"nom": nom_tournoi})
