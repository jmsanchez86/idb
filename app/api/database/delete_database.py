# pylint: disable=missing-docstring

from app.api.main import API_SERVICE
from app.api import models

if __name__ == "__main__":
    print("deleting...")
    with API_SERVICE.app_context():
        models.db.engine.execute("drop schema if exists public cascade")
        models.db.engine.execute("create schema public")
        models.db.engine.execute("grant all on schema public to postgres")
        models.db.engine.execute("grant all on schema public to public")
    print("done deleting")
