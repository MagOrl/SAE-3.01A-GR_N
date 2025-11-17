import logging
import os
from hashlib import sha256
from .app import app, db
import sqlalchemy
from sqlalchemy import text

lg = logging.getLogger(__name__)
CONNEXION = None
try:
    CONNEXION = sqlalchemy.create_engine('mysql://'+"arsamerzoev"+':'+"arsamerzoev"+'@'+"servinfo-maria"+'/'+"DBarsamerzoev")
except Exception as err:
    print(err)
    
    

@app.cli.command()
def syncdb() -> None:
    """
    Crée les tables de la base de données.
    """
    files = ["CREATION.sql","TRIGGER.sql"]
    for file in files:    
        path = os.path.join("code/BD/", file)
        with CONNEXION.connect() as con:
            with open(path,'r') as fic:
                query = text(fic.read())
                con.execute(query)
    lg.warning('Base de donnée synchronisée!')