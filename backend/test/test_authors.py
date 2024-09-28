from app.app import app
from app.extensions import db
from app.authors.author import Author
from app.util.validators import DATE_FORMAT
from datetime import datetime

import pytest

# Run before all tests to clean up in-memory db instance
@pytest.fixture(autouse=True)
def client():
    with app.app_context():
        db.session.query(Author).delete()
        db.session.commit()
    with app.test_client() as testclient:
        yield testclient
        
# Author request objects that are in some way invalid to get 500 response code        
invalid_authors = [
    {
        # incorrect date
        "name": "asas",
        "bio": "Hello",
        "birth_date": "1991-01"
    },
    {
        # empty string
        "name": "",
        "bio": "Hello",
        "birth_date": "1990-01-01"
    },
    {
        # wrong data type
        "name": "ds",
        "bio": 1,
        "birth_date": "1990-01-01"
    },
]

# Valid author object, expecting success
valid_author = {
    "name": "asdas",
    "bio": "hello",
    "birth_date": "1990-01-01"
}

# Updated author object, for comparing in update test
updated_author = {
    "name": "asdas",
    "bio": "bye",
    "birth_date": "1990-01-01"
}


# Testing all validators, they should all fail and result in 500 status code
@pytest.mark.parametrize("request_data", invalid_authors)
def test_validators(client, request_data):
    test_response = client.post("/authors", json=request_data)
    assert test_response.status_code == 500

# Test POST /authors, expecting same data stored except date as that is converted
def test_create_author(client):
    test_response = client.post("/authors", json=valid_author)
    assert test_response.status_code == 200

    response_json = test_response.get_json()
    assert response_json["name"] == valid_author["name"]
    assert response_json["bio"] == valid_author["bio"]

# Test GET /authors with id after adding one data point, expecting it back
def test_get_author(client):
    with app.app_context():
        author_id = "4f859bd4-7c85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=author_id, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))

        test_response = client.get(f"/authors/{author_id}")
        assert test_response.status_code == 200

        response_json = test_response.get_json()
        assert response_json["name"] == valid_author["name"]
        assert response_json["bio"] == valid_author["bio"]

# Test GET /authors after adding two data points, expecting two back
def test_get_authors(client):
    author_id_a = "4f859bd4-7c85-4c71-bd93-d15670bec314"
    author_id_b = "6f859bd4-7c85-4c71-bd93-d15670bec314"
    with app.app_context():
        db.session.add(Author(id=author_id_a, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))
        db.session.add(Author(id=author_id_b, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))

        test_response = client.get("/authors").get_json()
        assert len(test_response) == 2

# Test PUT /authors with ID and updated object, checking after initial response again to ensure update is saved
def test_put_author(client):

    with app.app_context():
        author_id = "5f859bd4-7c85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=author_id, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))

        test_response = client.put(f"/authors/{author_id}", json=updated_author)
        assert test_response.status_code == 200

        test_response = client.get(f"/authors/{author_id}").get_json()
        assert test_response["name"] == valid_author["name"]
        assert test_response["bio"] == updated_author["bio"]

# Test DELETE /authors with ID, checking response code to ensure deletion
def test_delete_author(client):
    with app.app_context():
        author_id = "5f859bd4-7c85-4c71-bd93-d15670bec314"
        db.session.add(Author(id=author_id, name=valid_author['name'], bio=valid_author["bio"], birth_date=datetime.strptime(valid_author["birth_date"], DATE_FORMAT)))

        test_response = client.delete(f"/authors/{author_id}")
        assert test_response.status_code == 200

