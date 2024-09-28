from flask import Flask

from app.config import Config
from app.extensions import db
from app.extensions import cache

def create_app(config_class=Config):
    # Initialize Flask App
    app = Flask(__name__)

    # Import config from config class
    app.config.from_object(config_class)

    # Initializing SQLAlchemy extension with Flask app
    db.init_app(app)

    # Initializing Flask Caching
    cache.init_app(app)

    # Importing all models to include into SQLAlchemy Metadata
    from .authors.author import Author
    from .books.book import Book

    with app.app_context():
        # Create all tables according to schema from model in metadata
        db.create_all()

    return app, cache, db