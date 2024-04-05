"""
Fichier qui contient des fonctions relatives à la collection equipements et qui permet d'alléger le code
"""

from Client2Mongo import Client2Mongo

# Ouverture de la connexion à la bd
bd = Client2Mongo("MyTennisPlan")


# Méthode qui permet d'afficher la quantité d'un équipement en fonction de son type.
def affiche_nb_equip(type: str):
    # Récupération de la collection equipements.
    collection = bd.get_collection("equipements")
    # Récupère le nombre d'équipement disponible du type choisi.
    nb_equipements = collection.count_documents({"type": type, "statut": "Disponible"})

    # Gère le retour, si il n'y a aucun équipement du type associé ou sinon affiche le résultat.
    if nb_equipements == 0:
        return f"Aucun equipement disponible n'a été trouvé avec ce type : {type}"
    else:
        return str(nb_equipements)


"""
Méthode qui permet de mettre  à jour le statut d'occupation d'un équipement en fonction 
de son utilisation par un match.
"""


def modif_statut_en_fonction_tournoi(id_tournoi: str):
    # Récupération de la collection equipements.
    collection = bd.get_collection("equipements")

    # Récupère l'id tournoi en paramètre.
    equipement = collection.find_one({"idTournoi": id_tournoi})

    """
    Condition pour gérer si l'équipement n'est associé à aucun tournoi, le cas échant il modifie son statut 
    et son idtournoi associé.
    """

    if not equipement:
        return f"Aucun equipement n'a été trouvé avec comme idTournoi : {id_tournoi}"
    else:
        collection.update_many({"statut": "Occupé", "idTournoi": id_tournoi}, {"$set": {"statut": "Disponible",
                                                                                        "idTournoi": "Aucun"}})
        return "Modification du statut effectuée"


# Méthode permettant d'alléger le code
def modif_statut_liste_equip(id_tournoi, liste):
    # Récupération de la collection equipements.
    collection = bd.get_collection("equipements")

    # Mise à jour du statut des équipements de la liste
    for equipement in liste:
        collection.update_one({"_id": equipement["_id"]},
                              {"$set": {"statut": "Occupé", "idTournoi": id_tournoi}})
