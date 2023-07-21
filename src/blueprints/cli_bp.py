"""
CLI Blueprints

The following commands are run in the CLI. To invoke a command in the blue print:

       ``flask cli <command>``

Commands:

    ``create`` - create tables in the database

    ``drop`` - drop the existing tables in the database

    ``seed`` - seed the existing tables in the database
"""
from flask import Blueprint
from models.quote import Quote
from models.user import User
from init import db, bcrypt

cli_bp = Blueprint('cli', __name__)

@cli_bp.cli.command('create')
def create_tables():
    """Create tables in the database using the defined models"""
    db.create_all()
    print('Tables created')


@cli_bp.cli.command('drop')
def drop_tables():
    """Drop tables in the database"""
    db.drop_all()
    print('Tables dropped')

@cli_bp.cli.command('seed')
def seed_tables():
    """
    Seed the existing tables in the database
    """
    # seed the dom_quotes table
    quotes = [
        Quote(
            quote= "Ask any racer. Any real racer. It doesn't matter if you win by an inch\
 or a mile. Winning's winning.",
            movie_title= "Fast And The Furious"
        ),
        Quote(
            quote= "I don't have friends, I have a family.",
            movie_title= "Fast & Furious 7"
        ),
        Quote(
            quote= "I choose to make my own fate.",
            movie_title= "The Fate Of The Furious"
        ),
        Quote(
            quote= "I don't feel like I'm under arrest.",
            movie_title= "Fast Five"
        ),
        Quote(
            quote= "Show me how you drive, It'll show you who you are.",
            movie_title= "Fast And The Furious"
        ),
        Quote(
            quote= "I said a ten-second car, not a ten-minute car.",
            movie_title= "Fast And The Furious"
        )
    ]
    user = User(
        email= 'adminDom@family.com',
        password= bcrypt.generate_password_hash('WeAreFamilyDomTorretto').decode('utf8')
    )
    # add and commit the list
    db.session.add_all(quotes)
    db.session.add(user)
    db.session.commit()
    print('Tables seeded')
