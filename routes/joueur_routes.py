from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo
from id.createur_id import creation_id

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

    dernier_id = creation_id("joueurs")

    # Création d'un document qui correspond aux champs de la collection joueurs
    joueur = {"_id": str(dernier_id), "nom": nom, "prenom": prenom, "Categorie": {"age": str(age), "niveau": niveau}}

    # Insertion du joueur dans la collection joueurs de la bd
    collection.insert_one(joueur)

    return "Joueur inséré avec succès", 201


# Méthode qui permet l'insertion de joueurs dans la bd en fonction d'un fichier json
@joueurs_bp.route('/insertion_fichier', methods=['POST'])
def inserer_joueurs():

    # Récupération du fichier envoyé
    joueurs = request.json

    # Récupération de la collection joueurs de la bd
    collection = bd.get_collection("joueurs")

    for joueur in joueurs:

        # Décomposition de joueur pour son insertion
        nom = joueur.get("nom")
        prenom = joueur.get("prenom")
        age = joueur.get("age")
        niveau = joueur.get("niveau")

        dernier_id = creation_id("joueurs")

        # Création d'un document qui correspond aux champs de la collection joueurs
        joueur = {"_id": str(dernier_id), "nom": nom, "prenom": prenom, "Categorie": {"age": str(age), "niveau": niveau}}

        # Insertion du joueur dans la collection joueurs de la bd
        collection.insert_one(joueur)

    return "Joueurs insérés avec succès", 201


# Méthode qui permet d'afficher un joueur et qui prend en paramètre le nom du joueur chercher
@joueurs_bp.route('/<string:nom>', methods=['GET'])
def affiche_joueur(nom):

    # Récupération de la collection joueurs de la bd
    collection = bd.get_collection("joueurs")

    # Requête qui permet de vérifier si le joueur existe
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
