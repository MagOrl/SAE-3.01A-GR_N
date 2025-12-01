from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, DateField, PasswordField
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
    
# Roles : Chercheur, Technicien, Admin, Direction. 

class FormCamp(FlaskForm):
    idCamp = HiddenField('id_camp')
    debCamp = DateField('date_deb_camp', validators =[DataRequired()])
    dureeCamp = IntegerField('duree', validators =[DataRequired()])
    