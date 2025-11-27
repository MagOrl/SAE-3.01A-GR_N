import logging
import os
from hashlib import sha256
from .app import app, db
import sqlalchemy
from sqlalchemy import text
from .models import *


lg = logging.getLogger(__name__)    

@app.cli.command()
def syncdb() -> None:
    """
    Crée les tables de la base de données.
    """
    db.create_all()
    lg.warning('Base de donnée synchronisée!')


@app.cli.command()
def loaddb() -> None:
    """
    Charge les données de peuplement.
    """
    import os
    
    # Chemin vers le fichier PEUPLEMENT.sql
    # On suppose que le fichier est dans code/BD/PEUPLEMENT.sql par rapport à la racine du projet
    file_path = os.path.join(os.getcwd(), 'code', 'BD', 'PEUPLEMENT.sql')
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            sql_commands = f.read().split(';')
        
        for command in sql_commands:
            if command.strip():
                db.session.execute(text(command))
        db.session.commit()
        lg.warning('Données chargées depuis PEUPLEMENT.sql !')
    else:
        lg.error(f'Fichier non trouvé : {file_path}')