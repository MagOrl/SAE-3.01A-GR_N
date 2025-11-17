import click
import logging
from hashlib import sha256
from .models import Habilitation, Personnel, Plateforme, Materiel, Utiliser, Necessiter, SpecialiserEn, Budget, Campagne, Participer, Sequence, Extraire, Espece, Echantillon
from .app import app, db
from sqlalchemy import func
import datetime

lg = logging.getLogger(__name__)


@app.cli.command()
@click.argument('filename')
def loaddb(filename: str) -> None:
    """
    Crée les tables et les remplit avec des données depuis un fichier YAML.
    
    Args:
        filename (str): Chemin du fichier YAML contenant les données.
    """
    # recréer la base
    db.drop_all()
    db.create_all()

    import yaml

    with open(filename, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file) or []

    # Charger les habilitations
    for hab in data.get("habilitations", []):
        habilitation = Habilitation(id_hab=hab['id_hab'],
                                    nom_hab=hab['nom_hab'])
        db.session.add(habilitation)
        db.session.commit()

    # Charger le personnel
    for pers in data.get("personnels", []):
        personnel = Personnel(id_pers=pers['id_pers'],
                              nom_pers=pers['nom_pers'])
        db.session.add(personnel)
        db.session.commit()

    # Charger les plateformes
    for pla in data.get("plateformes", []):
        plateforme = Plateforme(id_pla=pla['id_pla'],
                                nom_pla=pla['nom_pla'],
                                nb_pers_nec=pla['nb_pers_nec'],
                                cout_exploi_jour=pla['cout_exploi_jour'],
                                inter_mainte=pla['inter_mainte'],
                                jours_av_mainte=pla['jours_av_mainte'])
        db.session.add(plateforme)
        db.session.commit()

    # Charger les matériels
    for mat in data.get("materiels", []):
        materiel = Materiel(id_mat=mat['id_mat'],
                            id_hab=mat['id_hab'],
                            nom_mat=mat['nom_mat'])
        db.session.add(materiel)
        db.session.commit()

    # Charger les utilisations
    for util in data.get("utilisers", []):
        utiliser = Utiliser(id_mat=util['id_mat'],
                            id_pla=util['id_pla'])
        db.session.add(utiliser)
        db.session.commit()

    # Charger les nécessités
    for nec in data.get("necessiters", []):
        necessiter = Necessiter(id_hab=nec['id_hab'],
                                id_pla=nec['id_pla'])
        db.session.add(necessiter)
        db.session.commit()

    # Charger les spécialisations
    for spec in data.get("specialiserens", []):
        specialiser = SpecialiserEn(id_hab=spec['id_hab'],
                                    id_pers=spec['id_pers'])
        db.session.add(specialiser)
        db.session.commit()

    # Charger les budgets
    for budg in data.get("budgets", []):
        date_deb_mois = datetime.date.fromisoformat(budg['date_deb_mois'])
        budget = Budget(id_budg=budg['id_budg'],
                        valeur=budg['valeur'],
                        date_deb_mois=date_deb_mois)
        db.session.add(budget)
        db.session.commit()

    # Charger les campagnes
    for camp in data.get("campagnes", []):
        date_deb_camp = datetime.date.fromisoformat(camp['date_deb_camp'])
        campagne = Campagne(id_camp=camp['id_camp'],
                            duree=camp['duree'],
                            date_deb_camp=date_deb_camp,
                            id_pla=camp['id_pla'],
                            id_budg=camp['id_budg'])
        db.session.add(campagne)
        db.session.commit()

    # Charger les participations
    for part in data.get("participers", []):
        participer = Participer(id_pers=part['id_pers'],
                                id_camp=part['id_camp'])
        db.session.add(participer)
        db.session.commit()

    # Charger les séquences
    for seq in data.get("sequences", []):
        sequence = Sequence(id_seq=seq['id_seq'],
                            nom_fichier=seq['nom_fichier'])
        db.session.add(sequence)
        db.session.commit()

    # Charger les extractions
    for ext in data.get("extractions", []):
        extraire = Extraire(id_camp=ext['id_camp'],
                            id_seq=ext['id_seq'])
        db.session.add(extraire)
        db.session.commit()

    # Charger les espèces
    for esp in data.get("especes", []):
        espece = Espece(id_esp=esp['id_esp'],
                        id_seq=esp['id_seq'],
                        nom_esp=esp['nom_esp'])
        db.session.add(espece)
        db.session.commit()

    # Charger les échantillons
    for ech in data.get("echantillons", []):
        echantillon = Echantillon(id_ech=ech['id_ech'],
                                  id_seq=ech['id_seq'],
                                  commentaire=ech['commentaire'])
        db.session.add(echantillon)
        db.session.commit()


@app.cli.command()
def syncdb() -> None:
    """
    Crée les tables de la base de données.
    """
    db.create_all()
    lg.warning('Base de donnée synchronisée!')