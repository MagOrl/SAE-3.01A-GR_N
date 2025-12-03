from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, HiddenField, IntegerField, widgets,DateField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional
from .models import User
from hashlib import sha256


class LoginForm(FlaskForm):
    """Formulaire de connexion."""
    Login = StringField('Identifiant')
    Password = PasswordField('Mot de passe')
    next = HiddenField()

    def get_authenticated_user(self):
        """Vérifie les identifiants et retourne l'utilisateur si valide."""
        unUser = User.query.get(self.Login.data)
        if unUser is None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None


class BudgetForm(FlaskForm):
    """Formulaire de création de budget mensuel."""
    id_budget = HiddenField("id_budg")
    valeur = IntegerField('Valeur', validators=[DataRequired()])
    dat_deb = DateField('date_deb_mois',
                        validators=[DataRequired()],
                        format='%Y-%m-%d')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PlanCampagneForm(FlaskForm):
    """Formulaire de planification de campagne."""
    id_camp = HiddenField("id_camp")
    plateform_affecte = SelectField('Role', validators=[DataRequired()])
    dat_deb = DateField('dat_deb',
                        validators=[DataRequired()],
                        format='%Y-%m-%d')
    duree_camp = IntegerField('duree_camp', validators=[DataRequired(), NumberRange(min=0)])
    lieu_fouille = StringField('lieu_fouille', validators=[DataRequired()])
    pers = MultiCheckboxField("Personel")
    def init_list_pers(self, list_pers):
        """Initialise la liste du personnel disponible."""
        self.pers.choices = [(pers.Id_pers , pers.nom_pers) for pers in list_pers ]
    def init_plateform_affecte(self, list_plat):
        """Initialise la liste des plateformes disponibles."""
        self.plateform_affecte.choices = [(plat.id_pla , plat.nom_pla) for plat in list_plat ]
    

class SequenceADNForm(FlaskForm):
    """Formulaire de saisie de séquence ADN."""
    id_ech = HiddenField("id_ech")
    sequence_adn = TextAreaField('Séquence ADN', validators=[DataRequired()], 
                                  render_kw={"placeholder": "Entrez la séquence ADN (ex: ATCGATCGATCG...)", 
                                            "rows": 10})


class AjouterSequenceForm(FlaskForm):
    """Formulaire d'ajout d'une nouvelle séquence."""
    nom_fichier = StringField('Nom du fichier', validators=[DataRequired()],
                              render_kw={"placeholder": "Ex: S001.fasta"})


class AnalyseADNForm(FlaskForm):
    """Formulaire d'analyse de mutation ADN."""
    id_ech = HiddenField("id_ech")
    type_analyse = SelectField('Type d\'analyse', 
                               choices=[
                                   ('mutation_remplacement', 'Mutation par remplacement'),
                                   ('mutation_insertion', 'Mutation par insertion'),
                                   ('mutation_deletion', 'Mutation par suppression')
                               ],
                               validators=[DataRequired()])
    taux_mutation = IntegerField('Taux de mutation (0-100%)', 
                                validators=[DataRequired(), NumberRange(min=0, max=100)],
                                default=10)


class CompareSequencesForm(FlaskForm):
    """Formulaire de comparaison de séquences ADN."""
    id_ech1 = HiddenField("id_ech1")
    id_ech2 = SelectField('Échantillon à comparer', validators=[DataRequired()], coerce=int)
    type_distance = SelectField('Type de calcul', 
                               choices=[
                                   ('distance_naive', 'Distance naïve (même longueur)'),
                                   ('distance_levenshtein', 'Distance de Levenshtein'),
                                   ('estimation_distance', 'Estimation de distance')
                               ],
                               validators=[DataRequired()])


# Roles : Chercheur, Technicien, Admin, Direction.
