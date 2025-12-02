from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, HiddenField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired
from .models import User
from hashlib import sha256


class LoginForm(FlaskForm):
    Login = StringField('Identifiant')
    Password = PasswordField('Mot de passe')
    next = HiddenField()

    def get_authenticated_user(self):
        unUser = User.query.get(self.Login.data)
        if unUser is None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None


class BudgetForm(FlaskForm):
    id_budget = HiddenField("id_budg")
    valeur = IntegerField('Valeur', validators=[DataRequired()])
    dat_deb = DateField('date_deb_mois',
                        validators=[DataRequired()],
                        format='%Y-%m-%d')


class PlanCampagneForm(FlaskForm):
    id_camp = HiddenField("id_camp")
    plateform_affecte = SelectField('Role', validators=[DataRequired()])
    dat_deb = DateField('date_deb',
                        validators=[DataRequired()],
                        format='%Y-%m-%d')
    duree_camp = IntegerField('duree_camp', validators=[DataRequired()])
    lieu_fouille = StringField('lieu_fouille', validators=[DataRequired()])
    list_pers = []
    


# Roles : Chercheur, Technicien, Admin, Direction.
