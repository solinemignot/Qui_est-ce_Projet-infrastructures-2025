import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from static.construction import construire_personnage, construire_liste_questions, liste_personnages

def test_construire_personnage_retourne_liste(): #test liste construire perso
    personnages = construire_personnage()
    assert isinstance(personnages, list)
    assert len(personnages) > 0

def test_liste_personnages_existe(): #test liste perso existe
    assert liste_personnages is not None
    assert isinstance(liste_personnages, list)
    assert len(liste_personnages) > 0

def test_personnages_uniques(): #test non doublon
    noms = [p.nom for p in liste_personnages]
    assert len(noms) == len(set(noms))  

def test_personnages_maisons_valides(): # tests maisons valides
    maisons_valides = ["Gryffondor", "Serpentard", "Poufsouffle", "Serdaigle", "Beauxbâtons"]
    for perso in liste_personnages:
        assert perso.maison in maisons_valides, f"{perso.nom} a une maison invalide: {perso.maison}"

def test_personnages_genres_valides():
    genres_valides = ["H", "F"]
    for perso in liste_personnages:
        assert perso.genre in genres_valides, f"{perso.nom} a un genre invalide: {perso.genre}"

def test_construire_liste_questions_easy(): #test constrution liste questions faciles
    questions = construire_liste_questions("easy")
    assert isinstance(questions, list)
    assert len(questions) > 0
    
    for q in questions:
        assert hasattr(q, 'question')
        assert hasattr(q, 'attribut')
        assert hasattr(q, 'valeur')
        assert q.question is not None

def test_construire_liste_questions_hard(): #test constrution liste questions difficiles
    questions = construire_liste_questions("hard")
    assert isinstance(questions, list)
    assert len(questions) > 0
    for q in questions:
        assert hasattr(q, 'question')
        assert q.question is not None

def test_questions_ont_texte_unique(): #test doublons questions
    questions = construire_liste_questions("easy")
    textes = [q.question for q in questions]
    assert len(textes) == len(set(textes)), "Il y a des questions en double"

def test_personnages_cheveux_valides(): #test couleurs valides cheveux
    couleurs_valides = ["Noirs", "Roux", "Blonds", "Bruns", "Gris", "Argentés", "Variables"]
    for perso in liste_personnages:
        assert perso.cheveux in couleurs_valides, f"{perso.nom} a une couleur de cheveux invalide: {perso.cheveux}"

def test_personnages_lunettes_boolean(): # test booléen lunettes
    for perso in liste_personnages:
        assert isinstance(perso.lunettes, bool), f"{perso.nom}.lunettes n'est pas un booléen"


def test_toutes_maisons_representees():
    maisons = set([p.maison for p in liste_personnages])
    assert "Gryffondor" in maisons
    assert "Serpentard" in maisons
    assert "Poufsouffle" in maisons
    assert "Serdaigle" in maisons

def test_les_deux_genres_representes():
    genres = set([p.genre for p in liste_personnages])
    assert "H" in genres
    assert "F" in genres
