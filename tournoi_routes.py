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


@tournois_bp.route('/<string:id>', methods=['GET'])
def affiche_tournoi(id):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id})

    if not tournoi:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id}", 404
    else:
        return jsonify(tournoi), 200


@tournois_bp.route('/<string:id>', methods=['DELETE'])
def suppresion_tournoi(id):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id})
    if tournoi is None:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id}", 404
    else:
        collection.delete_one({"_id": id})
        return "Suppression du tournoi effectuée avec succès", 200
