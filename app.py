from flask import Flask, render_template, request, session, redirect, url_for
import random
import time

from static.construction import liste_personnages, liste_questions
from static.perso_images import personnages

app = Flask(__name__)
app.secret_key = "secret123"


@app.route('/')
def accueil():
    session.clear() #We can remove if we don't want to reset everytime we go back to the home page
    return render_template('accueil.html')



# Mode SOLO
@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    session["mode"] = "solo"

    if "elimines" not in session:
        session["elimines"] = []

    if "asked_questions" not in session:
        session["asked_questions"] = []

    # L'ordinateur choisit le personnage à deviner
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom
        #start_time démarre au début d'une partie
        session["start_time"] = int(time.time())

    # Sécurité si jamais secret existe mais pas start_time 
    if "start_time" not in session:
        session["start_time"] = int(time.time())

    secret_nom = session["secret"]
    secret_obj = next(p for p in liste_personnages if p.nom == secret_nom)

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

            # temps final
            elapsed = int(time.time()) - int(session.get("start_time", int(time.time())))

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
                elapsed=elapsed
            )


        # Question
        elif question_index:
            idx = int(question_index)
            if idx not in session["asked_questions"]:
                session["asked_questions"].append(idx)

            question_obj = liste_questions[idx]
            reponse_oui = question_obj.poser_question(secret_obj)
            reponse = "Oui" if reponse_oui else "Non"

    return render_template(
        "jeu.html",
        personnages=personnages,
        elimines=session["elimines"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions"],
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
    return ("", 204)  # pas de page, juste OK


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

    if "elimines_duo" not in session:
        session["elimines_duo"] = []

    if "awaiting_computer" not in session:
        session["awaiting_computer"] = False

    secret_obj = next(p for p in liste_personnages if p.nom == session["secret"])
    restants_opponent = [p for p in liste_personnages if p.nom in session["restants_opponent"]]

    reponse = None
    message = None
    opponent_question_idx = session.get("opponent_question_idx")

    if request.method == 'POST':

        
        #Le joueur lance le tour de l'ordinateur (après avoir grisé)

        if request.form.get("next_turn") == "1":
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

            session["awaiting_computer"] = False
            return redirect('/jeu_duo')

 
        #  Le joueur répond à la question de l'ordinateur
     
        answer_opp = request.form.get("answer_opponent")
        opponent_question_idx = session.get("opponent_question_idx")

        if answer_opp is not None and opponent_question_idx is not None:
            question_obj = liste_questions[opponent_question_idx]

            new_restants_opp = filter_for_computer(restants_opponent, question_obj, answer_opp)
            session["restants_opponent"] = [p.nom for p in new_restants_opp]
            session["opponent_question_idx"] = None

            # Cas incohérent : plus aucun perso possible
            if len(new_restants_opp) == 0:
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

            # L'ordi a trouvé exactement 1 candidat et gagne
            if len(new_restants_opp) == 1:
                computer_guess_obj = new_restants_opp[0]
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


        # si on attend le tour de l'ordi, on bloque question/guess

        if session.get("awaiting_computer", False):
            # Si quelqu'un essaie quand même d'envoyer un guess ou une question
            if (request.form.get("guess") or "").strip() or (request.form.get("question") or "").strip():
                return redirect('/jeu_duo')

       
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

      
        question_index = (request.form.get("question") or "").strip()
        if question_index:
            idx = int(question_index)
            if idx not in session["asked_questions"]:
                session["asked_questions"].append(idx)

            question_obj = liste_questions[idx]
            reponse_oui = question_obj.poser_question(secret_obj)
            reponse = "Oui" if reponse_oui else "Non"

         
            session["awaiting_computer"] = True

            
            session["opponent_question_idx"] = None

    return render_template(
        "jeu_duo.html",
        personnages=personnages,
        elimines=session["elimines_duo"],
        restants_opponent=session["restants_opponent"],
        reponse=reponse,
        questions=liste_questions,
        asked_questions=session["asked_questions"],
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



if __name__ == '__main__':
    app.run(debug=True)
