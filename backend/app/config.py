import os

# Configuration class for flask app config
class Config:
    # Setting config variable for SQLAlchemy DB Connection String
    # When it is undefined as in testing mode, defaults to in memory SQLite DB allowing for test w/o docker
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONNECTION_STRING', 'sqlite://')