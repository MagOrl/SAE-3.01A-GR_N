from flask import render_template, url_for, redirect, request
from .app import app, db
from .models import *
import random
from datetime import date, datetime, timedelta

@app.route('/')
@app.route('/index/')
def index():
    return render_template("nav_bar.html")

@app.route("/admin/")
def admin():
    return render_template("home_admin.html")


# Page d'accueil technicien
@app.route("/technicien/")
def technicien():
    return render_template("accueil_technicien.html")

# Page de menu gestion des changements de technicien
@app.route("/gestion_changement_technicien/")
def gestion_changement_technicien():
    return render_template("gestion_changement_technicien.html")

# Page de gestion des maintenances
@app.route("/gestion_maintenance/")
def gestion_maintenance():
    # Supprimer les maintenances passées
    maintenances_passees = Maintenance.query.filter(Maintenance.date_fin_maint < date.today()).all()
    for m in maintenances_passees:
        db.session.delete(m)
    if maintenances_passees:
        db.session.commit()

    donnees_plateformes = []
    for m in Maintenance.query.order_by(Maintenance.date_deb_maint).all():
        p = Plateforme.query.get(m.id_pla)
        
        # Calcul des jours restants avant le début de cette maintenance
        jours_restants = (m.date_deb_maint - date.today()).days
            
        donnees_plateformes.append((m.id_maint, p.id_pla, p.nom_pla, m.date_deb_maint, m.date_fin_maint, jours_restants))
            
    return render_template("gestion_maintenance.html", plateformes=donnees_plateformes)

# Méthode pour ajouter une Maintenance
@app.route("/maintenance/ajouter/", methods=["GET", "POST"])
def ajouter_maintenance():
    if request.method == "POST":
        id_pla = request.form.get("id_pla")
        id_maint = request.form["id_maint"]
        date_deb = request.form["date_deb_maint"]
        date_fin = request.form["date_fin_maint"]
        
        # Formatage des dates
        date_deb = datetime.strptime(date_deb, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()

        # Création et ajout de la nouvelle maintenance
        nouvelle_maintenance = Maintenance(id_maint, id_pla, date_deb, date_fin)
        db.session.add(nouvelle_maintenance)
        db.session.commit()
        
        return redirect(url_for('gestion_maintenance'))
    
    plateformes = []
    for p in Plateforme.query.all():
        # Calcul des dates suggérées pour la prochaine maintenance en fonction de la dernière et de l'intervalle
        last_maint = Maintenance.query.filter_by(id_pla=p.id_pla).order_by(Maintenance.date_fin_maint.desc()).first()
        if last_maint:
            next_start = last_maint.date_fin_maint + timedelta(days=p.inter_mainte)
        else:
            next_start = date.today()
        
        # Durée aléatoire de 1 ou 2 jours
        duree = random.choice([1, 2])
        next_end = next_start + timedelta(days=duree)
        
        plateformes.append({
            'id_pla': p.id_pla,
            'nom_pla': p.nom_pla,
            'next_start': next_start,
            'next_end': next_end
        })
        
    return render_template("ajouter_maintenance.html", plateformes=plateformes)

# Méthode pour supprimer une Maintenance
@app.route("/maintenance/supprimer/<id_maint>")
def supprimer_maintenance(id_maint):
    # Supprime la maintenance
    maintenance_a_supprimer = Maintenance.query.get(id_maint)
    if maintenance_a_supprimer:
        db.session.delete(maintenance_a_supprimer)
        db.session.commit()
    return redirect(url_for('gestion_maintenance'))

if __name__ == "__main__":
    app.run()