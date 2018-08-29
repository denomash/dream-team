# app/__init__.py

# third party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

# initialize db variable
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py')

    # prepare the application to work with SQLAlchemy
    Bootstrap(app)
    db.init_app(app)

    # prepare the application to work with LoginManager
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_views = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # tempolary route
    @app.route('/')
    def hello():
        return "What's cracking champ. You did it!!!"

    return app
