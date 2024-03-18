from pymongo import MongoClient
import Creation_tournoi as crea

class BD:
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client.rayan

    def insertion_tournoi(self, tournoi):
        tournois = self.database.tournois

        nom = tournoi.nom
        date = tournoi.date
        format = tournoi.format
        age = tournoi.categorie[0]
        niveau = tournoi.categorie[1]

        doc = {"nom": nom, "date": {"debut": date, "fin": date}, "format": format,
               "categorie": {"age": age, "niveau": niveau}, "status":"Prevu"}
        tournois.insert_one(doc)
        
    def ajout_joueurs_tournoi(self):
        pass


tournoi = crea.creation_tournoi()

base_donne = BD()
base_donne.insertion_tournoi(tournoi)
