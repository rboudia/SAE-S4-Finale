from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo
from id.createur_id import creation_id
from classe.joueur import Joueur

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
    nom, prenom, age, niveau = (joueur.get(attribut) for attribut in ["nom", "prenom", "age", "niveau"])

    # Creation d'un joueur pour vérifier si les entrées sont bonnes
    test_joueur = Joueur(nom, prenom, age, niveau)

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
        nom, prenom, age, niveau = (joueur.get(attribut) for attribut in ["nom", "prenom", "age", "niveau"])

        # Creation d'un joueur pour vérifier si les entrées sont bonnes
        test_joueur = Joueur(nom, prenom, age, niveau)

        dernier_id = creation_id("joueurs")

        # Création d'un document qui correspond aux champs de la collection joueurs
        joueur = {"_id": str(dernier_id), "nom": nom, "prenom": prenom,
                  "Categorie": {"age": str(age), "niveau": niveau}}

        # Insertion du joueur dans la collection joueurs de la bd
        collection.insert_one(joueur)

    return "Joueurs insérés avec succès", 201


# Méthode qui permet d'afficher un joueur et qui prend en paramètre le nom du joueur chercher
@joueurs_bp.route('/<string:nom>', methods=['GET'])
def affiche_joueur(nom: str):
    # Récupération de la collection joueurs de la bd
    collection = bd.get_collection("joueurs")

    # Requête qui permet de vérifier si le joueur existe
    joueur = collection.find_one({"nom": nom})

    if joueur is None:
        return f"Aucun joueur n'a été trouvé avec ce nom : {nom}", 404
    else:
        return jsonify(joueur), 200


# Méthode qui permet d'afficher la liste de tous les joueurs
@joueurs_bp.route('/', methods=['GET'])
def affiche_joueurs():
    # Récupération de la collection joueurs.
    collection = bd.get_collection("joueurs")
    joueurs = []

    # Boucle pour itérer sur la collection et retourner tous les joueurs existant.
    for joueur in collection.find():
        joueurs.append(joueur)

    return jsonify(joueurs), 200


# Méthode qui permet de supprimer un joueur de la collection par son id
@joueurs_bp.route('/<string:id>', methods=['DELETE'])
def suppression_joueur(id: str):
    # Récupération de la collection joueurs.
    collection_joueur = bd.get_collection("joueurs")

    # Récupération de la collection tournois.
    collection_tournoi = bd.get_collection("tournois")

    # Récupération du joueur avec l'id correspondant.
    joueur = collection_joueur.find_one({"_id": id})

    # Gère le cas où le joueur n'existe pas.
    if joueur is None:
        return f"Aucun joueur n'a été trouvé avec cet id : {id}", 404

    # Vérifie si le joueur est inscrit à un tournoi, ce qui empêchera sa suppression.
    if collection_tournoi.count_documents({"Joueurs._id": id}) > 0:
        return "Le joueur est inscrit à au moins un tournoi. Impossible de le supprimer.", 400

    # Supprime le joueur si les conditions précédentes ne sont pas vérifiées.
    collection_joueur.delete_one({"_id": id})

    return "Suppression du joueur effectuée avec succès", 200
