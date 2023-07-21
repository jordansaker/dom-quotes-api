"""
Initalise the Flask app

    Instance of SQLAlchemy assigned to db

    Instance of Marshmallow assigned to ma

    Instance of Bcrypt assigned to bcrypt

    Instance of JWTManager assigned to jwt
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
