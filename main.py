from Client2Mongo import Client2Mongo
from Tournoi import Tournoi

a = Tournoi("Tournoi 2", "12/05/2024", "Simple", ((10, 35), "Intermediaire"))
bd = Client2Mongo("rayan")
bd.insertion_tournoi(a)
bd.affiche_tournois()
# bd.affiche_tournoi("Tournoi g")
# bd.suppresion_tournoi("Tournoi 2")
"""
for tournoi in bd.find("tournois"):
    print(tournoi)

print()

# bd.insertion_tournoi(a)
bd.suppresion_tournoi("Tournoi 2")
bd.modif_tournoi("Test2", "Tournoi Test 2")

for tournoi in bd.find("tournois"):
    print(tournoi)
"""