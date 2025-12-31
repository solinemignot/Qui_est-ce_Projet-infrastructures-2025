import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key_123'
    with app.test_client() as client : 
        yield client

#Tests page accuei

def test_accueil_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_accueil_contient_mode_solo(client):
    response = client.get('/')
    assert b'Mode Solo' in response.data

def test_accueil_contient_mode_duel(client):
    """Test que la page d'accueil contient 'Mode Duel'"""
    response = client.get('/')
    assert b'Mode Duel' in response.data

# Tests jeu solo


def test_jeu_solo_auto_grey_true(client): # test grisage automatique
    response = client.get('/jeu?auto_grey=true')
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session.get('auto_grey_solo') == True

def test_jeu_solo_auto_grey_false(client): # test grisage manuel
    response = client.get('/jeu?auto_grey=false')
    assert response.status_code == 200
    
    with client.session_transaction() as session:
        assert session.get('auto_grey_solo') == False

def test_jeu_solo_secret_genere(client): # test génération secret
    response = client.get('/jeu')
    with client.session_transaction() as session:
        assert 'secret' in session
        assert session['secret'] is not None

def test_jeu_solo_start_time_genere(client): # test génération timer
    response = client.get('/jeu')
    
    with client.session_transaction() as session:
        assert 'start_time' in session
        assert isinstance(session['start_time'], int)

def test_jeu_solo_elimines_initialise(client): # test liste éliminés initialisée
    response = client.get('/jeu')
    with client.session_transaction() as session:
        assert 'elimines' in session
        assert isinstance(session['elimines'], list)

def test_poser_question_solo(client): # test poser des questions
    with client.session_transaction() as sess:
        sess['secret'] = 'Harry Potter'
        sess['asked_questions_solo'] = []
        sess['elimines'] = []
        sess['auto_grey_solo'] = False  # Mode manuel
        sess['start_time'] = 1234567890
    response = client.post('/jeu', data={'question': '0'})
    assert response.status_code == 200
    
    with client.session_transaction() as session:
        assert 0 in session.get('asked_questions_solo', [])

def test_deviner_correct_solo(client): # test deviner bon personnage
    with client.session_transaction() as sess:
        sess['secret'] = 'Harry Potter'
        sess['start_time'] = 1234567890
    
    response = client.post('/jeu', data={'guess': 'Harry Potter'})
    assert response.status_code == 200
    assert b'Victoire' in response.data

def test_deviner_incorrect_solo(client): # test deviner mauvais personnage
    with client.session_transaction() as sess:
        sess['secret'] = 'Harry Potter'
        sess['start_time'] = 1234567890
    
    response = client.post('/jeu', data={'guess': 'Hermione Granger'})
    assert response.status_code == 200
    assert b'Hermione Granger' in response.data

def test_toggle_elimine_solo_griser(client): # test cliquer pour griser une carte
    with client.session_transaction() as session:
        session['elimines'] = []
    response = client.post('/toggle_elimine/Harry Potter')
    assert response.status_code == 204  
    with client.session_transaction() as session:
        assert 'Harry Potter' in session.get('elimines', [])

def test_toggle_elimine_solo_degriser(client): # test cliquer pour dégriser une carte
    with client.session_transaction() as session:
        session['elimines'] = ['Harry Potter']
    response = client.post('/toggle_elimine/Harry Potter')
    assert response.status_code == 204
    with client.session_transaction() as session:
        assert 'Harry Potter' not in session.get('elimines', [])

# Tests jeu duo

def test_choisir_mode_duo_easy(client): #test jeu duo facile
    response = client.get('/choisir_mode_duo?difficulty=easy&auto_grey=true')
    assert response.status_code == 302  # Redirection vers /choisir
    with client.session_transaction() as session:
        assert session.get('duo_difficulty') == 'easy'
        assert session.get('auto_grey_duo') == True

def test_choisir_mode_duo_hard_manuel(client): #test jeu duo difficile manuel
    response = client.get('/choisir_mode_duo?difficulty=hard&auto_grey=false')
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert session.get('duo_difficulty') == 'hard'
        assert session.get('auto_grey_duo') == False

def test_jeu_duo_route(client):
    with client.session_transaction() as session:
        session['duo_difficulty'] = 'easy'
    response = client.get('/jeu_duo')
    assert response.status_code == 200

def test_jeu_duo_secret_genere(client): # test génération secret duo
    with client.session_transaction() as session:
        session['duo_difficulty'] = 'easy'
    response = client.get('/jeu_duo')
    with client.session_transaction() as session:
        assert 'secret' in session
        assert session['secret'] is not None

def test_jeu_duo_elimines_initialise(client): # test liste éliminés duo initialisée
    with client.session_transaction() as session:
        session['duo_difficulty'] = 'easy'
    response = client.get('/jeu_duo')
    with client.session_transaction() as session:
        assert 'elimines_duo' in session
        assert isinstance(session['elimines_duo'], list)

def test_toggle_elimine_duo_griser(client): # test griser carte duo
    with client.session_transaction() as session:
        session['elimines_duo'] = []
    response = client.post('/toggle_elimine_duo/Drago Malefoy')
    assert response.status_code == 204
    with client.session_transaction() as session:
        assert 'Drago Malefoy' in session.get('elimines_duo', [])

def test_toggle_elimine_duo_degriser(client): # test dégriser carte duo
    with client.session_transaction() as session:
        session['elimines_duo'] = ['Drago Malefoy']
    response = client.post('/toggle_elimine_duo/Drago Malefoy')
    assert response.status_code == 204
    with client.session_transaction() as session:
        assert 'Drago Malefoy' not in session.get('elimines_duo', [])

def test_isolation_auto_grey_solo_duo(client): # test indépendance grisage auto
    response = client.get('/jeu?auto_grey=true')
    with client.session_transaction() as session:
        assert session.get('auto_grey_solo') == True
    response = client.get('/choisir_mode_duo?difficulty=easy&auto_grey=false')
    with client.session_transaction() as session:
        assert session.get('auto_grey_solo') == True  # Reste inchangé
        assert session.get('auto_grey_duo') == False

def test_reset_route(client): #test reset vers accueil
    response = client.get('/reset')
    assert response.status_code == 302  # Redirection

def test_rejouer_route(client): #test rejouer redirige
    response = client.get('/rejouer')