from ..extensions import db
from sqlalchemy import inspect
from datetime import datetime

# Book table schema and object model definition
class Book(db.Model):
    
    # Book ID primary key
    id = db.Column(db.TEXT, primary_key=True, nullable=False, unique=True)
    # Creation date of object in DB - automatically filled
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.now)
    # Last updated date of object in DB - automatically filled
    last_updated_on = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # Book title
    title = db.Column(db.TEXT)
    # Book description
    description = db.Column(db.TEXT)
    # Book publish date
    publish_date = db.Column(db.DATE)

    # Foreign key relationship to Author id to ensure constraint
    author_id = db.Column(db.TEXT, db.ForeignKey("author.id", ondelete="CASCADE"), nullable=False)

    def toDict(self) -> dict:
        """ Converts Book Object into dictionary. 

        Returns:
            dict: dictionary containing attributes as key/value pairs
        """
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self) -> str:
        """ Representation of Book in string format

        Returns:
            str: String representation of object containing id
        """
        return f'<Author id={self.id}>'