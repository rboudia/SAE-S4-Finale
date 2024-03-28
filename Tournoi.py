class Tournoi:
    def __init__(self, nom: str, date: str, format: str, categorie: tuple):
        assert isinstance(nom, str), "Le nom doit être une chaine de caractère"

        assert isinstance(date, str), "La date est une chaine de caractère sous le format suivant : jj/mm/aaaa"
        jour, mois, annee = date.split("/")
        assert len(jour) == 2, "Le jour doit être de 2 caractères"
        assert len(mois) == 2, "Le mois doit être de 2 caractères"
        assert len(annee) == 4, "L'annee doit être de 4 caractères"

        assert jour.isdigit(), "Le jour doit être un nombre"
        assert mois.isdigit(), "Le mois doit être un nombre"
        assert annee.isdigit(), "L'annee doit être un nombre"

        jour = int(jour)
        mois = int(mois)
        annee = int(annee)

        assert 1 <= jour <= 31, "Le jour doit être compris entre 1 et 31"
        assert 1 <= mois <= 12, "Le mois doit être compris entre 1 et 12"
        assert annee >= 2024, "L'année doit être supérieure ou égale à 2024"

        assert format == "Simple" or format == "Double" or format == "Equipe" or format == "Mixte", "Le format doit être parmi l'un des 4 suivants: Simple, Double, Equipe, Mixte"

        assert categorie[0][0] >= 0 and categorie[0][1] >= 0, "Les ages doivent être positifs"
        assert categorie[0][0] < categorie[0][1], "Age max doit etre sup a age min"

        assert categorie[1] == "Amateur" or categorie[1] == "Intermédiaire" or categorie[1] == "Professionel", "Le niveau doit être parmi l'un des 3 suivants: Amateur, Intermédiaire, Professionel"

        self.nom = nom
        self.date = date
        self.format = format
        self.categorie = categorie
