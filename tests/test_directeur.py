"""Tests pour les vues directeur."""
import pytest


def test_directeur_accueil(auth_directeur):
    """Test page d'accueil directeur."""
    response = auth_directeur.get('/directeur/')
    assert response.status_code == 200


def test_directeur_accueil_access_denied(auth_chercheur):
    """Test accès refusé pour non-directeur."""
    response = auth_chercheur.get('/directeur/')
    assert response.status_code == 200
    assert b'401' in response.data or b"droits" in response.data


def test_directeur_budget_get(auth_directeur):
    """Test affichage page budget."""
    response = auth_directeur.get('/directeur/budget/')
    assert response.status_code == 200


def test_insert_budget(auth_directeur):
    """Test création d'un budget."""
    response = auth_directeur.post('/directeur/budget/cree_budget', data={
        'valeur': '15000',
        'dat_deb': '2026-01-01'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_insert_budget_invalid(auth_directeur):
    """Test création budget avec données invalides."""
    response = auth_directeur.post('/directeur/budget/cree_budget', data={
        'valeur': '',
        'dat_deb': '2026-01-01'
    })
    assert response.status_code == 200
