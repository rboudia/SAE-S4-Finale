from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo

joueurs_bp = Blueprint('joueurs', __name__)

bd = Client2Mongo("rayan")


@joueurs_bp.route('/nbJoueurs', methods=['GET'])
def nombre_de_joueur():
    nb_joueurs = bd.bd["joueurs"].count_documents({})
    return jsonify(nb_joueurs)


@joueurs_bp.route('/', methods=['POST'])
def inserer_joueur():
    joueur = request.json
    collJoueur = bd.get_collection("joueurs")
    insertion = collJoueur.insert_one(joueur)
    return jsonify({"id": str(insertion.inserted_id)})


@joueurs_bp.route('/<string:nom>', methods=['GET'])
def chercher_joueur(nom):
    collection = bd.get_collection("joueurs")
    joueur = collection.find_one({"nom": nom})

    if joueur is None:
        return ("erreur")
    else:
        return jsonify(joueur)