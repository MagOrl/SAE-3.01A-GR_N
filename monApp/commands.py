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