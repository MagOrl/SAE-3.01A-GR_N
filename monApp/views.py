from flask import render_template, url_for, request, redirect
from .app import app
from monApp.forms import LoginForm
from flask_login import login_user


@app.route('/')
@app.route("/login/", methods=("GET", "POST"))
def login():
    if len(request.args) == 0:
        unForm = LoginForm()
        unUser = None
        if not unForm.is_submitted():
            unForm.next.data = request.args.get('next')
        elif unForm.validate_on_submit():
            unUser = unForm.get_authenticated_user()
            if unUser:
                login_user(unUser)
                next = unForm.next.data or url_for(f"{unUser.Role}_accueil")
                return redirect(next)
    return render_template("login.html", form=unForm)


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


if __name__ == "__main__":
    app.run()
