"""
App config file containing the config object
"""
from os import environ
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    """
    Config file object class
    """
    JWT_SECRET_KEY =  environ.get("JWT_KEY")
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

class DevConfig(Config):
    """
    Config file object class for Dev
    """
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URI_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_DEBUG = '1'

class ProdConfig(Config):
    """
    Config file object class for Prod
    """
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = '0'
