# This file will contain the function used to load the correct configurations from config.py and instance/config.py
# 3rd-Party module imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local module imports
from config import app_config

# database variable initialisation
db = SQLAlchemy()
# db - this variable will be used to interact with the MySQL database

# This function will load the correct configuration from config.py
# depending on the configuration name passed as a parameter
# This function will also load the correct configurations from instance/config.py
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    # Migrations allow us to manage changes we make to models
    migrate = Migrate(app, db)
    # migrate - An object that allows us to run migrations using Flask-Migrate

    from app import models
    # Imported and registered the hpApp blueprint
    # change to hpApp as hpApp is the blueprint
    from .home.__init__ import hpApp as hpApp_blueprint
    app.register_blueprint(hpApp_blueprint)

    return app
