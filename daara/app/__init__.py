import os
from pathlib import Path

from flask import Flask

from config import config
from .extension import csrf, db, migrate


def create_app(config_name=None):
    app = Flask(__name__)
    selected_config = config_name or os.getenv("FLASK_CONFIG", "default")
    app.config.from_object(config[selected_config])

    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if database_uri.startswith("sqlite"):
        database_path = Path(database_uri.split("///", 1)[1])
        database_path.parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .models import Classe, Maitre, Progression, Talibe  # noqa: F401

    with app.app_context():
        db.create_all()

    from .models import Classe, Maitre, Progression, Talibe
    from .views.classe import bp_classes
    from .views.main import bp_main
    from .views.maitre import bp_maitres
    from .views.progression import bp_progressions
    from .views.talibe import bp_talibes

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_maitres)
    app.register_blueprint(bp_classes)
    app.register_blueprint(bp_talibes)
    app.register_blueprint(bp_progressions)

    return app
