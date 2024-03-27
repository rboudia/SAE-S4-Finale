

    f = open("../id/tournois_id.txt", "w")
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


@tournois_bp.route('/ajout_joueurs/<string:id_tournoi>/<string:id_joueur>')
def ajout_joueur(id_tournoi, id_joueur):
    collection_joueur = bd.get_collection("joueurs")
    collection_tournoi = bd.get_collection("tournois")

    tournoi = collection_tournoi.find_one({"_id": id_tournoi})
    joueur = collection_joueur.find_one({"_id": id_joueur})

    if not tournoi and not joueur:
        return "Le tournoi ou le joueur n'existe pas", 404
    else:

        joueurs_actuels = tournoi.get("Joueurs", [])

        if id_joueur not in joueurs_actuels:
            joueurs_actuels.append(id_joueur)

            filtre = {"_id": id_tournoi}
            nouvelles_valeurs = {"$set": {"Joueurs": joueurs_actuels}}
            collection_tournoi.update_one(filtre, nouvelles_valeurs)
            return "Modification effectuée", 200
        else:
            return "Le joueur est déjà inscrit dans ce tournoi", 400


@tournois_bp.route('/nb_inscrit/<string:id_tournoi>')
def affiche_nb_inscrit(id_tournoi):
    collection = bd.get_collection("tournois")
    tournoi = collection.find_one({"_id": id_tournoi})

    if not tournoi:
        return "Le tournoi n'existe pas", 404
    else:
        joueurs_inscrits = tournoi.get("Joueurs", [])
        nb_inscrits = len(joueurs_inscrits)

        return str(nb_inscrits), 200
