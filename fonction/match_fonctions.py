"""
Fichier qui contient des fonctions relatives à la collection matchs et qui permet d'alléger le code
"""

from Client2Mongo import Client2Mongo

# Ouverture de la connexion à la bd
bd = Client2Mongo("MyTennisPlan")


# Méthode qui est utilisée dans tournoi_routes et qui permet de supprimer les matchs d'un tournoi
def suppresion_matchs_tournois(nom_tournoi: str):
    # Récupération de la collection matchs de la bd
    collection = bd.get_collection("matchs")

    # Requête qui permet de vérifier si au moins un match existe pour le nom de tournoi donné
    match = collection.find_one({"nomTournoi": nom_tournoi})

    if not match:
        return f"Aucun match n'est en cours pour le tournoi : {nom_tournoi}"
    else:

        # Suppression des matchs associés au tournoi
        collection.delete_many({"nomTournoi": nom_tournoi})


# Méthode qui permet de modifier le nom du tournoi dans les matchs quand le nom du tournoi est modifié
def modif_nom_tournoi(ancien_nom_tournoi, nouveau_nom_tournoi):
    collection = bd.get_collection("matchs")

    match = collection.find_one({"nomTournoi": ancien_nom_tournoi})

    if not match:
        return "Aucun match n'a été trouvé pour ce tournoi"
    else:

        filtre = {"nomTournoi": ancien_nom_tournoi}
        nouvelle_valeur = {"$set": {"nomTournoi": nouveau_nom_tournoi}}
        collection.update_many(filtre, nouvelle_valeur)


# Méthode qui concoit les matchs pour faire un tournoi en arbre avec le nombre de matchs possibles
def niveaux_arbre_tournoi(matchs_possibles):
    niveaux = []
    matchs_restants = matchs_possibles
    matchs_au_niveau = 1
    niveau = 1

    while matchs_restants > 0 and matchs_restants >= matchs_au_niveau:
        niveaux.append((niveau, matchs_au_niveau))
        matchs_restants -= matchs_au_niveau
        niveau += 1
        matchs_au_niveau *= 2
        liste_inverse = niveaux[::-1]
    return liste_inverse


# Méthode qui récupère le nombre de match du premier niveau
def recup_nb_match(matchs_totales):
    liste = niveaux_arbre_tournoi(matchs_totales)
    premier_niveau = liste[0]

    return premier_niveau


# Méthode qui génère le nombre de matchs qui vont se joués après la création des premiers matchs
def generer_liste_niveau(nb_premiers_matchs):
    i = 1
    liste_niveau = [{"etape": i, "nbMatch": nb_premiers_matchs}]

    if nb_premiers_matchs % 2 != 0:
        nb_premiers_matchs = nb_premiers_matchs + 1

    while nb_premiers_matchs != 1:
        nb_premiers_matchs = nb_premiers_matchs // 2
        i += 1
        liste_niveau.append({"etape": i, "nbMatch": nb_premiers_matchs})

    return liste_niveau


