"""
Model for the admin to access the database and perform full CRUD
range
"""
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

class UserSchema(ma.Schema):
    """
    Creates a model instance of the database instance

    Attributes:

        email (str)
    """
    class Meta:
        """
        Defining the fields in a tuple and ordering the fields
        """
        fields = ('email')