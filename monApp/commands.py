import click
import logging
from .app import app, db
from sqlalchemy import text

lg = logging.getLogger(__name__)    

@app.cli.command()
def syncdb() -> None:
    """
    Crée les tables de la base de données.
    """
    db.create_all()
    lg.warning('Base de donnée synchronisée!')
    
@app.cli.command()
@click.argument('login')
@click.argument('pwd')
@click.argument('nom')
@click.argument('prenom')
@click.argument('role')
def newuser(login, pwd,nom,prenom,role):
    '''Adds a new user'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(pwd.encode())
    unUser = User(Login=login, Password=m.hexdigest(),Nom=nom,Prenom=prenom,Role=role)
    db.session.add(unUser)
    db.session.commit()
    lg.warning('User ' + login + ' created!')