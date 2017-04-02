
"""
Imports json data into the database.
"""

from pathlib import Path
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

    def run():
        """
        Run the importation process.
        """

        models.Ingredient(8, "star anise", "somesite.com/image/star_anise.jpg")


if __name__ == "__main__":
    imp = Import("data", models.db)
    imp.run()


