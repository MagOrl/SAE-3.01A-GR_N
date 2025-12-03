"""Tests pour les vues technicien."""
import pytest
from datetime import date, timedelta


def test_technicien_accueil(auth_technicien):
    """Test page d'accueil technicien."""
    response = auth_technicien.get('/technicien/')
    assert response.status_code == 200


def test_technicien_accueil_access_denied(auth_chercheur):
    """Test accès refusé pour non-technicien."""
    response = auth_chercheur.get('/technicien/')
    assert response.status_code == 200
    assert b'401' in response.data or b"droits" in response.data


def test_gestion_maintenance(auth_technicien):
    """Test page gestion maintenance."""
    response = auth_technicien.get('/technicien/gestion_maintenance/')
    assert response.status_code == 200


def test_ajouter_maintenance_get(auth_technicien):
    """Test affichage formulaire ajout maintenance."""
    response = auth_technicien.get('/technicien/ajouter/')
    assert response.status_code == 200


def test_ajouter_maintenance_post(auth_technicien):
    """Test ajout d'une maintenance."""
    date_deb = (date.today() + timedelta(days=35)).strftime('%Y-%m-%d')
    date_fin = (date.today() + timedelta(days=37)).strftime('%Y-%m-%d')
    
    response = auth_technicien.post('/technicien/ajouter/', data={
        'id_pla': '1',
        'date_deb_maint': date_deb,
        'date_fin_maint': date_fin
    }, follow_redirects=True)
    assert response.status_code == 200


def test_supprimer_maintenance(auth_technicien):
    """Test suppression d'une maintenance."""
    response = auth_technicien.get('/technicien/supprimer/1',
                                   follow_redirects=True)
    assert response.status_code == 200
