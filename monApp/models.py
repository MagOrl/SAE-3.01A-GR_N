from .app import db

class Habilitation(db.Model):
    id_hab = db.Column( db.String(10), primary_key=True )
    nom_hab = db.Column( db.String(20) )
    
    def __init__(self, nom_hab):
        self.nom_hab = nom_hab

    def __repr__(self):
        return "<Habilitation (%d) %s>" % (self.id_hab, self.nom_hab)

class Plateforme(db.Model):
    id_pla = db.column( db.String(10), primary_key=True )
    mon_pla = db.Column( db.String(20) )
    nb_pers_nec = db.Column( db.Integer )
    cout_exploit_j = db.Column( db.Float )
    inter_mainte = db.Column( db.Integer )

    def __init__(self, mon_pla, nb_pers_nec, cout_exploit_j, inter_mainte):
        self.mon_pla = mon_pla
        self.nb_pers_nec = nb_pers_nec
        self.cout_exploit_j = cout_exploit_j
        self.inter_mainte = inter_mainte

    def __repr__(self):
        return "<Personnel (%d) %s>" % (self.id_pla, self.mon_pla, self.nb_pers_nec, self.cout_exploit_j, self.inter_mainte )

class Necessiter(db.Model):
    id_hab = db.Column( db.String(10), primary_key=True )
    id_pla = db.Column( db.String(20), primary_key=True )
    habilitation_id = db.Column(db.Integer, db.ForeignKey("auteur.idA"))
    plateforme_id = db.Column(db.Integer, db.ForeignKey("auteur.idA"))
    
    def __init__(self, nom_hab):
        self.nom_hab = nom_hab

    def __repr__(self):
        return "<Habilitation (%d) %s>" % (self.id_hab, self.nom_hab)
