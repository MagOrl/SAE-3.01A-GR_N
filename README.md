# SAE-3.01A-GR_N
- ARSAMERZOEV Magomed
- DRAME Zakharia 
- BERTILI Erwann 
- DANZIN Titouan 
- groupe N de la classe info 2-3

- Lien GitHub : https://github.com/MagOrl/SAE-3.01A-GR_N.git
- Lien MCD v1 : https://www.tldraw.com/f/8d1Z-6LZPqw4lKANld8kj?d=v-101.0.1863.940.Q-cKYr0AFJYwYMZwRfBx2
- Lien google docs : https://docs.google.com/document/d/17NsF1P9UuVO49ut3BkotqYMttNVRFbQjYLHBYJkFbqc/edit?usp=sharing
- Video de présentation : https://www.youtube.com/watch?v=103dyLb9fvw

### Faire le pytest :
```
pytest --cov=exercice --cov-report=term-missing test.py #dans le répertoire ALGO
```

### Démarrer le projet sur Linux
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
flask --app monApp run
```

### Démarrer le projet sur Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirement.txt
flask --app monApp run
```

### Initialiser la base de données
```sh
flask --app monApp syncdb
```

### Peupler la base de données
```sh
flask --app monApp loaddb
```

### Crée un utilisateur:
- Admin : flask --app monApp newuser admin adminmdp NOMADMIN Prenomadmin admin None
- Technicien : flask --app monApp newuser tech techmdp NOMTECH Prenomtech technicien None
- Directeur : flask --app monApp newuser direct directmdp NOMDIRECT Prenomdirect directeur None
- Chercheur : flask --app monApp newuser cherch cherchmdp NOMCHERCH Prenomcherch chercheur 1 (1 représente l’ID du personnel)
