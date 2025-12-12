from flask import Flask, render_template, request, session, redirect, url_for
import random

from static.construction import liste_personnages, liste_questions
from static.perso_images import personnages

app = Flask(__name__)
app.secret_key = "secret123"


@app.route('/')
def accueil():
    return render_template('accueil.html')

# Mode SOLO

@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    session["mode"] = "solo"

    # L'ordinateur choisit le personnage à deviner
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom
        session["restants"] = [p.nom for p in liste_personnages]

    if "asked_questions" not in session:
        session["asked_questions"] = []

    secret_nom = session["secret"]
    secret_obj = next(p for p in liste_personnages if p.nom == secret_nom)

    restants_noms = session.get("restants", [p.nom for p in liste_personnages])
    restants = [p for p in liste_personnages if p.nom in restants_noms]

    reponse = None
    message = None

    if request.method == 'POST':
        guess = (request.form.get("guess") or "").strip()
        question_index = (request.form.get("question") or "").strip()

        # Quand le joueur devine 
        if guess:
            resultat = (guess == secret_obj.nom)
            if resultat:
                message = f"Bravo ! Tu as deviné le personnage {secret_obj.nom}"
            else:
                message = f"Raté, ce n'était pas {guess}. Le personnage à deviner était {secret_obj.nom}"
            return render_template(
                "fin.html",
                message=message,
                resultat=resultat,
                guess=guess,
                secret=secret_obj.nom,
                guessed_image=personnages.get(guess),
                secret_image=personnages.get(secret_obj.nom)
            )

        # Le joueur pose une question
        elif question_index:
            idx = int(question_index)
            session["asked_questions"].append(idx)
            question_obj = liste_questions[idx]
            reponse_oui, nouveaux_restants = filtrer_personnages(restants, question_obj, secret_obj )
            session["restants"] = [p.nom for p in nouveaux_restants]
            restants = nouveaux_restants
            reponse = "Oui" if reponse_oui else "Non"

    # Le tour est fini
    return render_template(
        'jeu.html',
        personnages=personnages,
        restants=session["restants"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions"],
        message=message
        )


# Mode DUO

@app.route('/choisir_mode_duo')
def choisir_mode_duo():
    difficulty = request.args.get("difficulty", "easy")
    session["duo_difficulty"] = difficulty
    return redirect('/jeu_duo')


def choosing_best_question(unused_questions, restants_opponent):
    nbre_restants = len(restants_opponent)
    best_question = None
    closest_to_half = float('inf')

    for question_idc in unused_questions:
        question = liste_questions[question_idc]
        count_yes = 0
        for perso in restants_opponent:
            if question.poser_question(perso):
                count_yes += 1
        ratio = count_yes / nbre_restants
        distance = abs(ratio - 0.5)
        if distance < closest_to_half:
            closest_to_half = distance
            best_question = question_idc
    return best_question


@app.route('/jeu_duo', methods=['GET', 'POST'])
def jeu_duo():
    session["mode"] = "duo"

    # L'ordinateur choisit un personnage à deviner
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom
        session["restants"] = [p.nom for p in liste_personnages]

    if "restants_opponent" not in session:
        session["restants_opponent"] = [p.nom for p in liste_personnages]

    if "asked_questions" not in session:
        session["asked_questions"] = []

    if "opponent_question_idx" not in session:
        session["opponent_question_idx"] = None

    secret_obj = next(p for p in liste_personnages if p.nom == session["secret"])
    restants = [p for p in liste_personnages if p.nom in session["restants"]]
    restants_opponent = [p for p in liste_personnages if p.nom in session["restants_opponent"]]
    reponse = None
    message = None
    opponent_question_idx = session.get("opponent_question_idx")

    if request.method == 'POST':

        # Le joueur répond à la question de l'ordinateur
        answer_opp = request.form.get("answer_opponent")
        if answer_opp is not None and opponent_question_idx is not None:
            question_obj = liste_questions[opponent_question_idx]
            new_restants_opp = filter_for_computer(restants_opponent, question_obj, answer_opp)
            session["restants_opponent"] = [p.nom for p in new_restants_opp]
            restants_opponent = new_restants_opp 
            session["opponent_question_idx"] = None
            if len(new_restants_opp) == 1:
                computer_guess = new_restants_opp[0]
                message = "Dommage, tu as perdu."
                return render_template(
                    "fin_duo.html",
                    message=message,
                    resultat=False,
                    guess=None,
                    secret=session["secret"],
                    guessed_image=None,
                    computer_guess=computer_guess,
                    personnages=personnages,
                    secret_image=personnages.get(computer_guess.nom)
                )
            return redirect('/jeu_duo')

        # Si le joueur émet une hypothèse
        guess = (request.form.get("guess") or "").strip()
        if guess:
            resultat = (guess == secret_obj.nom)
            if resultat:
                message = f"Bravo ! Tu as deviné le personnage {secret_obj.nom}"
            else:
                message = f"Raté, ce n'était pas {guess}. Le personnage était {secret_obj.nom}" #Loser
            return render_template(
                "fin.html",
                message=message,
                resultat=resultat,
                guess=guess,
                secret=secret_obj.nom,
                guessed_image=personnages.get(guess),
                secret_image=personnages.get(secret_obj.nom)
            )

        #Le joueur pose une question
        question_index = (request.form.get("question") or "").strip()
        if question_index:
            idx = int(question_index)
            session["asked_questions"].append(idx)
            question_obj = liste_questions[idx]
            reponse_oui, nouveaux_restants = filtrer_personnages(restants, question_obj, secret_obj)
            session["restants"] = [p.nom for p in nouveaux_restants]
            restants = nouveaux_restants
            reponse = "Oui" if reponse_oui else "Non"

            # Après le joueur, c'est au tour de l'ordinateur de poser une question
            asked = session["asked_questions"] 
            unused_questions = [i for i in range(len(liste_questions)) if i not in asked]
            difficulty = session.get("duo_difficulty", "easy")
            if unused_questions:
                if difficulty == "easy":
                    session["opponent_question_idx"] = random.choice(unused_questions)
                else:
                    session["opponent_question_idx"] = choosing_best_question(unused_questions, restants_opponent)
            else:
                session["opponent_question_idx"] = None

    #Fin du tour
    return render_template(
        'jeu_duo.html',
        personnages=personnages,
        restants=session["restants"],
        restants_opponent=session["restants_opponent"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions"],
        opponent_question_idx=session.get("opponent_question_idx"),
        message=message
    )


@app.route('/reset')
def reset():
    mode = session.get("mode", "solo")
    session.clear()
    session["mode"] = mode
    if mode == "solo":
        return redirect(url_for('jeu'))
    else:
        return redirect(url_for('jeu_duo'))


# Filtrer les réponses

def filter_for_computer(restants_opponent, question_obj, player_answer):
    if player_answer == "Oui":
        return [p for p in restants_opponent if question_obj.poser_question(p)]
    else:
        return [p for p in restants_opponent if not question_obj.poser_question(p)]


def filtrer_personnages(personnages_restants, question_obj, secret_obj):
    reponse = question_obj.poser_question(secret_obj)
    nouveaux_restants = [
        p for p in personnages_restants if question_obj.poser_question(p) == reponse
    ]
    return reponse, nouveaux_restants


if __name__ == '__main__':
    app.run(debug=True)
