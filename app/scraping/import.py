
"""
Imports json data into the database.
"""

from pathlib import Path
from flask import Flask
from app.api import models

class Import:
    """
    Imports json data from a directory into a databse.
    """

    def __init__(self, data_dir:str, db):
        """
        data_dir - a directory containing the necessary json files.
        db       - a SQLAlchemy database instance.
        """

        self.db = db
        self.data_dir = Path(data_dir)

    def run(self):
        """
        Run the importation process.
        """

        ingredient = models.Ingredient(8, "star anise", "someimage.jpg")
        self.db.session.add(ingredient)
        self.db.session.commit()

    # TODO: Remove this and add proper unit tests.
    def check(self):
        """
        Make some basic data integrity checks.
        """

        query = self.db.session.query(models.Ingredient).filter_by(name="star anise")
        ingredient = query.first()

        assert ingredient.ingredient_id == 8


if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    models.db.init_app(app)
    ctx = app.app_context()
    ctx.push()
    models.db.create_all()

    imp = Import("data", models.db)
    imp.run()
    imp.check()

    ctx.pop()


