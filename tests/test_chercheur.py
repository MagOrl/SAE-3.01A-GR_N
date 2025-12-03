"""Tests pour les vues chercheur."""
import pytest
from datetime import date


def test_chercheur_accueil(auth_chercheur):
    """Test page d'accueil chercheur."""
    response = auth_chercheur.get('/chercheur/')
    assert response.status_code == 200


def test_chercheur_accueil_access_denied(auth_directeur):
    """Test accès refusé pour non-chercheur."""
    response = auth_directeur.get('/chercheur/')
    assert response.status_code == 200
    assert b'401' in response.data or b"droits" in response.data


def test_insert_campagne(auth_chercheur):
    """Test insertion d'une campagne."""
    response = auth_chercheur.post('/chercheur/campagne/insert', data={
        'plateform_affecte': '1',
        'dat_deb': '2025-12-20',
        'duree_camp': '3',
        'lieu_fouille': 'Nouveau Site',
        'pers': ['1']
    }, follow_redirects=True)
    assert response.status_code == 200


def test_chercheur_sequence(auth_chercheur):
    """Test page séquences."""
    response = auth_chercheur.get('/chercheur/sequence/')
    assert response.status_code == 200


def test_chercheur_detail_campagne(auth_chercheur):
    """Test détail d'une campagne."""
    response = auth_chercheur.get('/chercheur/campagne/1')
    assert response.status_code == 200


def test_chercheur_detail_campagne_access_denied(auth_chercheur):
    """Test accès refusé à une campagne non participée."""
    from monApp.models import Campagne, db
    from datetime import date
    other_campagne = Campagne(
        id_camp=100,
        duree=30,
        date_deb_camp=date(2024, 7, 1),
        nom_lieu_fouille="Site Interdit",
        id_pla=1,
        id_budg=1
    )
    db.session.add(other_campagne)
    db.session.commit()
    
    response = auth_chercheur.get('/chercheur/campagne/100')
    assert b"ne participez pas" in response.data or response.status_code == 403


def test_upload_sequence_adn_get(auth_chercheur):
    """Test affichage formulaire upload ADN."""
    response = auth_chercheur.get('/chercheur/campagne/1/upload_adn/1')
    assert response.status_code == 200


def test_upload_sequence_adn_post(auth_chercheur):
    """Test upload séquence ADN."""
    response = auth_chercheur.post('/chercheur/campagne/1/upload_adn/1', data={
        'id_ech': '1',
        'sequence_adn': 'ATCGATCGATCGATCG'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_ajouter_sequence_get(auth_chercheur):
    """Test affichage formulaire ajout séquence."""
    response = auth_chercheur.get('/chercheur/campagne/1/ajouter_sequence')
    assert response.status_code == 200


def test_ajouter_sequence_post(auth_chercheur):
    """Test ajout d'une séquence."""
    response = auth_chercheur.post('/chercheur/campagne/1/ajouter_sequence', data={
        'nom_fichier': 'SEQ002.fasta'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_supprimer_sequence(auth_chercheur):
    """Test suppression d'une séquence."""
    response = auth_chercheur.get('/chercheur/campagne/1/supprimer_sequence/1', 
                                  follow_redirects=True)
    assert response.status_code == 200


def test_analyser_adn_get(auth_chercheur):
    """Test affichage formulaire analyse ADN."""
    response = auth_chercheur.get('/chercheur/campagne/1/analyser_adn/1')
    assert response.status_code == 200


def test_analyser_adn_post(auth_chercheur):
    """Test analyse ADN."""
    response = auth_chercheur.post('/chercheur/campagne/1/analyser_adn/1', data={
        'type_analyse': 'mutation_remplacement',
        'taux_mutation': '10'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_comparer_sequences_get(auth_chercheur):
    """Test affichage formulaire comparaison."""
    response = auth_chercheur.get('/chercheur/campagne/1/comparer_sequences/1')
    assert response.status_code == 200


def test_comparer_sequences_post(auth_chercheur):
    """Test comparaison de séquences."""
    response = auth_chercheur.post('/chercheur/campagne/1/comparer_sequences/1', data={
        'id_ech2': '2',
        'type_distance': 'distance_levenshtein'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_chercheur_resultats(auth_chercheur):
    """Test page résultats."""
    response = auth_chercheur.get('/chercheur/resultats/')
    assert response.status_code == 200
