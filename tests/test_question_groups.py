import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from static.question_groups import QUESTION_GROUPS, get_related_questions

def test_question_groups_existe(): #test existence dictionnaire
    assert isinstance(QUESTION_GROUPS, dict)
    assert len(QUESTION_GROUPS) > 0

def test_question_groups_maisons(): # test groupe 4 maisons
    assert 'maison' in QUESTION_GROUPS
    maisons = QUESTION_GROUPS['maison']
    assert len(maisons) == 4

def test_question_groups_genres(): #test genres groupés
    assert 'genre' in QUESTION_GROUPS
    genres = QUESTION_GROUPS['genre']
    assert len(genres) == 2 

def test_get_related_questions_yes_maison():
    maison_questions = QUESTION_GROUPS.get('maison', [])
    if len(maison_questions) >= 4:
        gryffondor_idx = maison_questions[0]
        serpentard_idx = maison_questions[1]
        poufsouffle_idx = maison_questions[2]
        serdaigle_idx = maison_questions[3]
        # Si Gryffondor = Oui, les 3 autres doivent être grisées
        related = get_related_questions(question_index=gryffondor_idx, got_yes=True)
        
        assert serpentard_idx in related
        assert poufsouffle_idx in related
        assert serdaigle_idx in related
        assert gryffondor_idx not in related  # Pas elle-même

def test_get_related_questions_no_maison():
    maison_questions = QUESTION_GROUPS.get('maison', [])
    
    if len(maison_questions) >= 1:
        gryffondor_idx = maison_questions[0]
        # Si réponse = Non, la fonction retourne une liste vide
        related = get_related_questions(question_index=gryffondor_idx, got_yes=False)
        assert related == []

def test_get_related_questions_yes_genre():
    genre_questions = QUESTION_GROUPS.get('genre', [])
    if len(genre_questions) >= 2:
        homme_idx = genre_questions[0]
        femme_idx = genre_questions[1]

        related = get_related_questions(question_index=homme_idx, got_yes=True)
        assert femme_idx in related

def test_get_related_questions_no_genre():
    genre_questions = QUESTION_GROUPS.get('genre', [])
    if len(genre_questions) >= 1:
        homme_idx = genre_questions[0]
        related = get_related_questions(question_index=homme_idx, got_yes=False)
        assert related == []
