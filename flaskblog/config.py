
class Config:
    # empty values is overridden from sensitive_config.cfg file that holds sentitive applicaton config data 
    # such as username and passwords and will be exluded from version control.
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = ('Flask Blog', 'flaskblog-noreply@demo.com')
    MESSENTE_API_USERNAME = ""
    MESSENTE_API_PASSWORD = ""


class TestConfig(Config):
    SECRET_KEY = "testing"
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

