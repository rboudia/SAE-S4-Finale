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
    collection = bd.get_collection("joueurs")

    nom = joueur.get("nom")
    prenom = joueur.get("prenom")
    age = joueur.get("age")
    niveau = joueur.get("niveau")

    f = open("id/joueurs_id.txt", "r")
    dernier_id = int(f.read()) + 1
    f.close()

    f = open("id/joueurs_id.txt", "w")
    f.write(str(dernier_id))
    f.close()

    doc = {"_id": str(dernier_id), "nom": nom, "prenom": prenom, "Categorie": {"age": str(age), "niveau": niveau}}
    collection.insert_one(doc)

    return "Joueur inséré avec succès", 201

@joueurs_bp.route('/insertion_fichier', methods=['POST'])
def inserer_joueurs():
    joueurs = request.json
    collection = bd.get_collection("joueurs")

    for joueur in joueurs:
        nom = joueur.get("nom")
        prenom = joueur.get("prenom")
        age = joueur.get("age")
        niveau = joueur.get("niveau")

        f = open("id/joueurs_id.txt", "r")
        dernier_id = int(f.read()) + 1
        f.close()

        f = open("id/joueurs_id.txt", "w")
        f.write(str(dernier_id))
        f.close()

        doc = {"_id": str(dernier_id), "nom": nom, "prenom": prenom, "Categorie": {"age": str(age), "niveau": niveau}}
        collection.insert_one(doc)

    return "Joueurs insérés avec succès", 201

@joueurs_bp.route('/<string:nom>', methods=['GET'])
def affiche_joueur(nom):
    collection = bd.get_collection("joueurs")
    joueur = collection.find_one({"nom": nom})

    if joueur is None:
        return f"Aucun joueur n'a été trouvé avec ce nom : {nom}", 404
    else:
        return jsonify(joueur), 200


@joueurs_bp.route('/', methods=['GET'])
def affiche_joueurs():
    collection = bd.get_collection("joueurs")
    joueurs = []
    for joueur in collection.find():
        joueurs.append(joueur)
    return jsonify(joueurs), 200


@joueurs_bp.route('/<string:id>', methods=['DELETE'])
def suppresion_joueur(id):
    collection = bd.get_collection("joueurs")
    joueur = collection.find_one({"_id": id})
    if joueur is None:
        return f"Aucun joueur n'a été trouvé avec cet id : {id}", 404
    else:
        collection.delete_one({"_id": id})
        return "Suppression du joueur effectuée avec succès", 200
