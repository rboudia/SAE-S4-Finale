from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo as Mongo
from Tournoi import Tournoi

tournois_bp = Blueprint('tournois', __name__)

bd = Mongo("rayan")


@tournois_bp.route('/', methods=['POST'])
def insertion_tournoi():
    tournoi = request.json
    collection = bd.get_collection("tournois")

    nom = tournoi.get("nom")
    date = tournoi.get("date")
    format = tournoi.get("format")
    age_min = tournoi.get("ageMin")
    age_max = tournoi.get("ageMax")
    niveau = tournoi.get("niveau")

    # Creation d'un tournoi pour vérifier si les entrées sont bonnes
    t = Tournoi(nom, date, format, ((age_min, age_max), niveau))

    f = open("id/tournois_id.txt", "r")
    dernier_id = int(f.read()) + 1
    f.close()

    f = open("id/tournois_id.txt", "w")
    f.write(str(dernier_id))
    f.close()

    doc = {"_id": str(dernier_id), "nom": nom, "date": {"debut": date, "fin": date}, "format": format,
           "categories": {"age": str(age_min) + "-" + str(age_max), "niveau": niveau}, "status": "Prévu"}
    collection.insert_one(doc)

    return "Tournoi inséré avec succès", 201


def modif_tournoi(old_nom_tourn: str, new_nom_tourn: str):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"nom": old_nom_tourn})

    if tournoi is None:
        print("Aucun tournoi n'a été trouvé avec ce nom : ", old_nom_tourn)
    else:
        filtre = {"nom": old_nom_tourn}
        nouvelles_valeurs = {"$set": {"nom": new_nom_tourn}}
        collection.update_one(filtre, nouvelles_valeurs)


@tournois_bp.route('/', methods=['GET'])
def affiche_tournois():
    collection = bd.get_collection("tournois")
    tournois = []
    for tournoi in collection.find():
        tournois.append(tournoi)
    return jsonify(tournois)


@tournois_bp.route('/<string:id_tournoi>', methods=['GET'])
def affiche_tournoi(id_tournoi):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id_tournoi})

    if not tournoi:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id_tournoi}", 404
    else:
        return jsonify(tournoi), 200


@tournois_bp.route('/<string:id_tournoi>', methods=['DELETE'])
def suppresion_tournoi(id_tournoi):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id_tournoi})
    if tournoi is None:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id_tournoi}", 404
    else:
        collection.delete_one({"_id": id_tournoi})
        return "Suppression du tournoi effectuée avec succès", 200


@tournois_bp.route('/ajout_joueurs/<string:id_tournoi>/<string:id_joueur>', methods=['PATCH'])
def ajout_joueur(id_tournoi, id_joueur):
    collection_joueur = bd.get_collection("joueurs")
    collection_tournoi = bd.get_collection("tournois")

    tournoi = collection_tournoi.find_one({"_id": id_tournoi})
    joueur = collection_joueur.find_one({"_id": id_joueur})

    if not tournoi:
        return "Le tournoi n'existe pas", 404
    elif not joueur:
        return "Le joueur n'existe pas", 404

    else:

        joueurs_actuels = tournoi.get("Joueurs", [])

        if id_joueur not in joueurs_actuels:

            niveau_tournoi = tournoi.get("categories", {}).get("niveau")
            niveau_joueur = joueur.get("Categorie", {}).get("niveau")

            age_tournoi = str(tournoi.get("categories", {}).get("age"))
            age_min, age_max = age_tournoi.split("-")
            age_joueur = int(joueur.get("Categorie", {}).get("age"))

            if niveau_joueur == niveau_tournoi and int(age_min) <= age_joueur <= int(age_max):
                joueurs_actuels.append(id_joueur)

                filtre = {"_id": id_tournoi}
                nouvelles_valeurs = {"$set": {"Joueurs": joueurs_actuels}}
                collection_tournoi.update_one(filtre, nouvelles_valeurs)
                return "Le joueur a bien été inscrit", 200
            else:
                return "Le joueur ne correspond pas aux critères d'âge ou de niveau du tournoi", 450
        else:
            return "Le joueur est déjà inscrit dans ce tournoi", 455


@tournois_bp.route('/nb_inscrit/<string:id_tournoi>', methods=['GET'])
def affiche_nb_inscrit(id_tournoi):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id_tournoi})

    if not tournoi:
        return "Le tournoi n'existe pas", 404
    else:
        joueurs_inscrits = tournoi.get("Joueurs", [])
        nb_inscrits = len(joueurs_inscrits)

        return str(nb_inscrits), 200


@tournois_bp.route('/creer_match/<string:id_tournoi>')
def creation_match_tournois(id_tournoi):
    collection_tournoi = bd.get_collection("tournois")
    collection_joueur = bd.get_collection("joueurs")
    collection_match = bd.get_collection("matchs")

    tournoi = collection_tournoi.find_one({"_id": id_tournoi})

    if not tournoi:
        return "Le tournoi n'existe pas", 404

    nb_inscrit = int(affiche_nb_inscrit(id_tournoi)[0])

    if nb_inscrit < 4:
        return "Pas assez de joueurs pour créer des matchs", 404
    elif nb_inscrit % 2 != 0:
        return "Le nombre de participant doit être pair pour pouvoir créer les matchs", 409
    else:
        return "Le nombre de participant est bon", 200
