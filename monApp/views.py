from flask import render_template
from .app import app
from .models import *

@app.route('/')
@app.route('/index/')
def index():
    return render_template("nav_bar.html")

@app.route("/admin/")
def admin():
    return render_template("home_admin.html")


@app.route("/technicien/")
def technicien():
    return render_template("accueil_technicien.html")

@app.route("/gestion_changement_technicien/")
def gestion_changement_technicien():
    return render_template("gestion_changement_technicien.html")

@app.route("/gestion_maintenance/")
def gestion_maintenance():
    # Récupère toutes les plateformes et prépare les tuples (id_pla, nom_pla, jours_av_mainte)
    plateformes = [(p.id_pla, p.nom_pla, p.jours_av_mainte) for p in Plateforme.query.all()]
    return render_template("gestion_maintenance.html", plateformes=plateformes)

if __name__ == "__main__":
    app.run()