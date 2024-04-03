from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo

joueurs_bp = Blueprint('joueurs', __name__)

# Ouverture de la connexion à la bd
bd = Client2Mongo("rayan")


# Méthode qui permet l'insertion d'un joueur dans la bd
@joueurs_bp.route('/', methods=['POST'])
def inserer_joueur():

    # Récupération des données envoyées via le formulaire
    joueur = request.json

    # Récupération de la collection joueurs de la bd
    collection = bd.get_collection("joueurs")

    # Décomposition de la requête pour gérer l'insertion du joueur
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

    # Création d'un document qui correspond aux champs de la collection joueurs
    joueur = {"_id": str(dernier_id), "nom": nom, "prenom": prenom, "Categorie": {"age": str(age), "niveau": niveau}}

    # Insertion du tournoi dans la collection joueurs de la bd
    collection.insert_one(joueur)

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
def suppression_joueur(id):
    collection_joueur = bd.get_collection("joueurs")
    collection_tournoi = bd.get_collection("tournois")

    joueur = collection_joueur.find_one({"_id": id})
    if joueur is None:
        return f"Aucun joueur n'a été trouvé avec cet id : {id}", 404

    if collection_tournoi.count_documents({"Joueurs._id": id}) > 0:
        return "Le joueur est inscrit à au moins un tournoi. Impossible de le supprimer.", 400

    collection_joueur.delete_one({"_id": id})
    return "Suppression du joueur effectuée avec succès", 200
