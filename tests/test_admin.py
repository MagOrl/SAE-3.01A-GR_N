"""Tests pour les vues admin."""
import pytest


def test_admin_accueil(auth_admin):
    """Test page d'accueil admin."""
    response = auth_admin.get('/admin/')
    assert response.status_code == 200


def test_admin_accueil_access_denied(auth_chercheur):
    """Test accès refusé pour non-admin."""
    response = auth_chercheur.get('/admin/')
    assert response.status_code == 200
    assert b'401' in response.data or b"droits" in response.data


def test_admin_gerer_personnel_get(auth_admin):
    """Test affichage gestion personnel."""
    response = auth_admin.get('/admin/gerer_personnel')
    assert response.status_code == 200


def test_admin_gerer_personnel_post(auth_admin):
    """Test création d'un personnel."""
    response = auth_admin.post('/admin/gerer_personnel', data={
        'nom_pers': 'Nouveau Personnel'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_gerer_personnel_detail_get(auth_admin):
    """Test détail d'un personnel."""
    response = auth_admin.get('/admin/gerer_personnel/1')
    assert response.status_code == 200


def test_gerer_personnel_detail_update_name(auth_admin):
    """Test modification nom personnel."""
    response = auth_admin.post('/admin/gerer_personnel/1', data={
        'action': 'update_name',
        'nom_pers': 'Nouveau Nom'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_gerer_personnel_detail_add_hab(auth_admin):
    """Test ajout habilitation."""
    response = auth_admin.post('/admin/gerer_personnel/2', data={
        'action': 'add_hab',
        'id_hab': '2'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_gerer_personnel_detail_remove_hab(auth_admin):
    """Test retrait habilitation."""
    response = auth_admin.post('/admin/gerer_personnel/1', data={
        'action': 'remove_hab',
        'id_hab': '1'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_supprimer_personnel(auth_admin):
    """Test suppression personnel."""
    response = auth_admin.post('/admin/gerer_personnel/2/supprimer', 
                               follow_redirects=True)
    assert response.status_code == 200


def test_admin_gerer_materiel_get(auth_admin):
    """Test affichage gestion matériel."""
    response = auth_admin.get('/admin/gerer_materiel')
    assert response.status_code == 200


def test_admin_gerer_materiel_post(auth_admin):
    """Test création d'un matériel."""
    response = auth_admin.post('/admin/gerer_materiel', data={
        'nom_mat': 'Nouveau Matériel',
        'id_hab': '1'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_gerer_materiel_detail_get(auth_admin):
    """Test détail d'un matériel."""
    response = auth_admin.get('/admin/gerer_materiel/1')
    assert response.status_code == 200


def test_gerer_materiel_detail_update_name(auth_admin):
    """Test modification nom matériel."""
    response = auth_admin.post('/admin/gerer_materiel/1', data={
        'action': 'update_name',
        'nom_mat': 'Matériel Modifié'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_gerer_materiel_detail_update_hab(auth_admin):
    """Test modification habilitation matériel."""
    response = auth_admin.post('/admin/gerer_materiel/1', data={
        'action': 'update_hab',
        'id_hab': '2'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_supprimer_materiel(auth_admin):
    """Test suppression matériel."""
    response = auth_admin.post('/admin/gerer_materiel/1/supprimer',
                               follow_redirects=True)
    assert response.status_code == 200
