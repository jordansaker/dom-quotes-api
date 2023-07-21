"""
Main App

Contains the create_app( ) function
"""
from flask import Flask
from init import db, ma
from config import app_config

def create_app():
    """
    Function to create the Flask app
    """
    app = Flask(__name__)

    app.config.from_object(app_config)
    db.init_app(app)
    ma.init_app(app)


    return app
