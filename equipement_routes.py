from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo

equipements_bp = Blueprint('equipements', __name__)

bd = Client2Mongo("rayan")

dernier_id = 3


@equipements_bp.route('/', methods=['POST'])
def insertion_tournoi():
    global dernier_id
    equipement = request.json
    collection = bd.get_collection("equipements")

    type = equipement.get("type").lower()

    dernier_id += 1

    doc = {"_id": str(dernier_id), "type": type, "statut": "Disponible"}
    collection.insert_one(doc)

    return "Equipement inséré avec succès", 201


@equipements_bp.route('/', methods=['GET'])
def affiche_equipements():
    collection = bd.get_collection("equipements")
    equipements = []
    for equipement in collection.find():
        equipements.append(equipement)
    return jsonify(equipements), 200


@equipements_bp.route('/<string:id>', methods=['GET'])
def affiche_equipement(id):
    collection = bd.get_collection("equipements")
    equipement = collection.find_one({"_id": id})

    if not equipement:
        return f"Aucun equipement n'a été trouvé avec cet id : {id}", 404
    else:
        return jsonify(equipement), 200


@equipements_bp.route('/<string:id>', methods=['DELETE'])
def suppresion_equipement(id):
    collection = bd.get_collection("equipements")
    equipement = collection.find_one({"_id": id})
    if equipement is None:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id}", 404
    else:
        collection.delete_one({"_id": id})
        return "Suppression de l'équipement effectuée avec succès", 200


@equipements_bp.route('/count/<string:type>', methods=['GET'])
def affiche_nb_equip(type):
    collection = bd.get_collection("equipements")
    nb_equipements = collection.count_documents({"type": type})

    return str(nb_equipements)

