from flask import Blueprint, jsonify
from Client2Mongo import Client2Mongo as Mongo


matchs_bp = Blueprint('matchs', __name__)

# Ouverture de la connexion à la bd
bd = Mongo("MyTennisPlan")


# Méthode qui permet d'afficher les matchs d'un tournoi et qui prend en paramètre le nom du tournoi souhaité
@matchs_bp.route('/tournoi/<string:nom_tournoi>', methods=['GET'])
def affiche_matchs_tournoi(nom_tournoi: str):

    # Récupération de la collection matchs de la bd
    collection = bd.get_collection("matchs")

    # Requête qui permet de vérifier si au moins un match existe pour le nom de tournoi donné
    match = collection.find_one({"nomTournoi": nom_tournoi})

    if not match:
        return f"Aucun match n'est en cours pour le tournoi : {nom_tournoi}", 404
    else:

        # Création d'une liste pour stocker les documents de la requête find
        matchs_tournoi = []

        # Ajout des documents dans la liste
        for match in collection.find({"nomTournoi": nom_tournoi}):
            matchs_tournoi.append(match)

        return jsonify(matchs_tournoi), 200


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
