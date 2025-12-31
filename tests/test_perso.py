import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from static.perso import Personnage

def test_personnage_creation(): #test la création d'un personnage
    perso = Personnage(
        nom = "Harry Potter",
        maison = "Gryffondor",
        genre = "Homme",
        cheveux = "Noirs",
        lunettes = True,
        couleur_cheveux = "Noirs",
        animal = "Hibou"
    )
    assert perso.nom == "Harry Potter"
    assert perso.maison == "Gryffondor"
    assert perso.animal == "Hibou"


def test_personnage_appartenance_maison():
    perso = Personnage("Hermione Granger", "Une élève de Gryffondor ","Gryffondor", "Femme", "Bruns", False)
    assert perso.maison == "Gryffondor"
    assert perso.maison != "Serpentard"

