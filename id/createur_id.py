"""
Ce fichier permet de gérer les id lors de l'insertion dans la base de donnée

Il permet de sauvegarder et de lire les derniers de chaque collection de la base de donnée car si nous laissons
MongoDB gérer les id lors de l'insertion nous obtenions des erreurs d'affichages

Pour ce faire nous avons crée un fichier texte par collection qui contient le dernier id en date choisis initialement
par nos soins

Lors d'une insertion la méthode contenu dans ce fichier est appelé, elle va donc lire l'id contenu dans le fichier
texte de la collection correspondante puis l'incrémenté avant l'insertion et ensuite effacer l'id précédent
pour mettre le nouveau

"""


def creation_id(collection):
    with open(f"id/{collection}_id.txt", "r+") as f:
        dernier_id = int(f.read()) + 1
        f.seek(0)
        f.write(str(dernier_id))
    return dernier_id
