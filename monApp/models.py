from .app import db
from sqlalchemy.orm import validates
from datetime import timedelta
from sqlalchemy import func
from flask_login import UserMixin
from .app import login_manager


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


class User(db.Model, UserMixin):
    Login = db.Column(db.String(50), primary_key=True)
    Password = db.Column(db.String(64))
    Nom = db.Column(db.String(20))
    Prenom = db.Column(db.String(20))
    Role = db.Column(db.String(15))

    def get_id(self):
        return self.Login

    def __str__(self):
        return f"User: {self.Login}"

    def __repr__(self):
        return f"<User {self.Login}>"


class Habilitation(db.Model):
    id_hab = db.Column(db.Integer, primary_key=True)
    nom_hab = db.Column(db.String(20))

    def __init__(self, id_hab, nom_hab):
        self.id_hab = id_hab
        self.nom_hab = nom_hab

    def __repr__(self):
        return "<habilitation (%s) %s>" % (self.id_hab, self.nom_hab)


class Personnel(db.Model):
    id_pers = db.Column(db.Integer, primary_key=True)
    nom_pers = db.Column(db.String(20))

    def __init__(self, id_pers, nom_pers):
        self.id_pers = id_pers
        self.nom_pers = nom_pers

    def __repr__(self):
        return "<personnel (%s) %s>" % (self.id_pers, self.nom_pers)


class Plateforme(db.Model):
    id_pla = db.Column(db.Integer, primary_key=True)
    nom_pla = db.Column(db.String(20))
    nb_pers_nec = db.Column(db.Integer)
    cout_exploi_jour = db.Column(db.Float)
    inter_mainte = db.Column(db.Integer)
    jours_av_mainte = db.Column(db.Integer)

    def __init__(self, id_pla, nom_pla, nb_pers_nec, cout_exploi_jour,
                 inter_mainte, jours_av_mainte):
        self.id_pla = id_pla
        self.nom_pla = nom_pla
        self.nb_pers_nec = nb_pers_nec
        self.cout_exploi_jour = cout_exploi_jour
        self.inter_mainte = inter_mainte
    
    def __repr__(self):
        return "<Plateforme (%s) %s>" % (self.id_pla, self.nom_pla)

class Maintenance(db.Model):
    id_maint = db.Column(db.Integer, primary_key=True)
    id_pla = db.Column(db.Integer, db.ForeignKey('plateforme.id_pla'))
    date_deb_maint = db.Column(db.Date)
    date_fin_maint = db.Column(db.Date)
    
    def __init__(self, id_maint, id_pla, date_deb_maint, date_fin_maint):
        self.id_maint = id_maint
        self.id_pla = id_pla
        self.date_deb_maint = date_deb_maint
        self.date_fin_maint = date_fin_maint
    
    def __repr__(self):
        return "<Maintenance (%s) %s>" % (self.id_maint, self.id_pla)

class OperationMaintenance(db.Model):
    id_op_maint = db.Column(db.Integer, primary_key=True)
    id_pla = db.Column(db.Integer, db.ForeignKey('plateforme.id_pla'))
    date_maintenance = db.Column(db.Date)
    
    def __init__(self, id_op_maint, id_pla, date_maintenance):
        self.id_op_maint = id_op_maint
        self.id_pla = id_pla
        self.date_maintenance = date_maintenance
    
    def __repr__(self):
        return "<OperationMaintenance (%s) %s>" % (self.id_op_maint, self.id_pla)

class Materiel(db.Model):
    id_mat = db.Column(db.Integer, primary_key=True)
    id_hab = db.Column(db.Integer, db.ForeignKey('habilitation.id_hab'))
    nom_mat = db.Column(db.String(20))

    def __init__(self, id_mat, id_hab, nom_mat):
        self.id_mat = id_mat
        self.id_hab = id_hab
        self.nom_mat = nom_mat

    def __repr__(self):
        return "<Materiel (%s, %s, %s)>" % (self.id_mat, self.id_hab,
                                            self.nom_mat)


class Utiliser(db.Model):
    id_mat = db.Column(db.Integer,
                       db.ForeignKey('materiel.id_mat'),
                       primary_key=True)
    id_pla = db.Column(db.Integer,
                       db.ForeignKey('plateforme.id_pla'),
                       primary_key=True)

    def __init__(self, id_mat, id_pla):
        self.id_mat = id_mat
        self.id_pla = id_pla

    def __repr__(self):
        return "<Utiliser (%s, %s)>" % (self.id_mat, self.id_pla)


class Necessiter(db.Model):
    id_hab = db.Column(db.Integer,
                       db.ForeignKey('habilitation.id_hab'),
                       primary_key=True)
    id_pla = db.Column(db.Integer,
                       db.ForeignKey('plateforme.id_pla'),
                       primary_key=True)

    def __init__(self, id_hab, id_pla):
        self.id_hab = id_hab
        self.id_pla = id_pla

    def __repr__(self):
        return "<Necessiter (%s, %s)>" % (self.id_hab, self.id_pla)


class SpecialiserEn(db.Model):
    id_hab = db.Column(db.Integer,
                       db.ForeignKey('habilitation.id_hab'),
                       primary_key=True)
    id_pers = db.Column(db.Integer,
                        db.ForeignKey('personnel.id_pers'),
                        primary_key=True)

    def __init__(self, id_hab, id_pers):
        self.id_hab = id_hab
        self.id_pers = id_pers

    def __repr__(self):
        return "<SpecialiserEn (%s, %s)>" % (self.id_hab, self.id_pers)


class Budget(db.Model):
    id_budg = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Float)
    date_deb_mois = db.Column(db.Date)


    def __repr__(self):
        return "<Budget (%s, %s, %s)>" % (self.id_budg, self.valeur,
                                          self.date_deb_mois)


class Campagne(db.Model):
    id_camp = db.Column(db.Integer, primary_key=True)
    duree = db.Column(db.Integer)
    date_deb_camp = db.Column(db.Date)
    id_pla = db.Column(db.Integer, db.ForeignKey('plateforme.id_pla'))
    id_budg = db.Column(db.Integer, db.ForeignKey('budget.id_budg'))
    nom_lieu_fouille = db.Column(db.String(40))

    def __init__(self, id_camp, duree, date_deb_camp, id_pla, id_budg):
        self.id_camp = id_camp
        self.duree = duree
        self.date_deb_camp = date_deb_camp
        self.id_pla = id_pla
        self.id_budg = id_budg

    def __repr__(self):
        return "<Campagne (%s)>" % (self.id_camp)

    @validates('id_pla', 'date_deb_camp', 'duree', 'id_budg')
    def validate_campagne(self, key, value):
        if key == 'id_pla' and hasattr(
                self, 'date_deb_camp') and self.date_deb_camp and hasattr(
                    self, 'duree') and self.duree:
            from datetime import datetime
            try:
                date_ajoutee = datetime.strptime(str(self.date_deb_camp),
                                                 '%Y-%m-%d').date()
                date_fin_ajoutee = date_ajoutee + timedelta(days=self.duree)

                campagnes_existantes = Campagne.query.filter_by(
                    id_pla=value).all()
                for camp in campagnes_existantes:
                    if camp.id_camp != getattr(self, 'id_camp', None):
                        if hasattr(camp, 'date_deb_camp'
                                   ) and camp.date_deb_camp and hasattr(
                                       camp, 'duree') and camp.duree:
                            date_deb_exist = datetime.strptime(
                                str(camp.date_deb_camp), '%Y-%m-%d').date()
                            date_fin_exist = date_deb_exist + timedelta(
                                days=camp.duree)

                            if (date_ajoutee <= date_fin_exist
                                    and date_fin_ajoutee >= date_deb_exist):
                                raise ValueError(
                                    'La plateforme est déjà affectée à une autre campagne pendant cette période.'
                                )
            except (ValueError, TypeError, AttributeError):
                pass

        if key == 'duree' and hasattr(self, 'id_pla') and self.id_pla:
            plateforme = Plateforme.query.get(self.id_pla)
            if plateforme and hasattr(plateforme,
                                      'duree_max') and plateforme.duree_max:
                if value > plateforme.duree_max:
                    raise ValueError(
                        'La durée de la campagne dépasse la durée maximale de la plateforme.'
                    )

            if plateforme and hasattr(
                    plateforme, 'jours_av_mainte'
            ) and plateforme.jours_av_mainte is not None:
                if plateforme.jours_av_mainte >= value:
                    plateforme.jours_av_mainte -= value
                else:
                    plateforme.jours_av_mainte = plateforme.inter_mainte - value if hasattr(
                        plateforme, 'inter_mainte') else 0

        if key == 'id_budg' and hasattr(self,
                                        'id_pla') and self.id_pla and hasattr(
                                            self, 'duree') and self.duree:
            plateforme = Plateforme.query.get(self.id_pla)
            budget = Budget.query.get(value)
            if plateforme and budget and hasattr(
                    plateforme, 'cout_exploi_jour') and hasattr(
                        budget, 'valeur'):
                cout_nouveau = plateforme.cout_exploi_jour * self.duree

                cout_total = 0
                campagnes_budget = Campagne.query.filter_by(
                    id_budg=value).all()
                for camp in campagnes_budget:
                    if camp.id_camp != getattr(self, 'id_camp', None):
                        pla_camp = Plateforme.query.get(camp.id_pla)
                        if pla_camp and hasattr(pla_camp, 'cout_exploi_jour'):
                            cout_total += pla_camp.cout_exploi_jour * camp.duree

                if cout_total + cout_nouveau > budget.valeur:
                    raise ValueError(
                        f'Insertion impossible, la campagne est hors budget. Budget couvert : {cout_total}/{budget.valeur}'
                    )

        return value


class Participer(db.Model):
    id_pers = db.Column(db.Integer,
                        db.ForeignKey('personnel.id_pers'),
                        primary_key=True)
    id_camp = db.Column(db.Integer,
                        db.ForeignKey('campagne.id_camp'),
                        primary_key=True)

    def __init__(self, id_pers, id_camp):
        self.id_pers = id_pers
        self.id_camp = id_camp

    def __repr__(self):
        return "<Participer (%s, %s)>" % (self.id_pers, self.id_camp)

    @validates('id_pers', 'id_camp')
    def validate_habilitations_et_conflits(self, key, value):
        if key == 'id_camp' and hasattr(self, 'id_pers') and self.id_pers:
            campagne = Campagne.query.get(value)
            if campagne and hasattr(campagne, 'id_pla'):
                plateforme = Plateforme.query.get(campagne.id_pla)
                if plateforme:
                    habilitations_requises = [
                        n.id_hab for n in Necessiter.query.filter_by(
                            id_pla=plateforme.id_pla).all()
                    ]
                    habilitations_personnel = [
                        s.id_hab for s in SpecialiserEn.query.filter_by(
                            id_pers=self.id_pers).all()
                    ]
                    for hab_req in habilitations_requises:
                        if hab_req not in habilitations_personnel:
                            raise ValueError(
                                'Le personnel ne possède pas une habilitation requise pour la plateforme.'
                            )

            if campagne and hasattr(
                    campagne,
                    'date_deb_camp') and campagne.date_deb_camp and hasattr(
                        campagne, 'duree'):
                from datetime import datetime
                try:
                    date_ajoutee = datetime.strptime(
                        str(campagne.date_deb_camp), '%Y-%m-%d').date()
                    date_fin_ajoutee = date_ajoutee + timedelta(
                        days=campagne.duree)

                    participations_existantes = Participer.query.filter_by(
                        id_pers=self.id_pers).all()
                    for part in participations_existantes:
                        camp_exist = Campagne.query.get(part.id_camp)
                        if camp_exist and hasattr(
                                camp_exist, 'date_deb_camp'
                        ) and camp_exist.date_deb_camp and hasattr(
                                camp_exist, 'duree'):
                            date_deb_exist = datetime.strptime(
                                str(camp_exist.date_deb_camp),
                                '%Y-%m-%d').date()
                            date_fin_exist = date_deb_exist + timedelta(
                                days=camp_exist.duree)

                            if (date_ajoutee <= date_fin_exist
                                    and date_fin_ajoutee >= date_deb_exist):
                                raise ValueError(
                                    'Le personnel est déjà affecté à une autre campagne pendant cette période.'
                                )
                except (ValueError, TypeError, AttributeError):
                    pass

            if campagne and hasattr(campagne, 'id_pla'):
                plateforme = Plateforme.query.get(campagne.id_pla)
                if plateforme and hasattr(
                        plateforme, 'nb_pers_max') and plateforme.nb_pers_max:
                    nb_participants_actuel = Participer.query.filter_by(
                        id_camp=value).count()
                    if nb_participants_actuel >= plateforme.nb_pers_max:
                        raise ValueError(
                            'Le nombre maximum de participants pour cette plateforme est atteint.'
                        )

        return value


class Sequence(db.Model):
    id_seq = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(40))

    def __init__(self, id_seq, nom_fichier):
        self.id_seq = id_seq
        self.nom_fichier = nom_fichier

    def __repr__(self):
        return "<Sequence (%s, %s)>" % (self.id_seq, self.nom_fichier)


class Extraire(db.Model):
    id_camp = db.Column(db.Integer,
                        db.ForeignKey('campagne.id_camp'),
                        primary_key=True)
    id_seq = db.Column(db.Integer,
                       db.ForeignKey('sequence.id_seq'),
                       primary_key=True)

    def __init__(self, id_camp, id_seq):
        self.id_camp = id_camp
        self.id_seq = id_seq

    def __repr__(self):
        return "<Extraire (%s, %s)>" % (self.id_camp, self.id_seq)


class Espece(db.Model):
    id_esp = db.Column(db.Integer, primary_key=True)
    id_seq = db.Column(db.Integer, db.ForeignKey('sequence.id_seq'))
    nom_esp = db.Column(db.String(40))

    def __init__(self, id_esp, id_seq, nom_esp):
        self.id_esp = id_esp
        self.id_seq = id_seq
        self.nom_esp = nom_esp

    def __repr__(self):
        return "<Espece (%s) %s>" % (self.id_esp, self.nom_esp)


class Echantillon(db.Model):
    id_ech = db.Column(db.Integer, primary_key=True)
    id_seq = db.Column(db.Integer, db.ForeignKey('sequence.id_seq'))
    commentaire = db.Column(db.String(255))

    def __init__(self, id_ech, id_seq, commentaire):
        self.id_ech = id_ech
        self.id_seq = id_seq
        self.commentaire = commentaire

    def __repr__(self):
        return "<Echantillon (%s)>" % (self.id_ech)
