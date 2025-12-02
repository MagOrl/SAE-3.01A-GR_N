from flask import Flask,render_template, url_for, redirect, request,Response, session, flash
from monApp.forms import LoginForm
from .app import app, db
from .models import *
import random
from datetime import date, datetime, timedelta
from monApp.models import Plateforme
from flask_login import login_user,login_required,logout_user

@app.route('/')
@app.route('/index')
@app.route("/login/", methods=("GET", "POST"))
def login():
    if "user" not in session or session["user"] is None :
        unForm = LoginForm()
        unUser = None
        if not unForm.is_submitted():
            unForm.next.data = request.args.get('next')
        elif unForm.validate_on_submit():
            unUser = unForm.get_authenticated_user()
            if unUser:
                login_user(unUser)
                session["user"] = unUser
                next = unForm.next.data or url_for(f"{unUser.Role}_accueil")
                return redirect(next)
        return render_template("login.html", form=unForm)
    else:
        return redirect(url_for(f"{session["user"].Role}_accueil"))
@app.route ("/logout/")
def logout():
    logout_user()
    session["user"] = None
    return redirect ( url_for ('login'))
@app.route('/chercheur/')
@app.errorhandler(401)
@login_required
def chercheur_accueil():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")

    return render_template("Chercheur_Accueil.html")

@app.route('/chercheur/campagne/')
@app.errorhandler(401)
@login_required
def chercheur_campagne():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    plateformes = Plateforme.query.all()
    personnels = Personnel.query.all()
    return render_template("Chercheur_Planifier_Camp.html", lesPlateformes = plateformes, lesPersonnels = personnels)

@app.route('/chercheur/echantillon/')
@app.errorhandler(401)
@login_required
def chercheur_echantillon():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("Chercheur_Echantillon.html")

@app.route('/chercheur/sequence/')
@login_required
@app.errorhandler(401)
def chercheur_sequence():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("Chercheur_Sequence.html")

@app.route('/directeur/budget/')
def directeur_budget():
    return render_template("Directeur_Fixer_Budget.html")

@app.route("/admin/")
@app.errorhandler(401)
@login_required
def admin_accueil():
    if session["user"].Role != 'admin':
            return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("home_admin.html")

@app.route("/directeur/")
def directeur_accueil():
    return render_template("directeur_accueil.html",user=session["user"])        
@app.route('/admin/gerer_personnel/<id_pers>', methods=['GET', 'POST'])

def gerer_personnel_detail(id_pers):
    pers = Personnel.query.get_or_404(id_pers)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            pers.nom_pers = request.form['nom_pers']
            db.session.commit()
        return redirect(url_for('gerer_personnel_detail', id_pers=id_pers))
    
    specialisations = db.session.query(Habilitation).join(SpecialiserEn).filter(SpecialiserEn.id_pers == id_pers).all()
    participations = Participer.query.filter_by(id_pers=id_pers).all()
    return render_template('view_personel_admin.html', personnel=pers, specialisations=specialisations, participations=participations)
@app.route("/admin/gerer_personnel")
def admin_gerer_personnel():
    personnels = Personnel.query.all()
    return render_template("gerer_personnel_admin.html", personnels=personnels)
@app.route("/admin/gerer_materiel")
def admin_gerer_materiel():
    materiels = Materiel.query.join(Habilitation, Materiel.id_hab == Habilitation.id_hab).add_columns(Habilitation.nom_hab).all()
    return render_template("gerer_materiel_admin.html", materiels=materiels)

#------------------------------------------------------------------------------------------------------------------------------------------

# Page d'accueil technicien
@app.errorhandler(401)
@login_required
@app.route("/technicien/")
def technicien_accueil():
    if session["user"].Role != 'technicien':
            return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("accueil_technicien.html")

#-----------------------------------------------------------------

# Page de menu gestion des changements de technicien
@app.route("/technicien/gestion_changement_technicien/")
def gestion_changement_technicien():
    return render_template("gestion_changement_technicien.html")

#------------------------------

# Page de gestion du matériel du technicien
@app.route("/technicien/gestion_changement_technicien/gerer_materiel")
def technicien_gerer_materiel():
    materiels = Materiel.query.join(Habilitation, Materiel.id_hab == Habilitation.id_hab).add_columns(Habilitation.nom_hab).all()
    return render_template("gerer_materiel_technicien.html", materiels=materiels)

#------------------------------
# Page de gestion du personnel du technicien

@app.route("/technicien/gestion_changement_technicien/gerer_personnel/")
def technicien_gerer_personnel():
    personnels = Personnel.query.all()
    return render_template("gerer_personnel_technicien.html", personnels=personnels)

#--------------

@app.route("/technicien/gestion_changement_technicien/gerer_personnel/<id_pers>", methods=['GET', 'POST'])
def technicien_gerer_personnel_detail(id_pers):
    pers = Personnel.query.get_or_404(id_pers)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            pers.nom_pers = request.form['nom_pers']
            db.session.commit()
            flash('Nom du personnel mis à jour avec succès.', 'success')
        return redirect(url_for('technicien_gerer_personnel_detail', id_pers=id_pers))
    
    specialisations = db.session.query(Habilitation).join(SpecialiserEn).filter(SpecialiserEn.id_pers == id_pers).all()
    participations = Participer.query.filter_by(id_pers=id_pers).all()
    return render_template('view_personnel_technicien.html', personnel=pers, specialisations=specialisations, participations=participations)

#--------------

@app.route('/technicien/gestion_changement_technicien/gerer_personnel/<id_pers>/supprimer', methods=['POST'])
def technicien_supprimer_personnel(id_pers):
    pers = Personnel.query.get_or_404(id_pers)
    SpecialiserEn.query.filter_by(id_pers=id_pers).delete(synchronize_session=False)
    Participer.query.filter_by(id_pers=id_pers).delete(synchronize_session=False)
    db.session.delete(pers)
    db.session.commit()
    return redirect(url_for('technicien_gerer_personnel'))

#--------------

@app.route('/technicien/gestion_changement_technicien/gerer_materiel/<id_mat>', methods=['GET', 'POST'])
def technicien_gerer_materiel_detail(id_mat):
    materiel = Materiel.query.get_or_404(id_mat)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            materiel.nom_mat = request.form['nom_mat']
            flash('Nom du matériel mis à jour avec succès.', 'success')
        elif action == 'update_hab':
            nouvelle_hab = request.form.get('id_hab')
            if nouvelle_hab and Habilitation.query.get(nouvelle_hab):
                materiel.id_hab = nouvelle_hab
                flash("Habilitation du matériel mise à jour avec succès.", 'success')
        db.session.commit()
        return redirect(url_for('technicien_gerer_materiel_detail', id_mat=id_mat))

    habilitation = Habilitation.query.get(materiel.id_hab)
    toutes_habilitations = Habilitation.query.all()
    plateformes = db.session.query(Plateforme).join(Utiliser, Utiliser.id_pla == Plateforme.id_pla).filter(Utiliser.id_mat == id_mat).all()
    return render_template(
        'view_materiel_technicien.html',
        materiel=materiel,
        habilitation=habilitation,
        habilitations=toutes_habilitations,
        plateformes=plateformes,
    )

#--------------
    
@app.route('/technicien/gestion_changement_technicien/gerer_materiel/<id_mat>/supprimer', methods=['POST'])
def technicien_supprimer_materiel(id_mat):
    materiel = Materiel.query.get_or_404(id_mat)
    Utiliser.query.filter_by(id_mat=id_mat).delete(synchronize_session=False)
    db.session.delete(materiel)
    db.session.commit()
    return redirect(url_for('technicien_gerer_materiel'))



#-----------------------------------------------------------------

# Page de gestion des maintenances
@app.route("/technicien/gestion_maintenance/")
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

#------------------------------

# Méthode pour ajouter une Maintenance
@app.route("/technicien/gestion_maintenance/ajouter/", methods=["GET", "POST"])
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
        flash("Maintenance ajoutée avec succès.", 'success')
        return redirect(url_for('ajouter_maintenance'))
    
    
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

#------------------------------

# Méthode pour supprimer une Maintenance
@app.route("/technicien/gestion_maintenance/supprimer/<id_maint>")
def supprimer_maintenance(id_maint):
    # Supprime la maintenance
    maintenance_a_supprimer = Maintenance.query.get(id_maint)
    if maintenance_a_supprimer:
        db.session.delete(maintenance_a_supprimer)
        db.session.commit()
    return redirect(url_for('gestion_maintenance'))

#------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()
