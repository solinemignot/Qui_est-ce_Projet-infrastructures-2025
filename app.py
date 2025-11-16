from flask import Flask, render_template, request, session
import random

# Import des photos
from static.perso_images import personnages

# Import des caractéristiques
from static.perso_caract import caracteristiques_personnages

# Import des questions
from static.questions_map import questions_map

app = Flask(__name__)
app.secret_key = "secret123"     # nécessaire pour utiliser session


# Route accueil
@app.route('/')
def accueil():
    return render_template('accueil.html')



# Fonction pour filtrer les personnages restants
def filtrer_personnages(personnages_restants, cle, valeur, reponse_oui):
    nouveaux = []

    for nom in personnages_restants:
        perso = caracteristiques_personnages[nom]

        # Cas spécial : "a un animal ?"
        if cle == "animal" and valeur == "!=":
            perso_a_animal = perso["animal"] != "Aucun"
            if reponse_oui == perso_a_animal:
                nouveaux.append(nom)
            continue

        # Cas normal
        perso_valeur = perso[cle]

        if reponse_oui and perso_valeur == valeur:
            nouveaux.append(nom)
        elif not reponse_oui and perso_valeur != valeur:
            nouveaux.append(nom)

    return nouveaux



# Route du jeu
@app.route('/jeu', methods=['GET', 'POST'])

def jeu():

    # Si on clique sur "Commencer la partie", on réinitialise la session
    #Ca ne marche pas pour réinitialiser la session
    if request.method == 'POST' and request.form.get("reset"):
        session.pop("secret", None)
        session.pop("restants", None)

    # Si c'est la première visite ou après reset, on initialise
    if "secret" not in session:
        session["secret"] = random.choice(list(caracteristiques_personnages.keys()))
        session["restants"] = list(caracteristiques_personnages.keys())

    secret = session["secret"]
    restants = session["restants"]

    reponse = None

    # Quand une question est posée
    if request.method == 'POST':
        selected = request.form.get("question")

        if selected in questions_map:
            cle, valeur = questions_map[selected]
            secret_perso = caracteristiques_personnages[secret]

            # Déterminer si la réponse est OUI ou NON
            if valeur == "!=":
                reponse_oui = secret_perso["animal"] != "Aucun"
            else:
                reponse_oui = secret_perso[cle] == valeur

            reponse = "Oui" if reponse_oui else "Non"

            # On filtre les personnages restants
            restants = filtrer_personnages(restants, cle, valeur, reponse_oui)
            session["restants"] = restants

    # Préparer les images filtrées
    personnages_affiches = {nom: personnages[nom] for nom in restants}

    return render_template('jeu.html',
                            personnages=personnages,               # toutes les images
                            restants=session["restants"],          # liste des noms encore possibles
                            reponse=reponse
                        )




# Reset optionnel
@app.route('/reset')
def reset():
    session.clear()
    return "Partie réinitialisée ! <a href='/jeu'>Rejouer</a>"



# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
