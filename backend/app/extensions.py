from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Instantiating Flask extension objects

# Database object storing all models and for interacting with DB
db = SQLAlchemy()

# Cache object storing all cached preferences and results
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})