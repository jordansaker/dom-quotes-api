"""
Model for the admin to access the database and perform full CRUD
range
"""
from marshmallow import fields
from marshmallow.validate import Length
from init import db, ma

class User(db.Model):
    """
    User model

    Contains the following attributes

        id (int), email (str), password (str), is_admin (bool)
    """
    __tablename__ = 'users'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)


class AdminSchema(ma.Schema):
    """
    Schema used to load the body request of an admin operation

    Attributes:

        email (str), password (str), quote (text), movie_title (str)
    """
    quote = fields.String(validate=Length(3), required=True)
    movie_title = fields.String(validate=Length(2), required=True)
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('quote', 'movie_title')


class AdminLoginSchema(ma.Schema):
    """
    Schema used to load the body request of an admin login

    Attributes:

        email (str), password (str)
    """
    email = fields.Email(required=True)
    password = fields.String(required=True)
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('email', 'password')
