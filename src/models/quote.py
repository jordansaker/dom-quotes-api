"""
Quotes Model and schema

The Quote Model contains the following attributes:

    id, quote, movie_title
"""
from init import db, ma

class Quote(db.Model):
    """
    Creates a model instance of the database instance

    Attributes:

        quote (text),  movie_title (str)
    """
    __tablename__ = 'dom_quotes'
    # model attributes
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, unique=True, nullable=False)
    movie_title = db.Column(db.String(), nullable=False)


class QuoteSchema(ma.Schema):
    """
    Defines the schema for the Quote Model

    class Meta:
        fields = ('id', 'quote', 'movie_title')
    """
    class Meta:
        """
        Defining the fields in a Tuple
        """
        fields = ('id', 'quote', 'movie_title')
        ordered = True

class QuoteSearchSchema(ma.Schema):
    """
    Defines the schema for the Quote Search loading

    class Meta:
        fields = ('user', 'search')
    """
    class Meta:
        """
        Defining the fields in a Tuple
        """
        fields = ('', 'search')
