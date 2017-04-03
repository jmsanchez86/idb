
# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=pointless-string-statement
# pylint: disable=too-few-public-methods

"""
Imports json data into the database.
"""

import unittest
import json
import re
from pathlib import Path
from flask import Flask
from app.api import models

def strip_html(html):
    """
    Remove all html tags from a string.
    """
    # TODO: Remove all html tags if necessary
    stripper = re.compile("<a.*?>")
    html = re.sub(stripper, "", html)

    stripper = re.compile("</a>")
    html = re.sub(stripper, "", html)

    return html

class Import:
    """
    Imports json data from a directory into a databse.
    """

    recipe_tag_flags = ["cheap", "dairyFree", "glutenFree", "ketogenic",
                        "lowFodmap", "sustainable", "vegan", "vegeterian",
                        "veryHealthy", "veryPopular", "whole30"]

    tag_image_urls = {}
    tag_descriptions = {}

    def __init__(self, data_dir: str, database):
        """
        data_dir - a directory containing the necessary json files.
        database       - a SQLAlchemy database instance.
        """

        self.database = database
        self.data_dir = Path(data_dir)

    def read_json(self, filename):
        path = self.data_dir / filename
        return json.loads(path.read_text())


    @property
    def session(self):
        return self.database.session

    def run(self):
        """
        Run the importation process.
        """

        self.summary_data = self.read_json("summarize_recipe.json")

        recipes = self.read_json("recipes.json")

        for str_id in recipes:
            int_id = int(str_id)
            self.recipe(int_id, recipes[str_id])

    def recipe_tag(self, recipe_id, tag_name):
        query = self.session.query(models.Tag)
        query = query.filter_by(tag_name=tag_name)
        if not query.count():
            image_url = self.tag_image_urls.get(tag_name, "")
            description = self.tag_descriptions.get(tag_name, "")
            self.session.add(models.Tag(tag_name, image_url, description))

        self.session.add(models.TagRecipe(tag_name, recipe_id))

    def recipe(self, recipe_id, recipe_data):

        name = recipe_data.get("title", "")
        image_url = recipe_data.get("image", "")
        instructions = strip_html(recipe_data.get("instructions", "") or "")
        ready_time = recipe_data.get("readyInMinutes", 0)
        servings = recipe_data.get("servings", 0)

        summary_data = self.summary_data.get(str(recipe_id), None)
        summary = (summary_data and strip_html(summary_data.get("summary", ""))
                   or "")

        recipe = models.Recipe(recipe_id, name, image_url, instructions,
                               summary, ready_time, servings)
        self.session.add(recipe)

        for flag in self.recipe_tag_flags:
            if recipe_data.get(flag, False):
                self.recipe_tag(recipe_id, flag)

        for cuisine in recipe_data.get("cuisines", {}):
            self.recipe_tag(recipe_id, cuisine)

        for dish_type in recipe_data.get("dishTypes", {}):
            self.recipe_tag(recipe_id, dish_type)

        for ingredient_data in recipe_data.get("extendedIngredients", []):
            self.ingredient(ingredient_data)

    def ingredient(self, ingredient_data):
        ingredient_id = ingredient_data.get("id", 0)
        if ingredient_id > 0:
            return


        query = self.session.query(models.Ingredient)
        query = query.filter_by(ingredient_id=ingredient_id)
        if not query.count():

            name = ingredient_data.get("name", None)
            assert(name != None)

            aisle = ingredient_data.get("aisle", None)
            assert(aisle != None)

            self.session.add(models.Ingredient(ingredient_id, name, "",
                             aisle))



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
        self.assertEqual(recipe.ready_time, 45)
        self.assertEqual(recipe.servings, 12)
        self.assertEqual(recipe.name, "Bittersweet Chocolate Marquise with " +
                         "Cherry Sauce")
        self.assertEqual(recipe.image_url, "https://spoonacular.com/" +
                         "recipeImages/bittersweet-chocolate-marquise-with-" +
                         "cherry-sauce-151512.jpg")

        with open("recipe_description.txt", "r", encoding="utf-8") as desc_file:
            self.assertEqual(recipe.description + '\n', desc_file.read())

        with open("recipe_instructions.txt", "r", encoding="utf-8") as desc_file:
            self.assertEqual(recipe.instructions + '\n', desc_file.read())



    def test_ingredient(self):
        query = self.database.session.query(models.Ingredient)
        query = query.filter_by(ingredient_id=9070)
        ingredient = query.first()

        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient.name, "cherries")
        self.assertEqual(ingredient.image_url, "https://spoonacular.com/cdn/ingredients_100x100/cherries.jpg")
        self.assertEqual(ingredient.aisle, "Produce")

        # TODO: Test image_url

    def test_grocery_item(self):
        query = self.database.session.query(models.GroceryItem)
        query = query.filter_by(grocery_id=109704, ingredient_id=6972)
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

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(101323, recipe_ids)
        self.assertIn(119007, recipe_ids)
        self.assertIn(125858, recipe_ids)

    def test_tag_cuisine(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="american")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(119007, recipe_ids)
        self.assertIn(165522, recipe_ids)
        self.assertIn(176208, recipe_ids)

    def test_tag_dishtype(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="lunch")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(204569, recipe_ids)
        self.assertIn(229298, recipe_ids)
        self.assertIn(270874, recipe_ids)

    def test_tag_badge(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="no_artificial_colors")
        tag = query.first()
        self.assertIsNotNone(tag)

        grocery_items = tag.grocery_items
        grocery_ids = (item.grocery_id for item in grocery_items)
        self.assertIn(101017, grocery_ids)
        self.assertIn(101280, grocery_ids)
        self.assertIn(102111, grocery_ids)

    def test_ingredient_substitutes(self):
        query = self.database.session.query(models.Ingredient)
        query = query.filter_by(ingredient_id=11959)
        ingredient = query.first()
        self.assertIsNotNone(ingredient)

        substitutes = ingredient.substitutes
        expected = {"1 cup = 1 cup watercress",
                    "1 cup = 1 cup escarole",
                    "1 cup = 1 cup belgian endive",
                    "1 cup = 1 cup radicchio",
                    "1 cup = 1 cup baby spinach"}

        actual = {substitute.substitute for substitute in substitutes}

        self.assertEqual(actual, expected)

    def test_recipe_ingredients(self):
        query = self.database.session.query(models.Recipe)
        query = query.filter_by(recipe_id=510562)
        recipe = query.first()
        self.assertIsNotNone(recipe)

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


        ingredients = recipe.ingredients
        actual = {(ing.ingredient_id,
                   ing.verbal_quantity) for ing in ingredients}

        self.assertEqual(actual, expected)

    def test_strip_html(self):
        actual = strip_html("<a href=\"google.com\">WOWOWWWOW</a>")
        expected = "WOWOWWWOW"
        self.assertEqual(actual, expected)



def main():
    unittest.main()

if __name__ == "__main__":
    main()
