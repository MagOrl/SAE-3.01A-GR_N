from flask import Flask, render_template
from .app import app
from .models import *

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

@app.route('/admin/gerer_personnel/<id_pers>')
def gerer_personnel_detail(id_pers):
    pers = personnel.query.get_or_404(id_pers)
    specialisations = SpecialiserEn.query.filter_by(id_pers=id_pers).all()
    participations = Participer.query.filter_by(id_pers=id_pers).all()
    return render_template('view_personel_admin.html', personnel=pers, specialisations=specialisations, participations=participations)

if __name__ == "__main__":
    app.run()