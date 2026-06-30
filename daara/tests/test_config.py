from config import DevelopmentConfig


def test_development_config_defaults_to_sqlite():
    assert DevelopmentConfig.SQLALCHEMY_DATABASE_URI.startswith("sqlite")
