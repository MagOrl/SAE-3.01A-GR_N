from flask import Flask, render_template, request, redirect, url_for
from .app import app, db
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

@app.route('/admin/gerer_personnel/<id_pers>', methods=['GET', 'POST'])
def gerer_personnel_detail(id_pers):
    pers = personnel.query.get_or_404(id_pers)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            pers.nom_pers = request.form['nom_pers']
            db.session.commit()
        return redirect(url_for('gerer_personnel_detail', id_pers=id_pers))
    
    specialisations = db.session.query(habilitation).join(SpecialiserEn).filter(SpecialiserEn.id_pers == id_pers).all()
    participations = Participer.query.filter_by(id_pers=id_pers).all()
    return render_template('view_personel_admin.html', personnel=pers, specialisations=specialisations, participations=participations)

if __name__ == "__main__":
    app.run()