"""Tests pour l'authentification."""
import pytest


def test_login_page(client):
    """Test affichage de la page de login."""
    response = client.get('/login/')
    assert response.status_code == 200
    assert b'Identifiant' in response.data


def test_login_success(client):
    """Test connexion réussie."""
    response = client.post('/login/', data={
        'Login': 'chercheur',
        'Password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login_invalid_credentials(client):
    """Test connexion avec mauvais identifiants."""
    response = client.post('/login/', data={
        'Login': 'chercheur',
        'Password': 'wrongpassword'
    })
    assert response.status_code == 200


def test_logout(auth_chercheur):
    """Test déconnexion."""
    response = auth_chercheur.get('/logout/', follow_redirects=True)
    assert response.status_code == 200


def test_index_redirect(client):
    """Test redirection de l'index."""
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
