"""
Perform the CRUD operations on the Quote model
"""
from flask import Blueprint
from random import randint
from sqlalchemy import desc
from models.quote import Quote, QuoteSchema
from init import db

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/')
def get_quote():
    """
    Get a random quote from the dom_quotes table
    """
    # get the range for randint
    # query the database table, order by descending, get the first record
    # get the record id and set as the max range for randint
    stmt = db.select(Quote).order_by(desc(Quote.id))
    quotes = db.session.scalars(stmt).all()

    # grab the first object in the list and access the id key
    max_range = quotes[0].id
    # get a random number to use as the query condition
    random_quote_id = randint(1, max_range)
    # retrieve the quote from the database
    stmt = db.select(Quote).filter_by(id=random_quote_id)
    random_quote = db.session.scalar(stmt)
    return QuoteSchema().dump(random_quote)


