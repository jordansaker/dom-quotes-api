"""
Perform the CRUD operations on the Quote model
"""
from random import randint
from datetime import timedelta
from flask import Blueprint, request
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, create_access_token
from models.user import User, AdminSchema, AdminLoginSchema
from models.quote import Quote, QuoteSchema
from init import db, bcrypt

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


@quote_bp.route('/', methods=['POST'])
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


@quote_bp.route('/<int:quote_id>', methods=['DELETE'])
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


@quote_bp.route('/<int:quote_id>', methods=['PUT', 'PATCH'])
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
