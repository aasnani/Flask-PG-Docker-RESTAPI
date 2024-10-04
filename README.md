# Dockerized Flask App providing REST API with Postgres Service, tested with Pytest

## Getting Started

### Executing program

Before starting, please copy the provided .env file into the root directory alongside the docker-compose file.

Everything is dockerized. As such simply run the command below to start the program:

```
docker compose up
```

Should you experience some issues, please try the following:

```
docker compose down -v
docker-compose up --force-recreate --build
```

### Testing the program

In order to run the tests, please do the following:
* Change directory into the backend folder
* Install the requirements in requirements.txt
    * If you don't have postgres database installed, please temporarily comment out psycopg2 from the requirements as it may give you trouble. Keep in mind, you will need to uncomment it if you run the program via docker later.
* Run pytest on the test directory

```
cd backend
pip install -r requirements.txt
pytest test/
```

One thing to note is that one test case is not working properly, as noted in the code in test_books.py with instructions on how to manually test it.

## Authors

* Armand Asnani
