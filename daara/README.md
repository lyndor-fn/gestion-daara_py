# Gestion d'une Daara

Application Flask MVC pour gérer les maîtres, classes, talibés et progressions d'une école coranique.

## Lancement

```powershell
cd daara
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "run.py"
$env:FLASK_CONFIG = "development"
flask db init
flask db migrate -m "init"
flask db upgrade
flask run
```

Par défaut, la configuration utilise PostgreSQL :

```text
postgresql+psycopg2://postgres:motdepasse@localhost:5432/daara_py
```

L'URL peut être changée avec la variable d'environnement `DEV_DATABASE_URL`.
