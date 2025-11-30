from flask import Flask, render_template, request, session, redirect, url_for

import random

from static.construction import liste_personnages, liste_questions
from static.perso_images import personnages

app = Flask(__name__)
app.secret_key = "secret123"


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    # initialisation
    if "secret" not in session:
        secret_obj = random.choice(liste_personnages)
        session["secret"] = secret_obj.nom             
        session["restants"] = [p.nom for p in liste_personnages]


    secret_nom = session["secret"]
    secret_obj = next(p for p in liste_personnages if p.nom == secret_nom)
    restants_noms = session.get("restants", [p.nom for p in liste_personnages])
    restants = [p for p in liste_personnages if p.nom in restants_noms]

    reponse = None
    message = None

    if request.method == 'POST':
        guess = (request.form.get("guess") or "").strip()
        question_index = (request.form.get("question") or "").strip()

        #si le joeur veut deviner

        if guess :
            if guess == secret_obj.nom :
                message = f"Bravo ! Tu as deviné le personnage {secret_obj.nom}"
            else :
                message = f"Raté, ce n'était pas {guess}. Le personnage à deviner était {secret_obj.nom}"
            
            guessed_image = personnages[guess]                # image du choix
            secret_image = personnages[secret_obj.nom]         # image correcte
            resultat = guess == secret_obj.nom

            return render_template(
                "fin.html",
                message=message,
                resultat = resultat,
                guess=guess,
                secret=secret_obj.nom,
                guessed_image=guessed_image,
                secret_image=secret_image
            )
       
        # si le joueur pose une question
        elif question_index:
            idx = int(question_index)
            question_obj = liste_questions[idx]

            reponse_oui, nouveaux_restants = filtrer_personnages(
                restants, question_obj, secret_obj
            )

            # on met à jour la session 
            session["restants"] = [p.nom for p in nouveaux_restants]
            restants = nouveaux_restants

            reponse = "Oui" if reponse_oui else "Non"

  
    return render_template(
        'jeu.html',
        personnages=personnages,         
        restants=session["restants"],    
        reponse=reponse,                 
        questions=liste_questions,       
        message=message                  
        )

@app.route('/reset')
def reset():
    session.clear()           
    return redirect(url_for('jeu'))   


def filtrer_personnages(personnages_restants, question_obj, secret_obj):
    # éponse pour le personnage secret
    reponse = question_obj.poser_question(secret_obj)
    nouveaux_restants = []
    for perso in personnages_restants:
        #on garde seulement ceux qui ont la même réponse que le secret
        if question_obj.poser_question(perso) == reponse:
            nouveaux_restants.append(perso)
    return reponse, nouveaux_restants


#@app.route('/choisir', methods = ['GET', 'POST'])
#def choisir():
    #choix = None

   # if request.method == 'POST':
       # choix = request.form.get("mon_perso")
       # if choix in personnages :
            #session["secret_joueur"] = choix #rediriger vers l'endroit où l'IA devine la carte
           # return redirect('/jeu')
       # else :
            #choix = None
    
    #return render_template("choisir.html",
                          # personnages=personnages,
                          # choix=session.get("secret_joueur"))


if __name__ == '__main__':
    app.run(debug=True)
