"""
Main App

Contains the create_app( ) function
"""
from os import environ
from flask import Flask
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.quote_bp import quote_bp
import config

def create_app():
    """
    Function to create the Flask app
    """
    app = Flask(__name__)
    # configure the app using the object from config.py
    if config.Config.ENVIRONMENT == 'prod':
        app.config.from_object('config.ProdConfig')
    else:
        app.config.from_object('config.DevConfig')
        environ['FLASK_DEBUG'] = config.DevConfig.FLASK_DEBUG
    app.json.sort_keys = False
    # initalise the instances from the init.py file
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    # register blueprints
    app.register_blueprint(cli_bp)
    app.register_blueprint(quote_bp)

    return app
