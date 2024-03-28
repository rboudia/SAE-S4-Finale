from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo

equipements_bp = Blueprint('equipements', __name__)

bd = Client2Mongo("rayan")


@equipements_bp.route('/<string:nb_equip>', methods=['POST'])
def insertion_equipement(nb_equip):
    equipement = request.json
    collection = bd.get_collection("equipements")

    type = equipement.get("type").lower()
    for i in range(int(nb_equip)):

        f = open("id/equipements_id.txt", "r")
        dernier_id = int(f.read()) + 1
        f.close()

        f = open("id/equipements_id.txt", "w")
        f.write(str(dernier_id))
        f.close()

        doc = {"_id": str(dernier_id), "type": type, "statut": "Disponible", "idTournoi": "Aucun"}
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
    equipement = collection.find_one({"_id": id, "statut": "Disponible"})
    if equipement is None:
        return "Cette équipement est déja utilisée", 404
    else:
        collection.delete_one({"_id": id})
        return "Suppression de l'équipement effectuée avec succès", 200


@equipements_bp.route('/count/<string:type>', methods=['GET'])
def affiche_nb_equip(type):
    collection = bd.get_collection("equipements")
    nb_equipements = collection.count_documents({"type": type, "statut": "Disponible"})

    if nb_equipements == 0:
        return f"Aucun equipement disponible n'a été trouvé avec ce type : {type}", 404
    else:
        return str(nb_equipements)


@equipements_bp.route('/type/<string:type>', methods=['GET'])
def affiche_equipement_type(type):
    collection = bd.get_collection("equipements")
    equipement = collection.find_one({"type": type})

    if not equipement:
        return f"Aucun equipement n'a été trouvé avec ce type : {type}", 404
    else:
        equipements = []
        for equipement in collection.find({"type": type}):
            equipements.append(equipement)
        return jsonify(equipements), 200



def modif_statut_en_fonction_tournoi(id_tournoi):
    collection = bd.get_collection("equipements")
    equipement = collection.find_one({"idTournoi": id_tournoi})

    if not equipement:
        return f"Aucun equipement n'a été trouvé avec comme idTournoi : {id_tournoi}"
    else:
        collection.update_many({"statut": "Occupé", "idTournoi": id_tournoi}, {"$set": {"statut": "Disponible",
                                                                                        "idTournoi": "Aucun"}})
        return "Modification du statut effectuée"

