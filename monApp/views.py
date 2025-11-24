from flask import Flask,render_template
from .app import app

@app.route('/')
@app.route('/index/')
def index():
    return render_template("nav_bar.html")

@app.route('/chercheur/')
def chercheur_accueil():
    return render_template("Chercheur_Accueil.html")

@app.route('/chercheur/campagne/')
def chercheur_campagne():
    return render_template("Chercheur_Campagne.html")

@app.route('/chercheur/echantillon/')
def chercheur_echantillon():
    return render_template("Chercheur_Echantillon.html")

@app.route('/chercheur/sequence/')
def chercheur_sequence():
    return render_template("Chercheur_Sequence.html")

if __name__ == "__main__":
    app.run()