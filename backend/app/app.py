import os

# App Initialization
from . import create_app 
app, cache, db = create_app()

# Defining routes
from .authors import routes as author_routes
from .books import routes as book_routes

# Starting application
if __name__ == "__main__":
    app.run()