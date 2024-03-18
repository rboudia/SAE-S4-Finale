from pymongo import MongoClient
import Creation_tournoi as crea


class BD:
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client.rayan
        self.collections = [self.database.tournois]

    def insertion_tournoi(self, tournoi):
        tournois = self.collections[0]

        nom = tournoi.nom
        date = tournoi.date
        format = tournoi.format
        age = tournoi.categorie[0]
        niveau = tournoi.categorie[1]

        doc = {"nom": nom, "date": {"debut": date, "fin": date}, "format": format,
               "categorie": {"age": age, "niveau": niveau}, "status": "Prevu"}
        tournois.insert_one(doc)

    def modif_tournoi(self, old_nom_tourn, new_nom_tourn):
        tournois = self.collections[0]
        filtre = {"nom": old_nom_tourn}
        nouvelles_valeurs = {"$set": {"nom": new_nom_tourn}}
        tournois.update_one(filtre, nouvelles_valeurs)

    def affiche_tournoi(self):
        tournois = self.collections[0]
        for tournoi in tournois.find():
            print(tournoi)

    def suppresion_tournoi(self, nom_tournoi):
        tournois = self.collections[0]
        tournois.delete_one({"nom": nom_tournoi})


tournoi = crea.creation_tournoi()

base_donne = BD()
# base_donne.affiche_tournoi()
# base_donne.modif_tournoi("Test1", "Nouveau Test 1")
# base_donne.affiche_tournoi()
base_donne.insertion_tournoi(tournoi)
# base_donne.suppresion_tournoi("Test")
