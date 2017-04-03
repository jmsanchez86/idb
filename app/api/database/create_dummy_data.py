# pylint: disable=missing-docstring

from app.api.main import API_SERVICE
from app.api.database.crud import init_db, add_random_ingredient

if __name__ == "__main__":
    with API_SERVICE.app_context():
        init_db(API_SERVICE)
        add_random_ingredient()
