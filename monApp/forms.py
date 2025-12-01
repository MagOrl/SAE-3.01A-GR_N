from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField, HiddenField,IntegerField,DateField
from wtforms.validators import DataRequired
from . models import User
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
    valeur = IntegerField('Valeur',validators =[DataRequired()])
    dat_deb = DateField('date_deb_mois', validators =[DataRequired()],format='%Y-%m-%d')
    
# Roles : Chercheur, Technicien, Admin, Direction. 