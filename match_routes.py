from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo as Mongo


matchs_bp = Blueprint('matchs', __name__)

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
