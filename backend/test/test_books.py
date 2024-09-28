from app.app import app
from app.extensions import db
from app.authors.author import Author
from app.books.book import Book
from app.util.validators import DATE_FORMAT
from datetime import datetime

import pytest

# Run before all tests to clean up in-memory db instance
@pytest.fixture(autouse=True)
def client():
    with app.app_context():
        db.session.query(Author).delete()
        db.session.query(Book).delete()
        db.session.commit()
    with app.test_client() as testclient:
        yield testclient

# Book request objects that are in some way invalid to get 500 response code
invalid_books = [
    {
        # empty string
        "title": "",
        "description": "des",
        "publish_date": "1990-01-01",
        "author_id": "4f859bd4-7c85-4c71-bd93-d15670bec314"
    },
    {
        # wrong data type
        "title": "tile",
        "description": 1,
        "publish_date": "1990-01-01",
        "author_id": "4f859bd4-7c85-4c71-bd93-d15670bec314"
    },
    {
        # wrong date format
        "title": "tie",
        "description": "dec",
        "publish_date": "1990-01",
        "author_id": "4f859bd4-7c85-4c71-bd93-d15670bec314"
    },
    # NOTICE: test case not functional using SQLite DB, can be tested via creating book via API without any authors when running main application
    # { 
    #     # violate foreign key constraint with invalid author_id
    #     "title": "book",
    #     "description": "book",
    #     "publish_date": "1990-01-01",
    #     "author_id": "f8664c59-4270-4a74-9ca5-f4f8dab4d1da"
    # }
]

# Valid author object as single author is always needed in the database for a book object
valid_author = {
    "id": "4f859bd4-7c85-4c71-bd93-d15670bec314",
    "name": "asdas",
    "bio": "hello",
    "birth_date": "1990-01-01"
}

# Valid book object, expecting success
valid_book = {
    "title": "title",
    "description": "desc",
    "publish_date": "1990-01-01",
    "author_id": valid_author["id"]
}

# Updated book object, for comparing in update test
updated_book = {
    "title": "title",
    "description": "description",
    "publish_date": "1990-01-01",
    "author_id": valid_author["id"]
}

# Testing all validators, they should all fail and result in 500 status code
@pytest.mark.parametrize("request_data", invalid_books)
def test_validators(client, request_data):
    with app.app_context():
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        test_response = client.post("/books", json=request_data)
        assert test_response.status_code == 500

# Test POST /books, expecting same data stored except date as that is converted
def test_create_book(client):

    with app.app_context():
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        test_response = client.post("/books", json=valid_book)
        assert test_response.status_code == 200
        response_json = test_response.get_json()
        assert response_json["title"] == valid_book["title"]
        assert response_json["description"] == valid_book["description"]
        assert response_json["author_id"] == valid_book["author_id"]

# Test GET /books with id after adding one data point, expecting it back
def test_get_book(client):
    with app.app_context():
        book_id = "3f849bd4-7a85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Book(id=book_id, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=valid_author["id"]))

        test_response = client.get(f"/books/{book_id}")
        assert test_response.status_code == 200

        response_json = test_response.get_json()
        assert response_json["title"] == valid_book["title"]
        assert response_json["description"] == valid_book["description"]
        assert response_json["author_id"] == valid_book["author_id"]

# Test GET /books after adding two data points, expecting two back
def test_get_books(client):
    with app.app_context():
        book_id_a = "3f849bd4-7a85-4c71-bd93-d15670bec314"
        book_id_b = "3f849bd4-7a85-4c71-bd93-d15670bec315"
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Book(id=book_id_a, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=valid_author["id"]))
        db.session.add(Book(id=book_id_b, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=valid_author["id"]))

        test_response = client.get("/books")
        assert test_response.status_code == 200

        response_json = test_response.get_json()
        assert len(response_json) == 2

# Test PUT /books with ID and updated object, checking after initial response again to ensure update is saved
def test_put_book(client):
    with app.app_context():
        book_id = "1f849bd4-7a85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Book(id=book_id, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=valid_author["id"]))

        test_response = client.put(f"/books/{book_id}", json=updated_book)
        assert test_response.status_code == 200

        test_response = client.get(f"/books/{book_id}")

        response_json = test_response.get_json()
        assert response_json["title"] == valid_book["title"]
        assert response_json["description"] == updated_book["description"]
        assert response_json["author_id"] == valid_book["author_id"]

# Test DELETE /books with ID, checking response code to ensure deletion
def test_delete_book(client):
    with app.app_context():
        book_id = "9f849bd4-7a85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=valid_author["id"], name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Book(id=book_id, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=valid_author["id"]))

        test_response = client.delete(f"/books/{book_id}")
        assert test_response.status_code == 200

        test_response = client.get(f"/books/{book_id}")

# Test GET /authors/<author_id>/books with id to get all books by an author
def test_get_books_by_author(client):
    with app.app_context():
        book_id = "6f849bd4-7a85-4c71-bd93-d15670bec314"
        author_id = "f8664c59-4270-4a74-9ca5-f4f8dab4d1da"
        db.session.add(Author(id=author_id, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Book(id=book_id, title=valid_book["title"], description=valid_book["description"], publish_date=datetime.strptime(valid_book["publish_date"], DATE_FORMAT), author_id=author_id))

        test_response = client.get(f"/authors/{author_id}/books")
        assert test_response.status_code == 200
        
        response_json = test_response.get_json()
        assert len(response_json) == 1

