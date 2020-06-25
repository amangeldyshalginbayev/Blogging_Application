import os


class Config:
    """This class used for configuration of flask application for development
    and production environments. For development, config values are loaded from
    'development_config.cfg' file. This file is ignored by version control.
    When deploying application to production, config values are loaded from
    environment variables. 'development_config.cfg' file is not pushed to
    production and used only for local development.
    """


SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
MESSENTE_API_USERNAME = os.environ.get("MESSENTE_API_USERNAME")
MESSENTE_API_PASSWORD = os.environ.get("MESSENTE_API_PASSWORD")


class TestConfig(Config):
    SECRET_KEY = "testing"
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
