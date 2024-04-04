from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo
from id.createur_id import creation_id

equipements_bp = Blueprint('equipements', __name__)

# Ouverture de la connexion à la bd
bd = Client2Mongo("rayan")

"""
Méthode qui permet d'insérer un équipement dans la collection equipement. 
Prend un nombre d'équipement dans sa route pour en insérer x d'un coup.
"""
@equipements_bp.route('/<string:nb_equip>', methods=['POST'])
def insertion_equipement(nb_equip: str):
    #Récupération des données envoyées via le formulaire.
    equipement = request.json

    #Récupération de la collection equipements.
    collection = bd.get_collection("equipements")
    #Permet de mettre le type saisi en minuscule pour gérer les entrées utilisateurs.
    type = equipement.get("type").lower()

    #Boucle pour insérer les équipements en fonction de leur quantité et les rendant disponible.
    for i in range(int(nb_equip)):
        dernier_id = creation_id("equipements")

        doc = {"_id": str(dernier_id), "type": type, "statut": "Disponible", "idTournoi": "Aucun"}
        collection.insert_one(doc)

    return "Equipement inséré avec succès", 201

#Méthode qui permets d'afficher la liste de tous les équipements.
@equipements_bp.route('/', methods=['GET'])
def affiche_equipements():
    #Récupération de la collection equipements.
    collection = bd.get_collection("equipements")
    equipements = []
    #Boucle qui permet de retourner les equipements trouver dans la collection.
    for equipement in collection.find():
        equipements.append(equipement)
    return jsonify(equipements), 200

#Méthode qui permet de supprimer un équipement de la collection par son id
@equipements_bp.route('/<string:id>', methods=['DELETE'])
def suppresion_equipement(id: str):
    #Récupération de la collection equipements.
    collection = bd.get_collection("equipements")

    #Vérifie si l'équipement sélectionné est disponible.
    equipement = collection.find_one({"_id": id, "statut": "Disponible"})
    if equipement is None:
        return "Cette équipement est déja utilisée", 404
    else:
        collection.delete_one({"_id": id})
        return "Suppression de l'équipement effectuée avec succès", 200

#Méthode qui permet d'afficher la quantité d'un équipement en fonction de son type.
def affiche_nb_equip(type: str):
    #Récupération de la collection equipements.
    collection = bd.get_collection("equipements")
    #Récupère le nombre d'équipement disponible du type choisi.
    nb_equipements = collection.count_documents({"type": type, "statut": "Disponible"})

    #Gère le retour, si il n'y a aucun équipement du type associé ou sinon affiche le résultat.
    if nb_equipements == 0:
        return f"Aucun equipement disponible n'a été trouvé avec ce type : {type}"
    else:
        return str(nb_equipements)

#Méthode qui permet de mettre  à jour le statut d'occupation d'un équipement en fonction de son utilisation par un match.
def modif_statut_en_fonction_tournoi(id_tournoi: str):
    #Récupération de la collection equipements.
    collection = bd.get_collection("equipements")
    #Récupère l'id tournoi en paramètre.
    equipement = collection.find_one({"idTournoi": id_tournoi})

    #Condition pour gérer si l'équipement n'est associé à aucun tournoi, le cas échant il modifie son statut et son idtournoi associé.
    if not equipement:
        return f"Aucun equipement n'a été trouvé avec comme idTournoi : {id_tournoi}"
    else:
        collection.update_many({"statut": "Occupé", "idTournoi": id_tournoi}, {"$set": {"statut": "Disponible",
                                                                                        "idTournoi": "Aucun"}})
        return "Modification du statut effectuée"

