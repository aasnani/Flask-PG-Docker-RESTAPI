from flask import Response, request
import uuid
from datetime import datetime
from ..util.responses import BaseResponse
from ..util.validators import DATE_FORMAT

from ..extensions import db
from .author import Author

def list_all_authors() -> list[dict]:
    """ Retrieves all authors from database

    Returns:
        Response: JSONified list of all authors in database
    """
    authors_list = []

    authors = Author.query.all()
    
    for author in authors: 
        authors_list.append(author.toDict())

    return authors_list

def create_author(request_json: dict) -> dict:
    """ Creates and returns author from fields found in request JSON

    Returns:
        Response: Newly created JSONified Author object
    """

    author_id = str(uuid.uuid4())
    new_author = Author(
                        id = author_id,
                        name = request_json['name'],
                        bio = request_json['bio'],
                        birth_date  = datetime.strptime(request_json['birth_date'], DATE_FORMAT),
                        )
    db.session.add(instance=new_author)
    db.session.commit()

    newAuthor = db.session.get(entity=Author, ident=author_id)
    
    return newAuthor.toDict()

def get_author(author_id: str) -> dict:
    """ Retrieve specific author based on id

    Args:
        id (str): id of requested author

    Returns:
        Response: JSONified author object
    """

    author = db.session.get(entity=Author, ident=author_id)

    if not author:
        return {}


    return author.toDict()

def put_author(author_id: str, request_json: dict) -> dict:
    """ Update specific author based on id

    Args:
        author_id (str): id of author to update

    Returns:
        Response: JSONified updated author object
    """


    author = db.session.get(entity=Author, ident=author_id)

    author.name = request_json['name'] 
    author.bio = request_json['bio'] 
    author.birth_date = datetime.strptime(request_json['birth_date'], DATE_FORMAT) 

    db.session.commit()

    updatedAuthor = db.session.get(entity=Author, ident=author_id)
    
    return updatedAuthor.toDict()

def delete_author(author_id: str) -> dict:
    """ Delete specific author based on id

    Args:
        author_id (str): id of author to be deleted

    Returns:
        Response: 
    """

    author_delete_count = Author.query.filter(Author.id==author_id).delete()

    db.session.commit()

    response = BaseResponse(
        message=f"Succesfully deleted Author with id: {author_id}",
        )
    
    return response.toDict()