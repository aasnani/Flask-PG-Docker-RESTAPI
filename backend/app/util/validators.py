from schema import Schema, And
from datetime import datetime

DATE_FORMAT = f"%Y-%m-%d"

# Date validation function according to constant Date Format
def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except Exception as e:
        return False

# Validate that input arg is both string and non-empty    
def validate_str_and_nonempty(input_str) -> bool:
    if isinstance(input_str, str):
        if len(input_str) > 0:
            return True
    
    return False

# Request schemas to aid in debugging

# Create/Update Author Schema to validate requests on those endpoints, raises SchemaError with error message as defined which is passed to Response for easier debugging
create_update_author_schema = Schema(
    {
        "name": And(validate_str_and_nonempty, error="Check that name is non-empty and is a string"),
        "bio": And(validate_str_and_nonempty, error="Check that bio is non-empty and is a string"),
        "birth_date": And(validate_str_and_nonempty, validate_date, error="Check that birth_date is non-empty, is a string and uses the following date format: YYYY-MM-DD")
    }
)

# Create/Update Book Schema to validate requests on those endpoints, raises SchemaError with error message as defined which is passed to Response for easier debugging
create_update_book_schema = Schema(
    {
        "title": And(validate_str_and_nonempty, error="Check that title is non-empty and is a string"),
        "description": And(validate_str_and_nonempty, error="Check that description is non-empty and is a string"),
        "publish_date": And(validate_str_and_nonempty, validate_date, error="Check that publish_date is non-empty, is a string and uses the following date format: YYYY-MM-DD"),
        "author_id": And(validate_str_and_nonempty, error="Check that title is non-empty, is a string and is in the database")
    }
)

# ID schema to simply check string and non-empty
id_schema = Schema(And(validate_str_and_nonempty, error="Check that id is non-empty and is a string"))
