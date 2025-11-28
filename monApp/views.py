from flask import render_template, url_for, request, redirect, Response, session
from .app import app
from monApp.forms import LoginForm
from flask_login import login_user,login_required,logout_user
from monApp.models import User
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
    return render_template("Chercheur_Campagne.html")

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

if __name__ == "__main__":
    app.run()
