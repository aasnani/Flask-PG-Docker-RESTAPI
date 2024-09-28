from flask import request
import uuid
from datetime import datetime
from ..util.responses import BaseResponse
from ..util.validators import DATE_FORMAT

from ..extensions import db
from .book import Book


def list_all_books() -> list[dict]:
    """ Retrieves all books from database

    Returns:
        Response: JSONified list of all books in database
    """
    books_list = []

    books = Book.query.all()
    
    for book in books: 
        books_list.append(book.toDict())

    return books_list

def create_book(request_json: dict) -> dict:
    """ Creates and returns book from fields found in request JSON

    Returns:
        Response: Newly created JSONified Book object
    """
    book_id = str(uuid.uuid4())

    new_book = Book(
        id = book_id,
        title = request_json['title'],
        description = request_json['description'],
        publish_date = datetime.strptime(request_json['publish_date'], DATE_FORMAT),
        author_id = request_json['author_id']
    )

    db.session.add(instance=new_book)
    db.session.commit()

    
    newBook = db.session.get(entity=Book, ident=book_id)
    
    return newBook.toDict()


def get_book(book_id: str) -> dict:
    """ Retrieve specific book based on id

    Args:
        id (str): id of requested book

    Returns:
        Response: JSONified book object
    """

    book = db.session.get(entity=Book, ident=book_id)

    if not book:
        return {}

    return book.toDict()

def put_book(book_id: str, request_json: dict) -> dict:
    """ Update specific book based on id

    Args:
        book_id (str): id of book to update

    Returns:
        Response: JSONified updated book object
    """

    book = db.session.get(entity=Book, ident=book_id)

    book.title = request_json['title']
    book.description = request_json['description']
    book.publish_date = datetime.strptime(request_json['publish_date'], DATE_FORMAT)
    book.author_id = request_json['author_id']

    db.session.commit()

    updatedBook = db.session.get(entity=Book, ident=book_id)
    
    return updatedBook.toDict()

def delete_book(book_id: str) -> dict:
    """ Delete specific book based on id

    Args:
        book_id (str): id of book to be deleted

    Returns:
        Response: 
    """

    book_delete_count = Book.query.filter(Book.id==book_id).delete()

    db.session.commit()

    response = BaseResponse(
        message=f"Succesfully deleted Book with id: {book_id}",
        )
    
    return response.toDict()

def get_books_by_author(author_id: str) -> list[dict]:
    """ Get all the books by a specific author

    Args:
        author_id (str): Author id of books to retrieve

    Returns:
        list[dict]: list of book objects by the author
    """
    books = Book.query.filter(Book.author_id == author_id).all()
    books_list = []
    for book in books:
        books_list.append(book.toDict())

    return books_list