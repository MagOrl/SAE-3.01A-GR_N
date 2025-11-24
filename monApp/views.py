from flask import Flask,render_template
from .app import app
from .models import Materiel, habilitation

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

@app.route("/admin/")
def admin():
    return render_template("home_admin.html")

@app.route("/admin/gerer_materiel")
def admin_gerer_materiel():
    materiels = Materiel.query.join(habilitation, Materiel.id_hab == habilitation.id_hab).add_columns(habilitation.nom_hab).all()
    return render_template("gerer_materiel_admin.html", materiels=materiels)


if __name__ == "__main__":
    app.run()