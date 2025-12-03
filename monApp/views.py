from flask import render_template, url_for, redirect, request,Response, session
from monApp.forms import LoginForm, BudgetForm,PlanCampagneForm, SequenceADNForm, AjouterSequenceForm, AnalyseADNForm, CompareSequencesForm
from .app import app, db
from .models import *
import random
from datetime import date, datetime, timedelta
from monApp.models import Plateforme
from flask_login import login_user,login_required,logout_user
from sqlalchemy import extract
import sys
import os
from sqlalchemy import func

# Import DNA analysis functions from exercice.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code', 'ALGO'))
from exercice import (
    mutation_par_remplacement, 
    mutation_par_insertion, 
    mutation_par_deletion,
    estimation_distance_mutation,
    sequence_levenshtein,
    estimation_distance
)

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
@login_required
def chercheur_accueil():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")

    return render_template("chercheur_accueil.html",user=session["user"])

@app.route('/chercheur/campagne/')
@login_required
def chercheur_campagne():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    formCamp = PlanCampagneForm(request.form)
    formCamp.init_list_pers(Personnel.query.all())
    formCamp.init_plateform_affecte(Plateforme.query.all())
    return render_template("chercheur_planifier_camp.html",form=formCamp)

@app.route('/chercheur/campagne/insert',methods=("POST",))
def insert_campagne():
    formCamp = PlanCampagneForm(request.form)
    formCamp.init_list_pers(Personnel.query.all())
    formCamp.init_plateform_affecte(Plateforme.query.all())

    if formCamp.validate_on_submit():
        mois_entrer = f"{str(formCamp.dat_deb.data).split("-")[0]}-{str(formCamp.dat_deb.data).split("-")[1]}"
        annee, mois = map(int, mois_entrer.split("-"))
        budget_mois = Budget.query.filter(extract('year', Budget.date_deb_mois) == annee).filter(extract('month', Budget.date_deb_mois) == mois).first()
        if budget_mois is None:
            return Response(f"<script>alert('Aucun budget défini pour {mois_entrer}. Veuillez demander un budget à votre directeur pour ce mois avant de planifier une campagne.'); window.location.href='{url_for('chercheur_campagne')}';</script>", mimetype='text/html')
        CampId = Campagne.query.count() + 1
        nouv_camp = Campagne(id_camp=CampId,id_pla=formCamp.plateform_affecte.data,duree=formCamp.duree_camp.data, 
                                 date_deb_camp=formCamp.dat_deb.data,nom_lieu_fouille=formCamp.lieu_fouille.data,id_budg=budget_mois.id_budg)
        db.session.add(nouv_camp)
        for pers in formCamp.pers.data:
            try:
                db.session.add(Participer(Id_pers=pers,id_camp=CampId))
            except HabilitationManquanteError as e:
                pers_obj = Personnel.query.get(pers)
                nom = pers_obj.nom_pers if pers_obj else f"ID {pers}"
                return Response(
                    f"<script>alert('Le personnel {nom} ne possède pas l’habilitation requise pour participer à cette campagne sur la plateforme sélectionnée. Veuillez vérifier ses habilitations ou sélectionner un autre personnel.'); window.location.href='{url_for('chercheur_campagne')}';</script>",
                    mimetype='text/html'
                )
        db.session.commit()
        return redirect(url_for('chercheur_campagne'))  
    else:
        print(formCamp.errors)  
    return redirect(url_for('chercheur_campagne'))

@app.route('/chercheur/echantillon/')
@login_required
def chercheur_echantillon():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("Chercheur_Echantillon.html")

@app.route('/chercheur/sequence/')
@login_required
def chercheur_sequence():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return render_template("chercheur_sequence.html", campagnes=[], error="Votre compte n'est pas lié à un personnel. Contactez l'administrateur.")
    
    participations = Participer.query.filter_by(Id_pers=user.Id_pers).all()
    campagnes_data = []
    
    for part in participations:
        campagne = Campagne.query.get(part.id_camp)
        if campagne:
            plateforme = Plateforme.query.get(campagne.id_pla)
            extractions = Extraire.query.filter_by(id_camp=campagne.id_camp).all()
            nb_echantillons = len(extractions)
            
            campagnes_data.append({
                'campagne': campagne,
                'plateforme': plateforme,
                'nb_echantillons': nb_echantillons
            })
    
    return render_template("chercheur_sequence.html", campagnes=campagnes_data, user=session["user"])

@app.route('/chercheur/campagne/<int:id_camp>')
@login_required
def chercheur_detail_campagne(id_camp):
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html", error='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return render_template("access_denied.html", error='403', reason="Vous ne participez pas à cette campagne.")
    
    campagne = Campagne.query.get_or_404(id_camp)
    plateforme = Plateforme.query.get(campagne.id_pla)
    budget = Budget.query.get(campagne.id_budg)
    
    participations = Participer.query.filter_by(id_camp=id_camp).all()
    participants = [Personnel.query.get(p.Id_pers) for p in participations]
    
    extractions = Extraire.query.filter_by(id_camp=id_camp).all()
    sequences_data = []
    for extraction in extractions:
        sequence = Sequence.query.get(extraction.id_seq)
        echantillons = Echantillon.query.filter_by(id_seq=sequence.id_seq).all()
        sequences_data.append({
            'sequence': sequence,
            'echantillons': echantillons
        })
    
    forms = {}
    for seq_data in sequences_data:
        for echantillon in seq_data['echantillons']:
            form = SequenceADNForm()
            form.id_ech.data = echantillon.id_ech
            if echantillon.sequence_adn:
                form.sequence_adn.data = echantillon.sequence_adn
            forms[echantillon.id_ech] = form
    
    return render_template("chercheur_detail_campagne.html", 
                         campagne=campagne, 
                         plateforme=plateforme,
                         budget=budget,
                         participants=participants,
                         sequences=sequences_data,
                         forms=forms,
                         user=session["user"])

@app.route('/chercheur/campagne/<int:id_camp>/upload_adn/<int:id_ech>', methods=['GET', 'POST'])
@login_required
def upload_sequence_adn(id_camp, id_ech):
    if session["user"].Role != 'chercheur':
        return redirect(url_for('chercheur_sequence'))
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return redirect(url_for('chercheur_sequence'))
    
    echantillon = Echantillon.query.get_or_404(id_ech)
    extraction = Extraire.query.filter_by(id_camp=id_camp, id_seq=echantillon.id_seq).first()
    if not extraction:
        return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
    
    form = SequenceADNForm()
    
    if request.method == 'GET':
        form.id_ech.data = id_ech
        if echantillon.sequence_adn:
            form.sequence_adn.data = echantillon.sequence_adn
    
    if form.validate_on_submit():
        try:
            echantillon.sequence_adn = form.sequence_adn.data
            db.session.commit()
            return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
        except Exception as e:
            db.session.rollback()
    
    campagne = Campagne.query.get_or_404(id_camp)
    sequence = Sequence.query.get(echantillon.id_seq)
    
    return render_template("chercheur_upload_adn.html", 
                         form=form,
                         echantillon=echantillon,
                         sequence=sequence,
                         campagne=campagne,
                         user=session["user"])

@app.route('/chercheur/campagne/<int:id_camp>/ajouter_sequence', methods=['GET', 'POST'])
@login_required
def ajouter_sequence(id_camp):
    if session["user"].Role != 'chercheur':
        return redirect(url_for('chercheur_sequence'))
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return redirect(url_for('chercheur_sequence'))
    
    campagne = Campagne.query.get_or_404(id_camp)
    form = AjouterSequenceForm()
    
    if form.validate_on_submit():
        try:
            id_seq = Sequence.query.count() + 1
            nouvelle_sequence = Sequence(id_seq=id_seq, nom_fichier=form.nom_fichier.data)
            db.session.add(nouvelle_sequence)
            
            extraction = Extraire(id_camp=id_camp, id_seq=id_seq)
            db.session.add(extraction)
            
            id_ech = Echantillon.query.count() + 1
            echantillon = Echantillon(id_ech=id_ech, id_seq=id_seq, commentaire="Échantillon par défaut")
            db.session.add(echantillon)
            
            db.session.commit()
            return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
        except Exception as e:
            db.session.rollback()
    
    return render_template("chercheur_ajouter_sequence.html", 
                         form=form,
                         campagne=campagne,
                         user=session["user"])

@app.route('/chercheur/campagne/<int:id_camp>/supprimer_sequence/<int:id_seq>')
@login_required
def supprimer_sequence(id_camp, id_seq):
    if session["user"].Role != 'chercheur':
        return redirect(url_for('chercheur_sequence'))
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return redirect(url_for('chercheur_sequence'))
    
    extraction = Extraire.query.filter_by(id_camp=id_camp, id_seq=id_seq).first()
    if not extraction:
        return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
    
    try:
        Echantillon.query.filter_by(id_seq=id_seq).delete()
        
        Espece.query.filter_by(id_seq=id_seq).delete()
        
        db.session.delete(extraction)
        
        sequence = Sequence.query.get(id_seq)
        if sequence:
            db.session.delete(sequence)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
    return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))

@app.route('/chercheur/campagne/<int:id_camp>/analyser_adn/<int:id_ech>', methods=['GET', 'POST'])
@login_required
def analyser_adn(id_camp, id_ech):
    if session["user"].Role != 'chercheur':
        return redirect(url_for('chercheur_sequence'))
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return redirect(url_for('chercheur_sequence'))
    
    echantillon = Echantillon.query.get_or_404(id_ech)
    extraction = Extraire.query.filter_by(id_camp=id_camp, id_seq=echantillon.id_seq).first()
    if not extraction:
        return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
    
    if not echantillon.sequence_adn:
        return redirect(url_for('upload_sequence_adn', id_camp=id_camp, id_ech=id_ech))
    
    form = AnalyseADNForm()
    
    if form.validate_on_submit():
        try:
            sequence_originale = echantillon.sequence_adn
            type_analyse = form.type_analyse.data
            p = form.taux_mutation.data / 100.0  # Convertir de pourcentage à décimal
            
            sequence_resultat = None
            
            if type_analyse == 'mutation_remplacement':
                sequence_resultat = mutation_par_remplacement(sequence_originale, p)
            elif type_analyse == 'mutation_insertion':
                sequence_resultat = mutation_par_insertion(sequence_originale, p)
            elif type_analyse == 'mutation_deletion':
                sequence_resultat = mutation_par_deletion(sequence_originale, p)
            
            if sequence_resultat is None:
                return redirect(url_for('analyser_adn', id_camp=id_camp, id_ech=id_ech))
            
            id_res = Resultat.query.count() + 1
            nouveau_resultat = Resultat(
                id_res=id_res,
                id_ech=id_ech,
                id_camp=id_camp,
                type_analyse=type_analyse,
                parametre=p,
                sequence_originale=sequence_originale,
                sequence_resultat=sequence_resultat
            )
            db.session.add(nouveau_resultat)
            db.session.commit()
            
            return redirect(url_for('chercheur_resultats'))
        except Exception as e:
            db.session.rollback()
    
    campagne = Campagne.query.get_or_404(id_camp)
    sequence = Sequence.query.get(echantillon.id_seq)
    
    return render_template("chercheur_analyser_adn.html",
                         form=form,
                         echantillon=echantillon,
                         sequence=sequence,
                         campagne=campagne,
                         user=session["user"])

@app.route('/chercheur/campagne/<int:id_camp>/comparer_sequences/<int:id_ech>', methods=['GET', 'POST'])
@login_required
def comparer_sequences(id_camp, id_ech):
    if session["user"].Role != 'chercheur':
        return redirect(url_for('chercheur_sequence'))
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return redirect(url_for('chercheur_sequence'))
    
    participation = Participer.query.filter_by(Id_pers=user.Id_pers, id_camp=id_camp).first()
    if not participation:
        return redirect(url_for('chercheur_sequence'))
    
    echantillon1 = Echantillon.query.get_or_404(id_ech)
    extraction = Extraire.query.filter_by(id_camp=id_camp, id_seq=echantillon1.id_seq).first()
    if not extraction:
        return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
    
    if not echantillon1.sequence_adn:
        return redirect(url_for('upload_sequence_adn', id_camp=id_camp, id_ech=id_ech))
    
    # Get all echantillons from this campaign
    extractions = Extraire.query.filter_by(id_camp=id_camp).all()
    echantillons_campagne = []
    for ext in extractions:
        echs = Echantillon.query.filter_by(id_seq=ext.id_seq).all()
        for ech in echs:
            if ech.id_ech != id_ech and ech.sequence_adn:
                echantillons_campagne.append(ech)
    
    if not echantillons_campagne:
        return redirect(url_for('chercheur_detail_campagne', id_camp=id_camp))
    
    form = CompareSequencesForm()
    form.id_ech2.choices = [(ech.id_ech, f"Échantillon {ech.id_ech} - Séquence {ech.id_seq}") for ech in echantillons_campagne]
    
    if form.validate_on_submit():
        try:
            echantillon2 = Echantillon.query.get(form.id_ech2.data)
            if not echantillon2:
                return redirect(url_for('comparer_sequences', id_camp=id_camp, id_ech=id_ech))
            
            sequence1 = echantillon1.sequence_adn
            sequence2 = echantillon2.sequence_adn
            type_distance = form.type_distance.data
            
            valeur_distance = None
            
            if type_distance == 'distance_naive':
                valeur_distance = estimation_distance_mutation(sequence1, sequence2)
                if valeur_distance is None:
                    return redirect(url_for('comparer_sequences', id_camp=id_camp, id_ech=id_ech))
            elif type_distance == 'distance_levenshtein':
                valeur_distance = sequence_levenshtein(sequence1, sequence2)
            elif type_distance == 'estimation_distance':
                valeur_distance = estimation_distance(sequence1, sequence2)
            
            id_res = Resultat.query.count() + 1
            nouveau_resultat = Resultat(
                id_res=id_res,
                id_ech=id_ech,
                id_camp=id_camp,
                type_analyse=type_distance,
                sequence_originale=sequence1,
                valeur_distance=valeur_distance,
                id_ech_compare=echantillon2.id_ech
            )
            db.session.add(nouveau_resultat)
            db.session.commit()
            
            return redirect(url_for('chercheur_resultats'))
        except Exception as e:
            db.session.rollback()
    
    campagne = Campagne.query.get_or_404(id_camp)
    sequence = Sequence.query.get(echantillon1.id_seq)
    
    return render_template("chercheur_comparer_sequences.html",
                         form=form,
                         echantillon=echantillon1,
                         sequence=sequence,
                         campagne=campagne,
                         user=session["user"])

@app.route('/chercheur/resultats/')
@login_required
def chercheur_resultats():
    if session["user"].Role != 'chercheur':
        return render_template("access_denied.html", error='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    
    user = User.query.get(session["user"].Login)
    if not user.Id_pers:
        return render_template("chercheur_resultats.html", resultats=[], error="Votre compte n'est pas lié à un personnel. Contactez l'administrateur.")
    
    participations = Participer.query.filter_by(Id_pers=user.Id_pers).all()
    id_camps = [p.id_camp for p in participations]
    
    resultats = Resultat.query.filter(Resultat.id_camp.in_(id_camps)).order_by(Resultat.date_analyse.desc()).all()
    
    resultats_data = []
    for res in resultats:
        campagne = Campagne.query.get(res.id_camp)
        echantillon = Echantillon.query.get(res.id_ech)
        sequence = Sequence.query.get(echantillon.id_seq) if echantillon else None
        echantillon_compare = Echantillon.query.get(res.id_ech_compare) if res.id_ech_compare else None
        
        resultats_data.append({
            'resultat': res,
            'campagne': campagne,
            'echantillon': echantillon,
            'sequence': sequence,
            'echantillon_compare': echantillon_compare
        })
    
    return render_template("chercheur_resultats.html", 
                         resultats=resultats_data,
                         user=session["user"])

@app.route("/directeur/")
@login_required
def directeur_accueil():
    if session["user"].Role != 'directeur':
            return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("directeur_accueil.html",user=session["user"])        

@app.route('/directeur/budget/')
@login_required
def directeur_budget():
    if session["user"].Role != 'directeur': 
            return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    budgForm = BudgetForm()
    return render_template("directeur_budget.html",user=session["user"],form=budgForm)

@app.route('/directeur/budget/cree_budget',methods=("POST",))
@login_required
def insert_budget():
    budgForm = BudgetForm(request.form)
    if budgForm.validate_on_submit():
        budgId = Budget.query.count() + 1
        insert_budget = Budget(id_budg=budgId,valeur=budgForm.valeur.data, date_deb_mois=budgForm.dat_deb.data)
        db.session.add(insert_budget)
        db.session.commit()
        return redirect(url_for('directeur_budget'))  
    else:
        print(budgForm.errors)  
    return render_template("directeur_budget.html",user=session["user"],form=budgForm)
@app.route("/admin/")
@login_required
def admin_accueil():
    if session["user"].Role != 'admin':
            return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("home_admin.html", admin=session.get("user"))

@app.route("/admin/gerer_personnel",methods=["POST","GET"])
@login_required
def admin_gerer_personnel():
    if request.method == 'POST':
        max_id = db.session.query(func.max(Personnel.Id_pers)).scalar()
        Id_pers = (max_id or 0) + 1
        nom_pers = request.form.get('nom_pers', '').strip()
        nouveau_pers = Personnel(Id_pers=Id_pers, nom_pers=nom_pers)
        db.session.add(nouveau_pers)
        db.session.commit()
        return redirect(url_for('admin_gerer_personnel'))
    personnels = Personnel.query.all()
    return render_template("gerer_personnel_admin.html", personnels=personnels)

@app.route('/admin/gerer_personnel/<Id_pers>', methods=['GET', 'POST'])
@login_required
def gerer_personnel_detail(Id_pers):
    pers = Personnel.query.get_or_404(Id_pers)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            nouveau_nom = request.form.get('nom_pers', '').strip()
            if nouveau_nom:
                pers.nom_pers = nouveau_nom
                db.session.commit()
        elif action == 'add_hab':
            id_hab = request.form.get('id_hab')
            if id_hab and Habilitation.query.get(id_hab):
                deja_present = SpecialiserEn.query.filter_by(Id_pers=Id_pers, id_hab=id_hab).first()
                if not deja_present:
                    print('Ce personnel possède déjà cette habilitation.')
                else:
                    specialisation = SpecialiserEn(id_hab=id_hab, Id_pers=Id_pers)
                    db.session.add(specialisation)
                    db.session.commit()
        elif action == 'remove_hab':
            id_hab = request.form.get('id_hab')
            lien = SpecialiserEn.query.filter_by(Id_pers=Id_pers, id_hab=id_hab).first()
            if lien:
                db.session.delete(lien)
                db.session.commit()
        return redirect(url_for('gerer_personnel_detail', Id_pers=Id_pers))
    
    specialisations = db.session.query(Habilitation).join(SpecialiserEn).filter(SpecialiserEn.Id_pers == Id_pers).all()
    participations = Participer.query.filter_by(Id_pers=Id_pers).all()
    habilitations = Habilitation.query.all()
    return render_template('view_personel_admin.html', personnel=pers, specialisations=specialisations, participations=participations, habilitations=habilitations)


@app.route('/admin/gerer_personnel/<Id_pers>/supprimer', methods=['POST'])
@login_required
def supprimer_personnel(Id_pers):
    pers = Personnel.query.get_or_404(Id_pers)
    SpecialiserEn.query.filter_by(Id_pers=Id_pers).delete(synchronize_session=False)
    Participer.query.filter_by(Id_pers=Id_pers).delete(synchronize_session=False)
    db.session.delete(pers)
    db.session.commit()
    return redirect(url_for('admin_gerer_personnel'))


@app.route('/admin/gerer_materiel/<id_mat>', methods=['GET', 'POST'])
def gerer_materiel_detail(id_mat):
    materiel = Materiel.query.get_or_404(id_mat)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            materiel.nom_mat = request.form['nom_mat']
        elif action == 'update_hab':
            nouvelle_hab = request.form.get('id_hab')
            if nouvelle_hab and Habilitation.query.get(nouvelle_hab):
                materiel.id_hab = nouvelle_hab
        db.session.commit()
        return redirect(url_for('gerer_materiel_detail', id_mat=id_mat))

    habilitation = Habilitation.query.get(materiel.id_hab)
    toutes_habilitations = Habilitation.query.all()
    plateformes = db.session.query(Plateforme).join(Utiliser, Utiliser.id_pla == Plateforme.id_pla).filter(Utiliser.id_mat == id_mat).all()
    return render_template(
        'view_materiel_admin.html',
        materiel=materiel,
        habilitation=habilitation,
        habilitations=toutes_habilitations,
        plateformes=plateformes,
    )


@app.route('/admin/gerer_materiel/<id_mat>/supprimer', methods=['POST'])
@login_required
def supprimer_materiel(id_mat):
    materiel = Materiel.query.get_or_404(id_mat)
    Utiliser.query.filter_by(id_mat=id_mat).delete(synchronize_session=False)
    db.session.delete(materiel)
    db.session.commit()
    return redirect(url_for('admin_gerer_materiel'))

@app.route("/admin/gerer_materiel", methods=['GET', 'POST'])
@login_required
def admin_gerer_materiel():
    if request.method == 'POST':
        nom_mat = request.form.get('nom_mat', '').strip()
        id_hab = request.form.get('id_hab') or None
        max_id = db.session.query(func.max(Materiel.id_mat)).scalar()
        id_mat = (max_id or 0) + 1

        nouvelle = Materiel(id_mat=id_mat, id_hab=id_hab, nom_mat=nom_mat)
        db.session.add(nouvelle)
        db.session.commit()
        return redirect(url_for('admin_gerer_materiel'))
    materiels = Materiel.query.join(Habilitation, Materiel.id_hab == Habilitation.id_hab).add_columns(Habilitation.nom_hab).all()
    habilitations = Habilitation.query.all()
    return render_template("gerer_materiel_admin.html", materiels=materiels, habilitations=habilitations)
@app.route("/technicien/")
@login_required
def technicien_accueil():
    if session["user"].Role != 'technicien':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    return render_template("technicien_accueil.html",user=session["user"])

@app.route("/technicien/gestion_maintenance/")
@login_required
def gestion_maintenance():
    if session["user"].Role != 'technicien':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    maintenances_passees = Maintenance.query.filter(Maintenance.date_fin_maint < date.today()).all()
    for m in maintenances_passees:
        db.session.delete(m)
    if maintenances_passees:
        db.session.commit()

    donnees_plateformes = []
    for m in Maintenance.query.order_by(Maintenance.date_deb_maint).all():
        p = Plateforme.query.get(m.id_pla)
        
        jours_restants = (m.date_deb_maint - date.today()).days
            
        donnees_plateformes.append((m.id_maint, p.id_pla, p.nom_pla, m.date_deb_maint, m.date_fin_maint, jours_restants))
            
    return render_template("gestion_maintenance.html", plateformes=donnees_plateformes)

@app.route("/technicien/ajouter/", methods=["GET", "POST"])
@login_required
def ajouter_maintenance():
    if session["user"].Role != 'technicien':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")
    if request.method == "POST":
        id_pla = request.form["id_pla"]
        date_deb = request.form["date_deb_maint"]
        date_fin = request.form["date_fin_maint"]
        max_id = db.session.query(func.max(Maintenance.id_maint)).scalar()
        id_maint = (max_id or 0) + 1

        date_deb = datetime.strptime(date_deb, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()

        nouvelle_maintenance = Maintenance(id_maint=id_maint,id_pla= id_pla,date_deb_maint= date_deb, date_fin_maint =date_fin)
        db.session.add(nouvelle_maintenance)
        db.session.commit()
        
        return redirect(url_for('gestion_maintenance'))
    
    plateformes = []
    for p in Plateforme.query.all():
        last_maint = Maintenance.query.filter_by(id_pla=p.id_pla).order_by(Maintenance.date_fin_maint.desc()).first()
        if last_maint:
            next_start = last_maint.date_fin_maint + timedelta(days=p.inter_mainte)
        else:
            next_start = date.today()
        
        duree = random.choice([1, 2])
        next_end = next_start + timedelta(days=duree)
        
        plateformes.append({
            'id_pla': p.id_pla,
            'nom_pla': p.nom_pla,
            'next_start': next_start,
            'next_end': next_end
        })
        
    return render_template("ajouter_maintenance.html", plateformes=plateformes)

@app.route("/technicien/supprimer/<id_maint>")
@login_required
def supprimer_maintenance(id_maint):
    if session["user"].Role != 'technicien':
        return render_template("access_denied.html",error ='401', reason="Vous n'avez pas les droits d'accès à cette page.")

    maintenance_a_supprimer = Maintenance.query.get(id_maint)
    if maintenance_a_supprimer:
        db.session.delete(maintenance_a_supprimer)
        db.session.commit()
    return redirect(url_for('gestion_maintenance'))

if __name__ == "__main__":
    app.run()
