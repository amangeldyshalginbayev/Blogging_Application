import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config, TestConfig



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()


def create_app(mode="prod"):
    config_class = Config
    if mode == "test":
        config_class = TestConfig
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.from_pyfile('sensitive_config.cfg')
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from flaskblog.main.routes import main
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.comments.routes import comments
    from flaskblog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(errors)

    return app



