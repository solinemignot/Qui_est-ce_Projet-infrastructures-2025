from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/jeu')
def jeu():
    return render_template('jeu.html')

