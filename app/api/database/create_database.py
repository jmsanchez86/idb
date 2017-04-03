# pylint: disable=missing-docstring

from app.api.database.crud import create_db
from app.api.main import API_SERVICE

if __name__ == "__main__":
    print("Creating new db...")
    create_db(API_SERVICE)
    print("Done!")
