import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from static.question import question
from static.perso import personnage

def test_question_maison():
    harry = personnage (
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
    draco = personnage (
        nom = "Draco Malefoy",
        description= "Un élève de Serpentard aux cheveux blonds",
        maison = "Serpentard",
        genre = "H",
        cheveux = "Blonds",
        lunettes = False,
        baguette_particuliere= None,
        animal = "Aucun",
        professeur=  False, 
        sang= "Pur",
        role = "méchant",
        trait_distinctif = "Aucun",
        moralite= "Méchant", 
        famille ="Malefoy",
        survit_fin = True, 
        meurt_dans_saga = False, 
        bataille_finale = True,
        role_majeur = True, 
        figure_autorite = False,
        evolution_perception = True, 
        camp_ambigu = True,
        famille_importante = True, 
        proche_harry = False,
        mort_marquante = False, 
        pouvoir_special= False,
        present_longtemps= True,
    )
    q1 = question("maison", "Gryffondor", "Est-ce que la maison est Gryffondor ?")

    assert q1.poser_question(harry) == True
    assert q1.poser_question(draco) == False

def test_question_genre():
    harry = personnage (
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
    hermione = personnage (
        nom = "Hermione Granger",
        description= "Une élève de Gryffondor aux cheveux bruns épais et bouclés. Brillante et très studieuse.",
        maison = "Gryffondor",
        genre = "F",
        cheveux = "Bruns",
        lunettes = False,
        baguette_particuliere= None,
        animal = "Chat",
        professeur=  False, 
        sang= "Moldu",
        role = "gentil",
        trait_distinctif = None,
        moralite= "Gentil", 
        famille ="N/A",
        survit_fin = True, 
        meurt_dans_saga = False, 
        bataille_finale = True,
        role_majeur = True, 
        figure_autorite = False,
        evolution_perception = False, 
        camp_ambigu = False,
        famille_importante = False, 
        proche_harry = True,
        mort_marquante = False, 
        pouvoir_special= False,
        present_longtemps= True,
    )
    q2 = question ("genre", "F", "Est-ce que le genre est Femme ?")

    assert q2.poser_question(hermione) == True
    assert q2.poser_question(harry) == False