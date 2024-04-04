class Joueur:
    def __init__(self, nom: str, prenom: str, age: str, niveau: str):
        assert isinstance(nom, str), "Le nom doit être une chaîne de caractères"
        assert isinstance(prenom, str), "Le prénom doit être une chaîne de caractères"
        assert isinstance(age, str), "L'âge doit être une chaîne de caractères"
        assert isinstance(niveau, str), "Le niveau doit être une chaîne de caractères"

        assert age.isdigit(), "L'âge doit être un nombre"
        age = int(age)
        assert age >= 0, "L'âge ne peut pas être négatif"

        assert niveau in ["Amateur", "Intermédiaire",
                          "Professionnel"], "Le niveau doit être l'un des suivants : Amateur, Intermédiaire, Professionnel"

        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.niveau = niveau





