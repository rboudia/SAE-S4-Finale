from Tournoi import Tournoi

def recup_nom():
    nom_tournoi = input("Choisissez le nom de votre tournoi : ")
    print("Le nom choisit est :", nom_tournoi)
    choix = input("Confirmez vous le choix ? (y ou n) : ")
    while choix != "y":
        if choix != "n" and choix != "y":
            choix = input("Erreur veuillez reconfirmez le choix ? y or n : ")
        elif choix == "n":
            nom_tournoi = input("Choisissez le nom de votre tournoi :")
            print("Le nom choisit est :", nom_tournoi)
            choix = input("Confirmez vous le choix ? y or n : ")
    
    return nom_tournoi
    
    
"""
def recup_joueurs():
    joueurs = []
    print("Ajout de joueurs")
    for i in range(2):
        print("Joueur ", i+1)
        nom = input("Quel est le nom : ")
        prenom = input("Quel est le prenom : ")
        age = input("Quel est l'age : ")
        niveau = input("Quel est votre niveau : ")
        joueurs.append((nom, prenom, age, niveau))
        print()
    return joueurs
"""
    
    
def recup_date():
    cond = False
    date = input("Choisissez une date sous le format suivant : jj/mm/aaaa : ")
    jour, mois, annee = date.split("/")
    print(mois)
    while (len(date) != 10 or len(jour) !=2 or len(mois) !=2 or len(annee) != 4) and cond == False:
        date = input("Erreur de saisie, choisissez une date sous le format suivant : jj/mm/aaaa : ")
        jour, mois, annee = date.split("/")
        jour_int, mois_int, annee_int = int(jour), int(mois), int(annee)
            
        if (jour_int > 0 and jour_int < 32) and (mois_int > 0 and mois_int < 13) and annee_int > 2023:
            cond = True
                
    return date
        
        
def recup_format():
    print("Choisissez le format du tournoi")
    choix = int(input("1 - Simple\n2 - Double\n3 - Equipe\n4 - Mixte\n"))
        
    while choix < 1 or choix > 4:
        print("Erreur de saisie, choisissez le format du tournoi")
        choix = int(input("1 - Simple\n2 - Double\n3 - Equipe\n4 - Mixte\n"))
            
    form = None
    if choix == 1:
        form = "Simple"
    elif choix == 2:
        form = "Double"
    elif choix == 3:
        form = "Equipe"
    else:
        form = "Mixte"
            
    return form
    
    
def recup_age():
    cond = False 
        
    while not cond:
        print("Veuillez choisir l'age minimale et l'age maximale pour le tournoi")
        age_min = int(input("Age min : "))
        age_max = int(input("Age max : "))
        if age_min >= 0 and age_max > age_min:
            cond = True
        else:
            print("Veuillez resaisir les ages, l'age minimale doit etre inferieur a l'age superieur")
    
    age = str(age_min) + "-" + str(age_max)
    return age
    
    
def recup_niveau():
    print("Choisissiez le niveau")
    choix = int(input("1 - Amateur\n2 - Intermédiaire\n3 - Profesionnel\n"))
        
    while choix < 1 or choix > 3:
        print("Erreur de saisie, choisissiez le niveau")
        choix = int(input("1 - Amateur\n2 - Intermédiaire\n3 - Profesionnel\n"))
            
    niveau = None
    if choix == 1:
        niveau = "Amateur"
    elif choix == 2:
        niveau = "Intermediaire"
    else:
        niveau = "Profesionnel"
            
    return(niveau)


def creation_tournoi():
    nom = recup_nom()
    date = recup_date()
    format = recup_format()
    age = recup_age()
    niveau = recup_niveau()
    categorie = (age, niveau)
    
    return Tournoi(nom, date, format, categorie)
    