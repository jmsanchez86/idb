
"""
Imports json data into the database.
"""

import unittest
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


class TestDatabaseIntegrity(unittest.TestCase):
    """
    Ensure that data was properly imported into the database.
    """

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.config["SQLALCHEMY_ECHO"] = False
        cls.db = models.db
        cls.db.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        cls.db.create_all()

        imp = Import("data", models.db)
        imp.run()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_ingredient(self):
        query = self.db.session.query(models.Ingredient).filter_by(name="star anise")
        ingredient = query.first()

        self.assertEqual(ingredient.ingredient_id, 8)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

