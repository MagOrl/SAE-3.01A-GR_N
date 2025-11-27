from .app import db
from datetime import timedelta
from sqlalchemy import func

class Habilitation(db.Model):
    id_hab = db.Column(db.String(10), primary_key=True)
    nom_hab = db.Column(db.String(20))
    
    def __init__(self, id_hab, nom_hab):
        self.id_hab = id_hab
        self.nom_hab = nom_hab
    
    def __repr__(self):
        return "<Habilitation (%s) %s>" % (self.id_hab, self.nom_hab)


class Personnel(db.Model):
    id_pers = db.Column(db.String(10), primary_key=True)
    nom_pers = db.Column(db.String(20))
    
    def __init__(self, id_pers, nom_pers):
        self.id_pers = id_pers
        self.nom_pers = nom_pers
    
    def __repr__(self):
        return "<Personnel (%s) %s>" % (self.id_pers, self.nom_pers)


class Plateforme(db.Model):
    id_pla = db.Column(db.String(10), primary_key=True)
    nom_pla = db.Column(db.String(20))
    nb_pers_nec = db.Column(db.Integer)
    cout_exploi_jour = db.Column(db.Float)
    inter_mainte = db.Column(db.Integer)
    
    def __init__(self, id_pla, nom_pla, nb_pers_nec, cout_exploi_jour, inter_mainte):
        self.id_pla = id_pla
        self.nom_pla = nom_pla
        self.nb_pers_nec = nb_pers_nec
        self.cout_exploi_jour = cout_exploi_jour
        self.inter_mainte = inter_mainte
    
    def __repr__(self):
        return "<Plateforme (%s) %s>" % (self.id_pla, self.nom_pla)

class Maintenance(db.Model):
    id_maint = db.Column(db.String(10), primary_key=True)
    id_pla = db.Column(db.String(10), db.ForeignKey('plateforme.id_pla'))
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
    id_op_maint = db.Column(db.String(10), primary_key=True)
    id_pla = db.Column(db.String(10), db.ForeignKey('plateforme.id_pla'))
    date_maintenance = db.Column(db.Date)
    
    def __init__(self, id_op_maint, id_pla, date_maintenance):
        self.id_op_maint = id_op_maint
        self.id_pla = id_pla
        self.date_maintenance = date_maintenance
    
    def __repr__(self):
        return "<OperationMaintenance (%s) %s>" % (self.id_op_maint, self.id_pla)

class Materiel(db.Model):
    id_mat = db.Column(db.String(10), primary_key=True)
    id_hab = db.Column(db.String(10), db.ForeignKey('Habilitation.id_hab'))
    nom_mat = db.Column(db.String(20))
    
    def __init__(self, id_mat, id_hab, nom_mat):
        self.id_mat = id_mat
        self.id_hab = id_hab
        self.nom_mat = nom_mat
    
    def __repr__(self):
        return "<Materiel (%s, %s, %s)>" % (self.id_mat, self.id_hab, self.nom_mat)

class Utiliser(db.Model):
    id_mat = db.Column(db.String(10), db.ForeignKey('Materiel.id_mat'), primary_key=True)
    id_pla = db.Column(db.String(10), db.ForeignKey('Plateforme.id_pla'), primary_key=True)
    
    def __init__(self, id_mat, id_pla):
        self.id_mat = id_mat
        self.id_pla = id_pla
    
    def __repr__(self):
        return "<Utiliser (%s, %s)>" % (self.id_mat, self.id_pla)

class Necessiter(db.Model):
    id_hab = db.Column(db.String(10), db.ForeignKey('Habilitation.id_hab'), primary_key=True)
    id_pla = db.Column(db.String(10), db.ForeignKey('Plateforme.id_pla'), primary_key=True)
    
    def __init__(self, id_hab, id_pla):
        self.id_hab = id_hab
        self.id_pla = id_pla
    
    def __repr__(self):
        return "<Necessiter (%s, %s)>" % (self.id_hab, self.id_pla)


class SpecialiserEn(db.Model):
    id_hab = db.Column(db.String(10), db.ForeignKey('Habilitation.id_hab'), primary_key=True)
    id_pers = db.Column(db.String(10), db.ForeignKey('Personnel.id_pers'), primary_key=True)
    
    def __init__(self, id_hab, id_pers):
        self.id_hab = id_hab
        self.id_pers = id_pers
    
    def __repr__(self):
        return "<SpecialiserEn (%s, %s)>" % (self.id_hab, self.id_pers)

class Budget(db.Model):
    id_budg = db.Column(db.String(10), primary_key=True)
    valeur = db.Column(db.Float)
    date_deb_mois = db.Column(db.Date)
    
    def __init__(self, id_budg, valeur, date_deb_mois):
        self.id_budg = id_budg
        self.valeur = valeur
        self.date_deb_mois = date_deb_mois
    
    def __repr__(self):
        return "<Budget (%s, %s, %s)>" % (self.id_budg, self.valeur, self.date_deb_mois)

class Campagne(db.Model):
    id_camp = db.Column(db.String(10), primary_key=True)
    duree = db.Column(db.Integer)
    date_deb_camp = db.Column(db.Date)
    id_pla = db.Column(db.String(10), db.ForeignKey('Plateforme.id_pla'))
    id_budg = db.Column(db.String(10),db.ForeignKey('Budget.id_budg'))
    
    def __init__(self, id_camp, duree, date_deb_camp, id_pla, id_budg):
        self.id_camp = id_camp
        self.duree = duree
        self.date_deb_camp = date_deb_camp
        self.id_pla = id_pla
        self.id_budg = id_budg
    
    def __repr__(self):
        return "<Campagne (%s)>" % (self.id_camp)


class Participer(db.Model):
    id_pers = db.Column(db.String(10), db.ForeignKey('Personnel.id_pers'), primary_key=True)
    id_camp = db.Column(db.String(10), db.ForeignKey('Campagne.id_camp'), primary_key=True)
    
    def __init__(self, id_pers, id_camp):
        self.id_pers = id_pers
        self.id_camp = id_camp
    
    def __repr__(self):
        return "<Participer (%s, %s)>" % (self.id_pers, self.id_camp)


class Sequence(db.Model):
    id_seq = db.Column(db.String(10), primary_key=True)
    nom_fichier = db.Column(db.String(40))
    
    def __init__(self, id_seq, nom_fichier):
        self.id_seq = id_seq
        self.nom_fichier = nom_fichier
    
    def __repr__(self):
        return "<Sequence (%s, %s)>" % (self.id_seq, self.nom_fichier)


class Extraire(db.Model):
    id_camp = db.Column(db.String(10), db.ForeignKey('Campagne.id_camp'), primary_key=True)
    id_seq = db.Column(db.String(10), db.ForeignKey('Sequence.id_seq'), primary_key=True)

    def __init__(self, id_camp, id_seq):
        self.id_camp = id_camp
        self.id_seq = id_seq
    
    def __repr__(self):
        return "<Extraire (%s, %s)>" % (self.id_camp, self.id_seq)


class Espece(db.Model):
    id_esp = db.Column(db.String(10), primary_key=True)
    id_seq = db.Column(db.String(10), db.ForeignKey('Sequence.id_seq'))
    nom_esp = db.Column(db.String(40))
    
    def __init__(self, id_esp, id_seq, nom_esp):
        self.id_esp = id_esp
        self.id_seq = id_seq
        self.nom_esp = nom_esp
    
    def __repr__(self):
        return "<Espece (%s) %s>" % (self.id_esp, self.nom_esp)


class Echantillon(db.Model):
    id_ech = db.Column(db.String(10), primary_key=True)
    id_seq = db.Column(db.String(10), db.ForeignKey('Sequence.id_seq'))
    commentaire = db.Column(db.String(255))
    
    def __init__(self, id_ech, id_seq, commentaire):
        self.id_ech = id_ech
        self.id_seq = id_seq
        self.commentaire = commentaire
    
    def __repr__(self):
        return "<Echantillon (%s)>" % (self.id_ech)

