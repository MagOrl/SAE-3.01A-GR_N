import sqlalchemy  
from sqlalchemy import text
import os

CONNEXION = sqlalchemy.create_engine('mysql://'+"arsamerzoev"+':'+"arsamerzoev"+'@'+"servinfo-maria"+'/'+"DBarsamerzoev")
                             
def syncdb():
    files = ["CREATION.sql","TRIGGER.sql"]
    for file in files:    
        path = os.path.join("code/BD/", file)
        with CONNEXION.connect() as con:
            with open(path,'r') as fic:
                query = text(fic.read())
                con.execute(query)
    
syncdb()