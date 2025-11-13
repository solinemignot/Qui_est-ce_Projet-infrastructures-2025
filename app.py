from flask import Flask, render_template, request
import json
import random 

#Import des photos des personnages
from static.perso_images import personnages

#Import des caractéristiques des personnages
from static.perso_caract import caracteristiques_personnages


app = Flask(__name__)


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    #L'algorithme choisit au hasard un personnage qu'il faudra deviner
    perso = random.choice(list(caracteristiques_personnages.keys()))

    print(perso)
    reponse = None
    if request.method == 'POST':
        question = request.form.get('question').lower()
        reponse = traiter_question(question, perso)
    return render_template('jeu.html', personnages=personnages, reponse=reponse)

def traiter_question(question, perso):
    if "lunettes" in question:
        avec_lunettes = [nom for nom, img in personnages.items() if personnages_info[nom]["lunettes"]]
        return f"Personnages avec des lunettes : {', '.join(avec_lunettes)}"
    # Add more rules here
    return "Je n'ai pas compris la question."

if __name__ == '__main__':
    app.run(debug=True)