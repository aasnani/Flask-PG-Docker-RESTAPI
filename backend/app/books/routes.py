from flask import jsonify, request

from ..app import app
from .controller import list_all_books, create_book, get_book, put_book, delete_book, get_books_by_author
from ..util.responses import BaseResponse
from ..util.validators import id_schema, create_update_book_schema
from ..extensions import cache


# Defining all author related API endpoints as per document

logger = app.logger

def id_cache_key(book_id: str) -> str:
    return book_id

def aid_cache_key(author_id: str) -> str:
    return 'books' + author_id


@app.route("/books", methods=['GET'])
@cache.cached(timeout=10, key_prefix="getbooks")
def list_books():
    try:
        return jsonify(list_all_books())
    except Exception as e:
        logger.error("GET /book failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem getting all the book objects: {str(e)}")
    return jsonify(response.toDict()), 500

@app.route("/books", methods=['POST'])
def create_books():
    try:
        validated_response_json = create_update_book_schema.validate(request.get_json())
        return jsonify(create_book(request_json=validated_response_json))
    except Exception as e:
        logger.error("POST /book failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem creating the book object: {str(e)}")
        return jsonify(response.toDict()), 500
    
@app.route("/books/<book_id>", methods=['GET'])
@cache.cached(timeout=10, make_cache_key=id_cache_key)
def get_book_by_id(book_id):
    try:
        validated_id = id_schema.validate(book_id)
        return jsonify(get_book(book_id=validated_id))
    except Exception as e:
        logger.error(f"GET /book/{book_id} failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem getting the book object with id={book_id}: {str(e)}")
        return jsonify(response.toDict()), 500


@app.route("/books/<book_id>", methods=['PUT'])
@cache.cached(timeout=10, make_cache_key=id_cache_key)
def put_book_by_id(book_id):
    try:
        validated_id = id_schema.validate(book_id)
        validated_request_json = create_update_book_schema.validate(request.get_json())
        return jsonify(put_book(book_id=validated_id, request_json=validated_request_json))
    except Exception as e:
        logger.error(f"PUT /book/{book_id} failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem updating the author object with id={book_id}: {str(e)}")
        return jsonify(response.toDict()), 500

@app.route("/books/<book_id>", methods=['DELETE'])
@cache.cached(timeout=10, make_cache_key=id_cache_key)
def delete_book_by_id(book_id):
    try:
        validated_id = id_schema.validate(book_id)
        return jsonify(delete_book(book_id=validated_id))
    except Exception as e:
        logger.error(f"DELETE /book/{book_id} failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem deleting the book object with id={book_id}: {str(e)}")
        return jsonify(response.toDict()), 500
    
@app.route("/authors/<author_id>/books", methods=["GET"])
@cache.cached(timeout=10, make_cache_key=aid_cache_key)
def get_books_of_author(author_id):
    try:
        validated_id = id_schema.validate(author_id)
        return jsonify(get_books_by_author(author_id=validated_id))
    except Exception as e:
        logger.error(f"GET /author/{author_id}/books failed with message:", str(e), exc_info=True)
        response = BaseResponse(f"There was a problem getting the book objects of Authors with id={author_id}: {str(e)}")
        return jsonify(response.toDict()), 500