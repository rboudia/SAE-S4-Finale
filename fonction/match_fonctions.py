"""
Fichier qui contient des fonctions relatives à la collection matchs et qui permet d'alléger le code
"""

from Client2Mongo import Client2Mongo


# Ouverture de la connexion à la bd
bd = Client2Mongo("MyTennisPlan")


# Méthode qui est utilisée dans tournoi_routes et qui permet de supprimer les matchs d'un tournoi
def suppresion_matchs_tournois(nom_tournoi: str):

    # Récupération de la collection matchs de la bd
    collection = bd.get_collection("matchs")

    # Requête qui permet de vérifier si au moins un match existe pour le nom de tournoi donné
    match = collection.find_one({"nomTournoi": nom_tournoi})

    if not match:
        return f"Aucun match n'est en cours pour le tournoi : {nom_tournoi}"
    else:

        # Suppression des matchs associés au tournoi
        collection.delete_many({"nomTournoi": nom_tournoi})


# Méthode qui permet de modifier le nom du tournoi dans les matchs quand le nom du tournoi est modifié
def modif_nom_tournoi(ancien_nom_tournoi, nouveau_nom_tournoi):
    collection = bd.get_collection("matchs")

    match = collection.find_one({"nomTournoi": ancien_nom_tournoi})

    if not match:
        return "Aucun match n'a été trouvé pour ce tournoi"
    else:

        filtre = {"nomTournoi": ancien_nom_tournoi}
        nouvelle_valeur = {"$set": {"nomTournoi": nouveau_nom_tournoi}}
        collection.update_many(filtre, nouvelle_valeur)