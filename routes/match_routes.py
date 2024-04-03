from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo as Mongo


matchs_bp = Blueprint('matchs', __name__)

# Ouverture de la connexion à la bd
bd = Mongo("rayan")


@matchs_bp.route('/', methods=['GET'])
def affiche_matchs():
    collection = bd.get_collection("matchs")
    matchs = []
    for match in collection.find():
        matchs.append(match)
    return jsonify(matchs), 200


@matchs_bp.route('/<string:id>', methods=['GET'])
def affiche_match(id):
    collection = bd.get_collection("matchs")
    match = collection.find_one({"_id": id})

    if not match:
        return f"Aucun match n'a été trouvé avec cet id : {id}", 404
    else:
        return jsonify(match), 200


@matchs_bp.route('/tournoi/<string:nom_tournoi>', methods=['GET'])
def affiche_matchs_tournoi(nom_tournoi):
    collection = bd.get_collection("matchs")
    match = collection.find_one({"nomTournoi": nom_tournoi})

    if not match:
        return f"Aucun match n'est en cours pour le tournoi : {nom_tournoi}", 404
    else:
        matchs_tournoi = []
        for match in collection.find({"nomTournoi": nom_tournoi}):
            matchs_tournoi.append(match)

        return jsonify(matchs_tournoi), 200


def suppresion_matchs_tournois(nom_tournoi):
    collection = bd.get_collection("matchs")
    match = collection.find_one({"nomTournoi": nom_tournoi})
    if not match:
        return f"Aucun match n'est en cours pour le tournoi : {nom_tournoi}"
    else:
        collection.delete_many({"nomTournoi": nom_tournoi})
        return "La suppression a été effectuée", 200
