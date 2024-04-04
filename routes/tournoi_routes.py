from flask import Blueprint, jsonify, request
from Client2Mongo import Client2Mongo as Mongo
from Tournoi import Tournoi
from routes.equipement_routes import affiche_nb_equip, modif_statut_en_fonction_tournoi
from routes.match_routes import suppresion_matchs_tournois
from id.createur_id import creation_id
import random

tournois_bp = Blueprint('tournois', __name__)

# Ouverture de la connexion à la bd
bd = Mongo("rayan")


# Méthode qui permet l'insertion d'un tournoi dans la bd
@tournois_bp.route('/', methods=['POST'])
def insertion_tournoi():
    # Récupération des données envoyées via le formulaire
    tournoi = request.json

    # Récupération de la collection tournois de la bd
    collection = bd.get_collection("tournois")

    # Décomposition de la requête pour gérer l'insertion du tournoi
    nom = tournoi.get("nom")
    date = tournoi.get("date")
    format = tournoi.get("format")
    age_min = tournoi.get("ageMin")
    age_max = tournoi.get("ageMax")
    niveau = tournoi.get("niveau")

    # Creation d'un tournoi pour vérifier si les entrées sont bonnes
    t = Tournoi(nom, date, format, ((age_min, age_max), niveau))

    dernier_id = creation_id("tournois")

    # Création d'un document qui correspond aux champs de la collection tournois
    tournoi = {"_id": str(dernier_id), "nom": nom, "date": {"debut": date, "fin": date}, "format": format,
               "categories": {"age": str(age_min) + "-" + str(age_max), "niveau": niveau}, "status": "Prévu"}

    # Insertion du tournoi dans la collection tournois de la bd
    collection.insert_one(tournoi)

    return "Tournoi inséré avec succès", 201


@tournois_bp.route('/modif/<string:id_tournoi>/<string:nom_champ>/<string:ancienne_valeur>/<string:nouvelle_valeur>',
                   methods=['PATCH'])
def modif_tournoi(id_tournoi, nom_champ, ancienne_valeur, nouvelle_valeur):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id_tournoi})

    if not tournoi:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id_tournoi}", 404
    else:
        tournoi = collection.find_one({"_id": id_tournoi, nom_champ: ancienne_valeur})

        if not tournoi:
            return f"Aucun valeur a été trouvé pour le champ {nom_champ}", 404
        else:
            filtre = {nom_champ: ancienne_valeur}
            nouvelles_valeurs = {"$set": {nom_champ: nouvelle_valeur}}
            collection.update_one(filtre, nouvelles_valeurs)

            return "Modif avec succès", 200


# Méthode qui permet d'afficher tous les tournois contenu dans la bd
@tournois_bp.route('/', methods=['GET'])
def affiche_tournois():
    # Récupération de la collection tournois de la bd
    collection = bd.get_collection("tournois")

    # Création d'une liste pour stocker les documents de la requête find
    tournois = []

    # Ajout des documents dans la liste
    for tournoi in collection.find():
        tournois.append(tournoi)
    return jsonify(tournois), 200


# Méthode qui permet d'afficher un tournoi et qui prend en paramètre l'id du tournoi voulue
@tournois_bp.route('/<string:id_tournoi>', methods=['GET'])
def affiche_tournoi(id_tournoi):
    # Récupération de la collection tournois de la bd
    collection = bd.get_collection("tournois")

    # Requête qui permet de vérifier si le tournoi existe
    tournoi = collection.find_one({"_id": id_tournoi})

    if not tournoi:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id_tournoi}", 404
    else:
        return jsonify(tournoi), 200


# Méthode qui permet de supprimer un tournoi et qui prend en paramètre l'id du tournoi qu'on souhaite supprimer
@tournois_bp.route('/<string:id_tournoi>', methods=['DELETE'])
def suppresion_tournoi(id_tournoi):
    # Récupération de la collection tournois de la bd
    collection = bd.get_collection("tournois")

    # Requête qui permet de vérifier si le tournoi existe
    tournoi = collection.find_one({"_id": id_tournoi})

    if tournoi is None:
        return f"Aucun tournoi n'a été trouvé avec cet id : {id_tournoi}", 404
    else:

        # Suppression dans la collection tournois
        collection.delete_one({"_id": id_tournoi})

        # Suppression des matchs du tournoi dans la collection matchs
        suppresion_matchs_tournois(tournoi.get("nom"))

        # Modification de la disponibilité des équipements dans la collection équipements
        modif_statut_en_fonction_tournoi(id_tournoi)

        return "Suppression du tournoi effectuée avec succès", 200


# Méthode qui permet d'inscrire un joueur à un tournoi et qui prend en paramètre l'id du joueur à ajouté et l'id du
# tournoi dans lequel on ajoute le joueur
@tournois_bp.route('/ajout_joueurs/<string:id_tournoi>/<string:id_joueur>', methods=['PATCH'])
def ajout_joueur(id_tournoi, id_joueur):
    # Récupération de la collection joueurs de la bd
    collection_joueur = bd.get_collection("joueurs")

    # Récupération de la collection tournois de la bd
    collection_tournoi = bd.get_collection("tournois")

    # Requête qui permet de vérifier si le tournoi existe
    tournoi = collection_tournoi.find_one({"_id": id_tournoi})

    # Requête qui permet de vérifier si le joueur existe
    joueur = collection_joueur.find_one({"_id": id_joueur})

    if not tournoi:
        return "Le tournoi n'existe pas", 404
    elif not joueur:
        return "Le joueur n'existe pas", 404

    else:

        # Récupération de la liste des joueurs qui sont déjà inscrit au tournoi
        joueurs_actuels = tournoi.get("Joueurs", [])

        if len(joueurs_actuels) >= 8:
            return "Nombre maximal de joueurs atteint pour ce tournoi", 456

        id_joueur_present = any(joueur.get("_id") == id_joueur for joueur in joueurs_actuels)
        if id_joueur_present:
            return "Le joueur est déja inscrit à ce tournoi.", 458
        else:

            # Récupération du niveau requis pour s'incrire au tournoi
            niveau_tournoi = tournoi.get("categories", {}).get("niveau")

            # Récupération du niveau du joueur
            niveau_joueur = joueur.get("Categorie", {}).get("niveau")

            # Récupération du de l'age requis pour s'incrire au tournoi
            age_tournoi = str(tournoi.get("categories", {}).get("age"))
            age_min, age_max = age_tournoi.split("-")

            # Récupération de l'âge du joueur
            age_joueur = int(joueur.get("Categorie", {}).get("age"))

            if niveau_joueur == niveau_tournoi and int(age_min) <= age_joueur <= int(age_max):
                nom = joueur.get("nom")
                prenom = joueur.get("prenom")
                joueurs_actuels.append({"_id": id_joueur, "nom": nom, "prenom": prenom})

                filtre = {"_id": id_tournoi}
                nouvelles_valeurs = {"$set": {"Joueurs": joueurs_actuels}}
                collection_tournoi.update_one(filtre, nouvelles_valeurs)
                return "Le joueur a bien été inscrit", 200
            else:
                return "Le joueur ne correspond pas aux critères d'âge ou de niveau du tournoi", 450


@tournois_bp.route('/retirer_joueur/<string:id_tournoi>/<string:id_joueur>', methods=['DELETE'])
def retirer_joueur(id_tournoi, id_joueur):
    collection_tournoi = bd.get_collection("tournois")

    tournoi = collection_tournoi.find_one({"_id": id_tournoi})

    if not tournoi:
        return "Le tournoi n'existe pas", 404

    joueurs_actuels = tournoi.get("Joueurs", [])

    if id_joueur in joueurs_actuels:
        joueurs_actuels.remove(id_joueur)

        filtre = {"_id": id_tournoi}
        nouvelles_valeurs = {"$set": {"Joueurs": joueurs_actuels}}
        collection_tournoi.update_one(filtre, nouvelles_valeurs)
        return "Le joueur a bien été retiré du tournoi", 200
    else:
        return "Le joueur n'est pas inscrit dans ce tournoi", 404


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


@tournois_bp.route('/creer_match/<string:id_tournoi>', methods=['PATCH'])
def creation_match_tournois(id_tournoi):
    collection_tournoi = bd.get_collection("tournois")
    collection_match = bd.get_collection("matchs")
    collection_equipement = bd.get_collection("equipements")

    tournoi = collection_tournoi.find_one({"_id": id_tournoi})

    if not tournoi:
        return "Le tournoi n'existe pas", 404

    nb_inscrit = int(affiche_nb_inscrit(id_tournoi)[0])
    nb_balle, nb_table, nb_raquette = [int(affiche_nb_equip(equip)[0]) for equip in ["balle", "table", "raquette"]]

    if nb_inscrit < 4:
        return "Pas assez de joueurs pour créer des matchs", 451
    elif nb_inscrit > 8:
        return "Trop de joueurs pour créer des matchs", 452
    elif nb_inscrit % 2 != 0:
        return "Le nombre de participant doit être pair pour pouvoir créer les matchs", 439
    elif nb_balle < 2:
        return "Le nombre de balle est insufisant pour pouvoir créer les matchs", 469
    elif nb_table < 2:
        return "Le nombre de table est insufisant pour pouvoir créer les matchs", 459
    elif nb_raquette < 4:
        return "Le nombre de raquette est insufisant pour pouvoir créer les matchs", 489
    else:
        cond_balle = {"type": "balle", "statut": "Disponible"}
        cond_table = {"type": "table", "statut": "Disponible"}
        cond_raquette = {"type": "raquette", "statut": "Disponible"}

        result_balle = collection_equipement.find(cond_balle).limit(2)
        result_table = collection_equipement.find(cond_table).limit(2)
        result_raquette = collection_equipement.find(cond_raquette).limit(4)

        for doc in result_balle:
            collection_equipement.update_one({"_id": doc["_id"]},
                                             {"$set": {"statut": "Occupé", "idTournoi": id_tournoi}})

        liste = list(result_table)

        for doc in liste:
            collection_equipement.update_one({"_id": doc["_id"]},
                                             {"$set": {"statut": "Occupé", "idTournoi": id_tournoi}})

        for doc in result_raquette:
            collection_equipement.update_one({"_id": doc["_id"]},
                                             {"$set": {"statut": "Occupé", "idTournoi": id_tournoi}})

        joueurs_actuels = tournoi.get("Joueurs", [])
        random.shuffle(joueurs_actuels)

        paires_matchs = []
        for i in range(0, len(joueurs_actuels), 2):
            if i + 1 < len(joueurs_actuels):
                paires_matchs.append((joueurs_actuels[i], joueurs_actuels[i + 1]))

        a = 0

        for paire in paires_matchs:
            joueur_1 = paire[0]
            joueur_2 = paire[1]

            dernier_id = creation_id("matchs")

            doc = {"_id": str(dernier_id), "nomTournoi": tournoi.get("nom"), "phase": "Phase de poule",
                   "format": "Simple", "joueurs": [joueur_1, joueur_2], "scores": "0-0",
                   "idTable": liste[a].get("_id"), "statut": "Prévu"}
            collection_match.insert_one(doc)
            a += 1

            if a == 2:
                a = 0

        return "Les matchs ont été créer", 200
