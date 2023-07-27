"""
Perform the CRUD operations on the Quote model
"""
from random import randint
from datetime import timedelta
from flask import Blueprint, request
from sqlalchemy import desc, asc
from flask_jwt_extended import jwt_required, create_access_token
from models.user import User, AdminSchema, AdminLoginSchema
from models.quote import Quote, QuoteSchema, QuoteSearchSchema
from init import db, bcrypt

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/all')
def get_all_quotes():
    """
    Get all quotes from quotes table
    """
    stmt = db.select(Quote).order_by(asc(Quote.id))
    quotes = db.session.scalars(stmt).all()
    return QuoteSchema(many=True).dump(quotes)

@quote_bp.route('/all/<int:quote_id>/')
def get_a_quote(quote_id):
    """
    Get quote from quotes table
    """
    stmt = db.select(Quote).filter_by(id=quote_id)
    quote = db.session.scalar(stmt)
    return QuoteSchema().dump(quote)

@quote_bp.route('/')
def get_quote():
    """
    Get a random quote from the dom_quotes table
    """
    # get the range for randint
    # query the database table, order by descending
    stmt = db.select(Quote).order_by(desc(Quote.id))
    quotes = db.session.scalars(stmt).all()

    # set the max range index to list - 1
    max_range = len(quotes) - 1
    # get a random number to use as the index for the quotes list
    random_quote = quotes[randint(1, max_range)]
    return QuoteSchema().dump(random_quote)

@quote_bp.route('/all/search/', methods=['POST'])
def search_quote():
    """
    Search for a quote
    """
    # sanitise incoming data
    search_query = QuoteSearchSchema().load(request.json)
    split_search = search_query['search'].split()
    # add % for SQL like expression
    prep_search_like_stmt = '%'.join(split_search) + '%'
    print(prep_search_like_stmt)
    # query DB
    stmt = db.select(Quote).where(Quote.quote.like(prep_search_like_stmt))
    search_results = db.session.scalars(stmt).all()
    return QuoteSchema(many=True).dump(search_results)

#ADMIN ONLY OPERATIONS
@quote_bp.route('/login', methods=['POST'])
def admin_login():
    """
    Admin only login

    Request Body:

        required fields:

            {
                "email": "admin email",

                "password": "admin password"
            }
    """
    # sanitise the request body
    post_request = AdminLoginSchema().load(request.json)
    # check if admin
    stmt = db.select(User).filter_by(email=post_request['email'])
    admin = db.session.scalar(stmt)
    if admin and bcrypt.check_password_hash(admin.password, post_request['password']):
        # return access token
        token = create_access_token(identity=admin.id, expires_delta=timedelta(minutes=120))
        return {
            "token": token,
            "msg": "admin authenticated"
        }, 200
    return {"invalid_auth": "Valid email address or password required"}, 401


@quote_bp.route('/new/', methods=['POST'])
@jwt_required()
def add_quote():
    """
    ADMIN ONLY

    Add a new quote to the database

    Request Body:

        required fields:

            {
                "quote": "new quote",

                "movie_title": "movie title of quote"
            }
    """
    # sanitise the request body
    post_request = AdminSchema().load(request.json)
    # allow post to database
    new_quote = Quote(
        quote= post_request['quote'],
        movie_title= post_request['movie_title']
    )
    # add and commit the new quote
    db.session.add(new_quote)
    db.session.commit()
    # return quote info and success message
    return {
        "msg": "Quote added to dom_quotes table",
        "quote": QuoteSchema().dump(new_quote)
    }, 201


@quote_bp.route('/all/<int:quote_id>/', methods=['DELETE'])
@jwt_required()
def delete_quote(quote_id):
    """
    ADMIN ONLY

    Delete quote from the database
    """
    # find the quote using the quote id
    stmt = db.select(Quote).filter_by(id=quote_id)
    quote = db.session.scalar(stmt)
    if quote:
        # delete the quote
        db.session.delete(quote)
        db.session.commit()
        return {
            "msg": "Quote deleted"
        }, 200
    return {"not_found": "quote not found"}, 404


@quote_bp.route('/all/<int:quote_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_quote(quote_id):
    """
    ADMIN ONLY

    Update the existing quote in the database
    """
    # find the quote using the quote_id
    stmt = db.select(Quote).filter_by(id=quote_id)
    existing_quote = db.session.scalar(stmt)
    if existing_quote:
        # sanitise the request body
        request_body = AdminSchema().load(request.json)

        existing_quote.quote = request_body.get('quote', existing_quote.quote)
        existing_quote.movie_title = request_body.get('movie_title', existing_quote.movie_title)

        # commit the update
        db.session.commit()
        return QuoteSchema().dump(existing_quote)
    return {"not_found": "quote not found"}, 404
