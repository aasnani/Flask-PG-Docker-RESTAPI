from flask import jsonify, request

from ..app import app
from .controller import list_all_authors, create_author, get_author, put_author, delete_author
from ..util.responses import BaseResponse
from ..util.validators import create_update_author_schema, id_schema
from ..extensions import cache

# Defining all author related API endpoints as per document

logger = app.logger

# Cache key function to get key to store cached results for end points involving id path argument
def id_cache_key(author_id: str) -> str:
    return author_id

@app.route("/authors", methods=['GET'])
@cache.cached(timeout=10, key_prefix="getauthors") # Cache definition
def list_authors():
    try:
        # controller method interacting with db
        return list_all_authors()
    except Exception as e:
        # logging output for any errors
        logger.error(msg=f"GET /author failed with message: {str(e)}", exc_info=True)
        # standardized response object
        response = BaseResponse(message=f"There was a problem getting all the author objects: {str(e)}")
        # 500 error catch-all
        return jsonify(response.toDict()), 500

@app.route("/authors", methods=['POST'])
def create_authors():
        try:
            # Validations by schema as defined for create/update authors
            validated_request_json = create_update_author_schema.validate(request.get_json())
            return create_author(request_json=validated_request_json)

        except Exception as e:
            logger.error(msg=f"POST /author failed with message: {str(e)}", exc_info=True)
            response = BaseResponse(message=f"There was a problem creating the author object: {str(e)}")
            return jsonify(response.toDict()), 500

@app.route("/authors/<author_id>", methods=['GET'])
@cache.cached(timeout=10, key_prefix="getauthor", make_cache_key=id_cache_key)
def get_author_by_id(author_id):
    try:
        # Validations as defined for id path arguments in request URL
        validated_author_id = id_schema.validate(author_id)
        return get_author(author_id=validated_author_id)
    except Exception as e:
        logger.error(msg=f"GET /author/{author_id} failed with message: {str(e)}", exc_info=True)
        response = BaseResponse(message=f"There was a problem getting the author object with id={author_id}: {str(e)}")
        return jsonify(response.toDict()), 500

@app.route("/authors/<author_id>", methods=['PUT'])
@cache.cached(timeout=10, key_prefix="putauthor", make_cache_key=id_cache_key)
def put_author_by_id(author_id):
    try:
        validated_author_id = id_schema.validate(author_id)
        validated_request_json = create_update_author_schema.validate(request.get_json())
        return put_author(author_id=validated_author_id, request_json=validated_request_json)
    except Exception as e:
        logger.error(msg=f"PUT /author/{author_id} failed with message: {str(e)}", exc_info=True)
        response = BaseResponse(message=f"There was a problem updating the author object with id={author_id}: {str(e)}")
        return jsonify(response.toDict()), 500
    
@app.route("/authors/<author_id>", methods=['DELETE'])
@cache.cached(timeout=10, key_prefix="deleteauthor", make_cache_key=id_cache_key)
def delete_author_by_id(author_id):
    try:
        validated_author_id = id_schema.validate(author_id)
        return delete_author(author_id=validated_author_id)
    except Exception as e:
        logger.error(msg=f"DELETE /author/{author_id} failed with message: {str(e)}", exc_info=True)
        response = BaseResponse(message=f"There was a problem deleting the author object with id={author_id}: {str(e)}")
        return jsonify(response.toDict()), 500
