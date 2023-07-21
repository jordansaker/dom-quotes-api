"""
App config file containing the config object
"""
from os import environ

class Config(object):
    """
    Config file object class

    Contains the sqlalchemy_database_uri(self) method
    """
    JWT_SECRET_KEY =  environ.get("JWT_KEY")
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """
        Method to access the .env and get the value of DB_URI
        """
        value = environ.get("DB_URI")
        if not value:
            raise ValueError("DB_URI is not set in .env")
        return value


class DevelopmentConfig(Config):
    """
    Development Config sets DEBUG to True
    """
    FLASK_DEBUG = "1"

class ProductionConfig(Config):
    """
    Pro Config sets DEBUG to False
    """
    FLASK_DEBUG = "0"

# check the env for the envrionment setting
environment = environ.get("FLASK_ENV")

match(environment):
    case 'development':
        app_config = DevelopmentConfig()
    case 'production':
        app_config = ProductionConfig()
# set the debug mode if applicable
environ['FLASK_DEBUG'] = app_config.FLASK_DEBUG
