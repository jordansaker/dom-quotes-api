"""
Main App

Contains the create_app( ) function
"""
from os import environ
from flask import Flask
from flask_cors import CORS
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.quote_bp import quote_bp
import config

def create_app():
    """
    Function to create the Flask app
    """
    app = Flask(__name__)
    # allow CORS
    CORS(app)
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

    # handle errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'validation_error': err.messages}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'bad_request': 'No JSON object found in request body'}, 400

    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        return {'integrity_error': 'Data already exists in database'}, 400

    @app.errorhandler(UnsupportedMediaType)
    def unsupported_request(err):
        return {'bad_request': 'No JSON object found in request body'}, 400

    return app
