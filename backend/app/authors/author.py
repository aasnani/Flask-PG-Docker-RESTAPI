from ..extensions import db
from sqlalchemy import inspect
from datetime import datetime

# Author table schema and object model definition
class Author(db.Model):
    # Author ID Primary Key
    id = db.Column(db.TEXT, primary_key=True, nullable=False, unique=True)
    # Creation date of object in DB - automatically filled
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.now)
    # Last updated date of object in DB - automatically filled
    last_updated_on = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # Name of Author
    name = db.Column(db.TEXT)
    # Bio of Author
    bio = db.Column(db.TEXT)
    # Author's birth date
    birth_date = db.Column(db.DATE)

    # Relationship that tells db that it is 1-to-many with Book model
    books = db.relationship("Book", backref="author", passive_deletes=True)

    def toDict(self) -> dict:
        """ Converts Author Object into dictionary. 

        Returns:
            dict: dictionary containing attributes as key/value pairs
        """
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self) -> str:
        """ Representation of Author in string format

        Returns:
            str: String representation of object containing id
        """
        return f'<Author id={self.id}>'