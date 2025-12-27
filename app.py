from flask import Flask, render_template, request, session, redirect, url_for
import random
import time

from static.construction import liste_personnages, liste_questions
from static.perso_images import personnages

app = Flask(__name__)
app.secret_key = "secret123"


@app.route('/')
def accueil():
    session.clear()  
    return render_template('accueil.html')


# =========================
#          SOLO
# =========================

@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    session["mode"] = "solo"
    descriptions = {p.nom: p.description for p in liste_personnages}
    if "elimines" not in session:
        session["elimines"] = []

    #clé dédiée SOLO (évite conflit avec DUO)
    if "asked_questions_solo" not in session:
        session["asked_questions_solo"] = []

    # L'ordinateur choisit le personnage à deviner
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom
        session["start_time"] = int(time.time())

    # Sécurité si secret existe mais pas start_time
    if "start_time" not in session:
        session["start_time"] = int(time.time())

    secret_nom = session["secret"]
    secret_obj = next((p for p in liste_personnages if p.nom == secret_nom), None)
    if secret_obj is None:
        session.pop("secret", None)
        return redirect(url_for("jeu"))

    reponse = None
    message = None

    if request.method == 'POST':
        guess = (request.form.get("guess") or "").strip()
        question_index = (request.form.get("question") or "").strip()

        # Devinette
        if guess:
            resultat = (guess == secret_obj.nom)
            if resultat:
                message = f"Bravo ! Tu as deviné le personnage {secret_obj.nom}."
            else:
                message = f"Raté, ce n'était pas {guess}. Le personnage à deviner était {secret_obj.nom}."

            guessed_obj = next((p for p in liste_personnages if p.nom == guess), None)

            elapsed_seconds = int(time.time()) - int(session.get("start_time", int(time.time())))

            return render_template(
                "fin.html",
                message=message,
                resultat=resultat,
                guess=guess,
                description_guess=guessed_obj.description if guessed_obj else None,
                secret=secret_obj.nom,
                description_secret=secret_obj.description,
                guessed_image=personnages.get(guess),
                secret_image=personnages.get(secret_obj.nom),
                elapsed_seconds=elapsed_seconds
            )

        # Question
        elif question_index:
            idx = int(question_index)
            if idx not in session["asked_questions_solo"]:
                session["asked_questions_solo"].append(idx)

            question_obj = liste_questions[idx]
            reponse_oui = question_obj.poser_question(secret_obj)
            reponse = "Oui" if reponse_oui else "Non"

    return render_template(
        "jeu.html",
        personnages=personnages,
        descriptions=descriptions,
        elimines=session["elimines"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions_solo"], 
        message=message,
        start_time=session.get("start_time")
    )


@app.route('/toggle_elimine/<nom>', methods=['POST'])
def toggle_elimine(nom):
    elimines = set(session.get("elimines", []))

    if nom in elimines:
        elimines.remove(nom)
    else:
        elimines.add(nom)

    session["elimines"] = list(elimines)
    return ("", 204)


# =========================
#          DUO
# =========================

@app.route('/choisir_mode_duo')
def choisir_mode_duo():
    difficulty = request.args.get("difficulty", "easy")
    session["duo_difficulty"] = difficulty
    # MODIFICATION : On va vers ta page existante 'choisir.html'
    return redirect(url_for('page_choix'))


def choosing_best_question(unused_questions, restants_opponent_objs):
    nbre_restants = len(restants_opponent_objs)
    if nbre_restants == 0:
        return None

    best_question = None
    closest_to_half = float('inf')

    for question_idc in unused_questions:
        question = liste_questions[question_idc]
        count_yes = 0

        for perso in restants_opponent_objs:
            if question.poser_question(perso):
                count_yes += 1

        ratio = count_yes / nbre_restants
        distance = abs(ratio - 0.5)

        if distance < closest_to_half:
            closest_to_half = distance
            best_question = question_idc

    return best_question

# Route pour afficher la page (GET) et traiter le choix (POST)
@app.route('/choisir', methods=['GET', 'POST'], endpoint='page_choix')
def page_choix():
    # Si le joueur a validé le formulaire (POST)
    if request.method == 'POST':
        # On récupère le nom via le champ caché 'mon_perso' de ton fichier HTML
        nom_choisi = request.form.get("mon_perso")
        
        if nom_choisi:
            session["secret_joueur"] = nom_choisi
            # On lance le jeu duo maintenant que le choix est fait
            return redirect(url_for('jeu_duo'))
    
    # Si on arrive juste sur la page (GET), on l'affiche
    return render_template('choisir.html', personnages=personnages)

@app.route('/jeu_duo', methods=['GET', 'POST'])
def jeu_duo():
    session["mode"] = "duo"
    descriptions = {p.nom: p.description for p in liste_personnages}
    # L'ordinateur choisit un personnage à deviner (joueur doit deviner session["secret"])
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom

    if "restants_opponent" not in session:
        session["restants_opponent"] = [p.nom for p in liste_personnages]

    #clés dédiées DUO
    if "asked_questions_duo" not in session:
        session["asked_questions_duo"] = []
    if "asked_questions_opponent" not in session:
        session["asked_questions_opponent"] = []

    if "opponent_question_idx" not in session:
        session["opponent_question_idx"] = None

    if "elimines_duo" not in session:
        session["elimines_duo"] = []

    if "awaiting_computer" not in session:
        session["awaiting_computer"] = False

    secret_obj = next((p for p in liste_personnages if p.nom == session["secret"]), None)
    if secret_obj is None:
        session.pop("secret", None)
        return redirect(url_for("jeu_duo"))

    # liste d'objets pour calculer la meilleure question
    restants_opponent_objs = [p for p in liste_personnages if p.nom in session["restants_opponent"]]

    reponse = None
    message = None

    if request.method == 'POST':

        # 1) Le joueur lance le tour de l'ordinateur (après avoir grisé)
        if request.form.get("next_turn") == "1":
            asked_player = set(session.get("asked_questions_duo", []))
            asked_opp = set(session.get("asked_questions_opponent", []))
            asked_all = asked_player | asked_opp

            unused_questions = [i for i in range(len(liste_questions)) if i not in asked_all]
            difficulty = session.get("duo_difficulty", "easy")

            if unused_questions:
                if difficulty == "easy":
                    chosen = random.choice(unused_questions)
                else:
                    chosen = choosing_best_question(unused_questions, restants_opponent_objs)

                session["opponent_question_idx"] = chosen

                # mémoriser la question de l'ordi
                if chosen is not None and chosen not in session["asked_questions_opponent"]:
                    session["asked_questions_opponent"].append(chosen)
            else:
                session["opponent_question_idx"] = None

            session["awaiting_computer"] = False
            return redirect('/jeu_duo')

        # 2) Le joueur répond à la question de l'ordinateur
        answer_opp = request.form.get("answer_opponent")
        opponent_question_idx = session.get("opponent_question_idx")

        if answer_opp is not None and opponent_question_idx is not None:
            question_obj = liste_questions[opponent_question_idx]

            new_restants_opp_objs = filter_for_computer(restants_opponent_objs, question_obj, answer_opp)
            session["restants_opponent"] = [p.nom for p in new_restants_opp_objs]
            session["opponent_question_idx"] = None

            # incohérent : plus aucun perso possible
            if len(new_restants_opp_objs) == 0:
                message = "Désolé, aucun personnage ne correspond à ta description."
                return render_template(
                    "fin_duo.html",
                    message=message,
                    resultat=None,
                    guess=None,
                    secret=session["secret"],
                    guessed_image=None,
                    computer_guess=None,
                    personnages=personnages,
                    secret_image=None
                )

            # l'ordi gagne
            if len(new_restants_opp_objs) == 1:
                computer_guess_obj = new_restants_opp_objs[0]
                computer_guess = computer_guess_obj.nom
                message = "Dommage, tu as perdu."
                return render_template(
                    "fin_duo.html",
                    message=message,
                    resultat=False,
                    guess=None,
                    secret=session["secret"],
                    guessed_image=None,
                    computer_guess=computer_guess,
                    computer_guess_description=computer_guess_obj.description,
                    personnages=personnages,
                    secret_image=personnages.get(computer_guess)
                )

            return redirect('/jeu_duo')

        # 3) Si on attend le tour de l'ordi, on bloque question/guess
        if session.get("awaiting_computer", False):
            if (request.form.get("guess") or "").strip() or (request.form.get("question") or "").strip():
                return redirect('/jeu_duo')

        # 4) Guess du joueur
        guess = (request.form.get("guess") or "").strip()
        if guess:
            resultat = (guess == secret_obj.nom)
            if resultat:
                message = f"Bravo ! Tu as deviné le personnage {secret_obj.nom}."
            else:
                message = f"Raté, ce n'était pas {guess}. Le personnage était {secret_obj.nom}."

            guessed_obj = next((p for p in liste_personnages if p.nom == guess), None)

            return render_template(
                "fin.html",
                message=message,
                resultat=resultat,
                guess=guess,
                description_guess=guessed_obj.description if guessed_obj else None,
                secret=secret_obj.nom,
                description_secret=secret_obj.description,
                guessed_image=personnages.get(guess),
                secret_image=personnages.get(secret_obj.nom)
            )

        # 5) Question du joueur
        question_index = (request.form.get("question") or "").strip()
        if question_index:
            idx = int(question_index)
            if idx not in session["asked_questions_duo"]:
                session["asked_questions_duo"].append(idx)

            question_obj = liste_questions[idx]
            reponse_oui = question_obj.poser_question(secret_obj)
            reponse = "Oui" if reponse_oui else "Non"

            # attendre que le joueur grise avant de lancer l'ordi
            session["awaiting_computer"] = True
            session["opponent_question_idx"] = None

    return render_template(
        "jeu_duo.html",
        personnages=personnages,
        descriptions=descriptions,
        elimines=session["elimines_duo"],
        restants_opponent=session["restants_opponent"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions_duo"], 
        opponent_question_idx=session.get("opponent_question_idx"),
        awaiting_computer=session.get("awaiting_computer", False),
        message=message
    )


@app.route('/toggle_elimine_duo/<nom>', methods=['POST'])
def toggle_elimine_duo(nom):
    elimines = set(session.get("elimines_duo", []))

    if nom in elimines:
        elimines.remove(nom)
    else:
        elimines.add(nom)

    session["elimines_duo"] = list(elimines)
    return ("", 204)



@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('accueil'))

# si le joueur veut rejouer après une partie
@app.route('/rejouer')
def rejouer():
    # On sauvegarde le mode et la difficulté avant de tout effacer
    mode_actuel = session.get("mode", "solo")
    difficulte = session.get("duo_difficulty", "easy")
    session.clear()
    # On remet le mode dans la nouvelle session
    session["mode"] = mode_actuel
    if mode_actuel == "solo":
        return redirect(url_for('jeu'))
    else:
        # En DUO, on remet la difficulté et on retourne au choix du perso
        session["duo_difficulty"] = difficulte
        return redirect(url_for('page_choix'))


def filter_for_computer(restants_opponent_objs, question_obj, player_answer):
    if player_answer == "Oui":
        return [p for p in restants_opponent_objs if question_obj.poser_question(p)]
    else:
        return [p for p in restants_opponent_objs if not question_obj.poser_question(p)]


if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0')
