import os



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = ('Flask Blog', 'flaskblog-noreply@demo.com')
    MESSENTE_API_USERNAME = os.environ.get('MESSENTE_API_USERNAME')
    MESSENTE_API_PASSWORD = os.environ.get('MESSENTE_API_PASSWORD')