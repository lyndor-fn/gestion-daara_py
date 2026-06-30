# Documentation du projet - Gestion d'une Daara

## 1. Presentation generale

Ce projet est une application web developpee avec Flask. Elle permet de gerer une daara, c'est-a-dire une ecole coranique.

L'application gere quatre entites principales :

- les maitres, appeles aussi serignes ;
- les classes, appelees halqas ;
- les talibes ;
- les progressions des talibes dans la memorisation du Coran.

Le but est de permettre a l'administration de la daara d'ajouter, modifier, supprimer, rechercher et exporter les donnees au format CSV.

## 2. Technologies utilisees

Le projet utilise :

- Python pour le langage de programmation ;
- Flask pour le framework web ;
- Flask-SQLAlchemy pour manipuler la base de donnees avec un ORM ;
- Flask-Migrate pour gerer les migrations de la base avec Alembic ;
- Flask-WTF et WTForms pour les formulaires et la validation ;
- Jinja2 pour les pages HTML dynamiques ;
- PostgreSQL comme systeme de base de donnees.

Aucun SQL brut n'est utilise dans le CRUD. Les vues utilisent `Model.query` et `db.session`.

## 3. Architecture MVC

Le projet respecte une architecture MVC.

### Modeles

Les modeles sont dans le dossier `app/models/`.

Ils representent les tables de la base de donnees :

- `Maitre` correspond a la table `maitres` ;
- `Classe` correspond a la table `classes` ;
- `Talibe` correspond a la table `talibes` ;
- `Progression` correspond a la table `progressions`.

Le fichier `base.py` contient `BaseModel`. Cette classe est abstraite et ajoute deux colonnes communes a toutes les entites :

- `cree_le` : date de creation ;
- `maj_le` : date de derniere modification.

### Vues / Controleurs

Les controleurs sont dans le dossier `app/views/`.

Chaque fichier est un Blueprint Flask :

- `maitre.py` gere les routes des maitres ;
- `classe.py` gere les routes des classes ;
- `talibe.py` gere les routes des talibes ;
- `progression.py` gere les routes des progressions ;
- `main.py` gere la route d'accueil.

Les vues recoivent les requetes HTTP, interrogent la base, valident les formulaires, gerent les exceptions, puis retournent un template ou une redirection.

### Templates

Les templates sont dans `app/templates/`.

Chaque entite a deux pages :

- `liste.html` pour afficher les donnees dans un tableau ;
- `formulaire.html` pour ajouter ou modifier une donnee.

Tous les templates heritent de `base.html`, qui contient la navigation, les messages `flash()` et le style general.

### Formulaires

Les formulaires sont dans `app/forms/`.

Ils definissent les champs visibles dans les pages HTML et les regles de validation cote serveur.

Exemple : dans `TalibeForm`, le matricule, le prenom, le nom et la classe sont obligatoires.

Les champs de type liste deroulante, comme la classe d'un talibe ou le maitre d'une classe, sont alimentes depuis la base de donnees dans les vues.

## 4. Relations entre les entites

Les relations suivent cette chaine :

```text
Maitre 1 -> N Classe 1 -> N Talibe 1 -> N Progression
```

Cela signifie :

- un maitre peut encadrer plusieurs classes ;
- une classe appartient a un seul maitre ;
- une classe peut contenir plusieurs talibes ;
- un talibe appartient a une seule classe ;
- un talibe peut avoir plusieurs progressions ;
- une progression appartient a un seul talibe.

La suppression d'un talibe supprime automatiquement ses progressions grace au cascade SQLAlchemy.

## 5. Regles metier importantes

### Maitre

Le matricule du maitre est unique et sert de cle primaire.

Un maitre ne peut pas etre supprime s'il encadre au moins une classe.

### Classe

Le code de la classe est unique et sert de cle primaire.

Une classe doit obligatoirement etre rattachee a un maitre.

Une classe ne peut pas etre supprimee si elle contient au moins un talibe.

### Talibe

Le matricule du talibe est unique et sert de cle primaire.

Un talibe doit obligatoirement etre rattache a une classe.

Quand on supprime un talibe, ses progressions sont aussi supprimees.

### Progression

Une progression doit obligatoirement etre rattachee a un talibe.

La sourate ne doit pas etre vide.

Le nombre de versets doit etre positif ou egal a zero.

## 6. Gestion des exceptions

Les exceptions metier sont definies dans `app/exceptions/__init__.py`.

Toutes les exceptions heritent de `DaaraException`, qui herite de `RuntimeError`.

Exemples :

- `MaitreIntrouvableException` est levee quand un maitre recherche n'existe pas ;
- `ClasseDejaExistanteException` est levee quand on ajoute une classe avec un code deja utilise ;
- `SuppressionImpossibleException` est levee quand une suppression viole une relation ;
- `ProgressionInvalideException` est levee quand une progression contient des donnees invalides.

Les exceptions sont levees et capturees dans les vues. Les templates ne capturent jamais d'exception.

Quand une exception est capturee, son message est affiche a l'utilisateur avec `flash()`.

## 7. Fonctionnement d'un CRUD

Chaque entite possede les fonctionnalites suivantes :

- lister les donnees ;
- rechercher ou filtrer les donnees ;
- ajouter une nouvelle donnee ;
- modifier une donnee existante ;
- supprimer une donnee ;
- exporter la liste affichee en CSV.

Exemple pour les talibes :

1. L'utilisateur ouvre `/talibes/`.
2. La vue `lister()` recupere les filtres `q` et `classe`.
3. La requete SQLAlchemy filtre les talibes selon le nom, le prenom ou la classe.
4. Le template `talibes/liste.html` affiche le tableau.
5. Si l'utilisateur clique sur Exporter, la route `/talibes/exporter` genere un fichier CSV avec les memes filtres.

## 8. Export CSV

L'export CSV est gere par `app/utils/csv_exporter.py`.

La fonction `exporter_csv()` recoit :

- le nom du fichier ;
- la ligne d'en-tete ;
- les lignes de donnees.

Elle retourne une reponse HTTP avec l'en-tete `Content-Disposition: attachment`, ce qui force le navigateur a telecharger le fichier.

Chaque page de liste possede un bouton Exporter.

## 9. Configuration de la base de donnees

La configuration se trouve dans `config.py`.

En developpement, l'application utilise par defaut :

```text
postgresql+psycopg2://postgres:motdepasse@localhost:5432/daara_py
```

La base de donnees PostgreSQL doit donc s'appeler `daara_py`.

Il est possible de remplacer cette URL avec la variable d'environnement `DEV_DATABASE_URL`.

## 10. Commandes de lancement

Depuis le dossier `daara`, executer :

```powershell
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

Avant les migrations, il faut creer la base PostgreSQL `daara_py`.

Exemple avec psql :

```sql
CREATE DATABASE daara_py;
```

## 11. Ce qu'il faut expliquer a l'oral

Pour presenter le projet, il faut insister sur les points suivants :

- l'application respecte MVC : modeles, vues, formulaires et templates sont separes ;
- les relations entre les tables representent la realite d'une daara ;
- SQLAlchemy evite d'ecrire du SQL brut ;
- WTForms valide les formulaires cote serveur ;
- les exceptions metier rendent les erreurs plus propres et plus faciles a comprendre ;
- les suppressions dangereuses sont bloquees pour proteger les donnees ;
- l'export CSV permet de recuperer les listes depuis le navigateur.

## 12. Exemple de parcours utilisateur

Un utilisateur peut commencer par ajouter un maitre.

Ensuite, il cree une classe et choisit ce maitre dans une liste deroulante.

Puis, il ajoute un talibe et le rattache a cette classe.

Enfin, il ajoute une progression pour ce talibe en indiquant la sourate, le nombre de versets, la date d'evaluation et les observations.

Ce parcours montre l'enchainement logique des relations entre les entites.
