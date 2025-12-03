"""Configuration pytest et fixtures communes."""
import pytest
from monApp.app import app, db
from monApp.models import (
    User, Personnel, Habilitation, Plateforme, Budget, 
    Campagne, Participer, Sequence, Extraire, Echantillon,
    SpecialiserEn, Necessiter, Materiel, Maintenance
)
from hashlib import sha256
from datetime import date, timedelta


@pytest.fixture
def client():
    """Client de test Flask."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # S'assurer que la base est vide
            db.create_all()
            _setup_test_data()
            yield client
            db.session.remove()
            db.drop_all()


def _setup_test_data():
    """Crée des données de test."""
    # Désactiver temporairement les validations
    from sqlalchemy import event
    from sqlalchemy.orm import Session
    
    # Habilitations
    hab1 = Habilitation(id_hab=1, nom_hab='Fouille')
    hab2 = Habilitation(id_hab=2, nom_hab='Analyse')
    db.session.add_all([hab1, hab2])
    
    # Personnel
    pers1 = Personnel(Id_pers=1, nom_pers='Dupont')
    pers2 = Personnel(Id_pers=2, nom_pers='Martin')
    db.session.add_all([pers1, pers2])
    
    # Spécialisations
    spec1 = SpecialiserEn(Id_pers=1, id_hab=1)
    spec2 = SpecialiserEn(Id_pers=1, id_hab=2)
    spec3 = SpecialiserEn(Id_pers=2, id_hab=1)
    db.session.add_all([spec1, spec2, spec3])
    
    # Plateforme
    plat1 = Plateforme(id_pla=1, nom_pla='Site A', nb_pers_nec=2, 
                       cout_exploi_jour=100.0, inter_mainte=30)
    db.session.add(plat1)
    
    # Nécessite
    nec1 = Necessiter(id_pla=1, id_hab=1)
    db.session.add(nec1)
    
    # Matériel
    mat1 = Materiel(id_mat=1, id_hab=1, nom_mat='Pelle')
    db.session.add(mat1)
    
    # Budget
    budget1 = Budget(id_budg=1, valeur=10000.0, date_deb_mois=date(2025, 12, 1))
    db.session.add(budget1)
    
    # Commit avant la campagne pour éviter l'autoflush
    db.session.commit()
    
    # Campagne
    camp1 = Campagne(id_camp=1, duree=5, date_deb_camp=date(2025, 12, 10),
                     id_pla=1, id_budg=1, nom_lieu_fouille='Site Test')
    db.session.add(camp1)
    db.session.commit()
    
    # Participation
    part1 = Participer(Id_pers=1, id_camp=1)
    db.session.add(part1)
    
    # Séquence et échantillon
    seq1 = Sequence(id_seq=1, nom_fichier='SEQ001.fasta')
    db.session.add(seq1)
    
    ext1 = Extraire(id_camp=1, id_seq=1)
    db.session.add(ext1)
    
    ech1 = Echantillon(id_ech=1, id_seq=1, commentaire='Test', 
                       sequence_adn='ATCGATCGATCG')
    ech2 = Echantillon(id_ech=2, id_seq=1, commentaire='Test 2',
                       sequence_adn='ATCGATCGATCG')
    db.session.add_all([ech1, ech2])
    
    # Maintenance
    maint1 = Maintenance(id_maint=1, id_pla=1, 
                        date_deb_maint=date.today() + timedelta(days=5),
                        date_fin_maint=date.today() + timedelta(days=7))
    db.session.add(maint1)
    
    # Utilisateurs
    m = sha256()
    m.update('password'.encode())
    pwd_hash = m.hexdigest()
    
    chercheur = User(Login='chercheur', Password=pwd_hash, Nom='Test', 
                     Prenom='Chercheur', Role='chercheur', Id_pers=1)
    directeur = User(Login='directeur', Password=pwd_hash, Nom='Test',
                     Prenom='Directeur', Role='directeur')
    admin = User(Login='admin', Password=pwd_hash, Nom='Test',
                 Prenom='Admin', Role='admin')
    technicien = User(Login='technicien', Password=pwd_hash, Nom='Test',
                      Prenom='Technicien', Role='technicien')
    
    db.session.add_all([chercheur, directeur, admin, technicien])
    db.session.commit()


@pytest.fixture
def auth_chercheur(client):
    """Authentifie un chercheur."""
    client.post('/login/', data={
        'Login': 'chercheur',
        'Password': 'password'
    }, follow_redirects=True)
    return client


@pytest.fixture
def auth_directeur(client):
    """Authentifie un directeur."""
    client.post('/login/', data={
        'Login': 'directeur',
        'Password': 'password'
    }, follow_redirects=True)
    return client


@pytest.fixture
def auth_admin(client):
    """Authentifie un admin."""
    client.post('/login/', data={
        'Login': 'admin',
        'Password': 'password'
    }, follow_redirects=True)
    return client


@pytest.fixture
def auth_technicien(client):
    """Authentifie un technicien."""
    client.post('/login/', data={
        'Login': 'technicien',
        'Password': 'password'
    }, follow_redirects=True)
    return client
