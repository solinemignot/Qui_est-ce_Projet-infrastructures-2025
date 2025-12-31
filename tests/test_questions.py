import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from static.question import question
from static.perso import Personnage

def test_question_maison():
    harry = Personnage(nom="Harry Potter", maison="Gryffondor", genre="Homme",couleur_cheveux="Noir", lunettes=True)
    draco = Personnage(nom="Draco Malfoy", maison="Serpentard", genre="Homme",couleur_cheveux="Blond", lunettes=False)
    question = Question ("maison", "Gryffondor", "Est-ce que la maison est Gryffondor ?")

    assert question.poser_question(harry) == True
    assert question.poser_question(draco) == False

def test_question_genre():
    hermione = Personnage(nom="Hermione Granger", maison="Gryffondor", genre="Femme",couleur_cheveux="Brun", lunettes=False)
    ron = Personnage(nom="Ron Weasley", maison="Gryffondor", genre="Homme",couleur_cheveux="Rouge", lunettes=False)
    question = Question ("genre", "Femme", "Est-ce que le genre est Femme ?")

    assert question.poser_question(hermione) == True
    assert question.poser_question(ron) == False
    