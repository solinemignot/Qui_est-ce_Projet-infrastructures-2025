import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from static.perso import personnage

def test_personnage_creation(): #test la création d'un personnage
    perso = personnage (
        nom = "Harry Potter",
        description= "Un élève de Gryffondor aux cheveux noirs en bataille",
        maison = "Gryffondor",
        genre = "H",
        cheveux = "Noirs",
        lunettes = True,
        baguette_particuliere= None,
        animal = "Hibou",
        professeur=  False, 
        sang= "Mélé",
        role = "gentil",
        trait_distinctif = "cicatrice",
        moralite= "Gentil", 
        famille ="Potter",
        survit_fin = True, 
        meurt_dans_saga = False, 
        bataille_finale = True,
        role_majeur = True, 
        figure_autorite = False,
        evolution_perception = False, 
        camp_ambigu = False,
        famille_importante = True, 
        proche_harry = True,
        mort_marquante = False, 
        pouvoir_special= True,
        present_longtemps= True,
    )
    assert perso.nom == "Harry Potter"
    assert perso.maison == "Gryffondor"
    assert perso.animal == "Hibou"



