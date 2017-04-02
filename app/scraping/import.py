
# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=pointless-string-statement
# pylint: disable=too-few-public-methods

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

    def __init__(self, data_dir: str, database):
        """
        data_dir - a directory containing the necessary json files.
        database       - a SQLAlchemy database instance.
        """

        self.database = database
        self.data_dir = Path(data_dir)

    def run(self):
        """
        Run the importation process.
        """

        ingredient = models.Ingredient(8, "star anise", "someimage.jpg")
        self.database.session.add(ingredient)
        self.database.session.commit()


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
        cls.database = models.db
        cls.database.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        cls.database.create_all()

        imp = Import("data", models.db)
        imp.run()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_recipe(self):
        query = self.database.session.query(models.Recipe)
        query = query.filter_by(recipe_id=151512)
        recipe = query.first()

        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, "Bittersweet Chocolate Marquise with " +
                         "Cherry Sauce")
        self.assertEqual(recipe.image_url, "https://spoonacular.com/" +
                         "recipeImages/bittersweet-chocolate-marquise-with-" +
                         "cherry-sauce-151512.jpg")

        with open("recipe_description.txt", "r", encoding="utf-8") as desc_file:
            self.assertEqual(recipe.instructions, desc_file.read())

    def test_ingredient(self):
        query = self.database.session.query(models.Ingredient)
        query = query.filter_by(ingredient_id=9070)
        ingredient = query.first()

        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient.name, "cherries")

        # TODO: Test image_url

    def test_grocery_item(self):
        query = self.database.session.query(models.GroceryItem)
        query = query.filter_by(grocery_id=109704)
        grocery_item = query.first()

        self.assertIsNotNone(grocery_item)
        self.assertEqual(grocery_item.name, "Lee Kum Kee Sriracha Chili Sauce")
        self.assertEqual(grocery_item.image_url, "https://spoonacular.com/" +
                         "productImages/109704-636x393.jpg")
        self.assertEqual(grocery_item.upc, "742812730712")


    def test_tag_flag(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="glutenFree")
        tag = query.first()

        recipes = tag.recipes()
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(101323, recipe_ids)
        self.assertIn(102715, recipe_ids)
        self.assertIn(106529, recipe_ids)

    def test_tag_cuisine(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="american")
        tag = query.first()

        recipes = tag.recipes()
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(119007, recipe_ids)
        self.assertIn(165522, recipe_ids)
        self.assertIn(176208, recipe_ids)

    def test_tag_dishtype(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="lunch")
        tag = query.first()

        recipes = tag.recipes()
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(204569, recipe_ids)
        self.assertIn(229298, recipe_ids)
        self.assertIn(270874, recipe_ids)

    def test_tag_badge(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="no_artificial_colors")
        tag = query.first()

        grocery_items = tag.grocery_items()
        grocery_ids = (item.grocery_id for item in grocery_items)
        self.assertIn(101017, grocery_ids)
        self.assertIn(101280, grocery_ids)
        self.assertIn(102111, grocery_ids)


    def test_recipe_ingredients(self):
        query = self.database.session.query(models.Recipe)
        query = query.filter_by(recipe_id=510562)
        recipe = query.first()

        expected = {(9019, "1/4 applesauce"),
                    (18372, "1/2 teaspoon baking soda"),
                    (19334, "1/4 cup packed brown sugar"),
                    (1001, "1/4 cup butter, softened"),
                    (2010, "1/2 teaspoon cinnamon"),
                    (9079, "3/4 cup dried cranberries"),
                    (1123, "1 large egg"),
                    (20081, "1/2 cup all-purpose flour"),
                    (8402, "1 1/2 cups quick-cooking oats (not instant)"),
                    (2047, "1/4 teaspoon salt"),
                    (19335, "3/4 cup sugar"),
                    (2050, "1/2 teaspoon vanilla extract"),
                    (20081, "1/2 cup wheat flour"),
                    (10019087, "4 ounces white chocolate chips")}


        ingredients = recipe.ingredients()
        actual = ((ing.ingredient_id,
                   ing.quantity_verbal) for ing in ingredients)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
