def niveaux_arbre_tournoi(matchs_totales):
    niveaus = []
    matchs_restants = matchs_totales
    matchs_au_niveau = 1
    niveau = 1

    while matchs_restants > 0 and matchs_restants >= matchs_au_niveau:
        niveaus.append((niveau, matchs_au_niveau))
        matchs_restants -= matchs_au_niveau
        niveau += 1
        matchs_au_niveau *= 2
        liste_inverse = niveaus[::-1]
    return liste_inverse


def recup_match(matchs_totales):

    nb_matchs = 0
    for niveau in niveaux_arbre_tournoi(matchs_totales):
        nb_matchs += niveau[1]

    return nb_matchs

# Exemple d'utilisation
print(36//5)
