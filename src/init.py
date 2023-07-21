"""
Initalise the Flask app

    Instance of SQLAlchemy assigned to db

    Instance of Marshmallow assigned to db
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
