from flask import Flask,render_template
from .app import app
from .models import Personnel,Plateforme

@app.route('/')
@app.route('/index/')
def index():
    return render_template("nav_bar.html")

@app.route('/chercheur/')
def chercheur_accueil():
    return render_template("Chercheur_Accueil.html")

@app.route('/chercheur/campagne/')
def chercheur_campagne():
    plateformes = Plateforme.query.all()
    personnels = Personnel.query.all()
    return render_template("Chercheur_Planifier_Camp.html", lesPlateformes = plateformes, lesPersonnels = personnels)

@app.route('/chercheur/echantillon/')
def chercheur_echantillon():
    return render_template("Chercheur_Echantillon.html")

@app.route('/chercheur/sequence/')
def chercheur_sequence():
    return render_template("Chercheur_Sequence.html")
@app.route("/admin/")
def admin():
    return render_template("home_admin.html")

if __name__ == "__main__":
    app.run()