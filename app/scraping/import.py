
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
from app.scraping.tag_translations import tag_names, tag_image_urls, tag_descriptions

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

"""

Known tags

'main course', 'free_range', 'snack', 'veryHealthy', 'pescetarian',
'dairy_free', 'latin american', 'south american', 'french', 'morning meal',
'american', 'asian', 'drink', 'primal', 'starter', 'grass_fed', 'sulfite_free',
'southern', 'no_artificial_colors', 'wild_caught', 'grain_free', 'vegetarian',
'sauce', 'breakfast', "hor d'oeuvre", 'glutenFree', 'condiment', 'indian',
'no_additives', 'sugar_free', 'no_artificial_ingredients', 'egg_free',
'kosher', 'pasture_raised', 'irish', 'ketogenic', 'hormone_free', 'vegan',
'appetizer', 'mexican', 'middl eastern', 'wheat_free', 'nut_free',
'veryPopular', 'salad', 'msg_free', 'whole30', 'antipasti', 'soup',
'no_preservatives', 'paleo', 'no_artificial_flavors', 'side dish', 'dip',
'lowFodmap', 'italian', 'fingerfood', 'gluten_free', 'peanut_free', 'brunch',
'main dish', 'fair_trade', 'antipasto', 'mediterranean', 'beverage', 'lunch',
'spread', 'european', 'dessert', 'organic', 'cage_free', 'sustainable',
'gmo_free', 'dinner', 'no_added_sugar', 'soy_free', 'dairyFree', 'corn_free',
'lactose_free'
"""


class Import:
    """
    Imports json data from a directory into a databse.
    """

    recipe_tag_flags = ["cheap", "dairyFree", "glutenFree", "ketogenic",
                        "lowFodmap", "sustainable", "vegan", "vegeterian",
                        "veryHealthy", "veryPopular", "whole30"]

    def __init__(self, data_dir: str, database):
        """
        data_dir - a directory containing the necessary json files.
        database       - a SQLAlchemy database instance.
        """

        self.database = database
        self.data_dir = Path(data_dir)

        self.summary_data = self.read_json("summarize_recipe.json")
        self.find_similar_recipes = self.read_json("find_similar_recipes.json")
        self.get_ingredient_substitutes = \
                self.read_json("get_ingredient_substitutes.json")
        self.get_product_information = \
                self.read_json("get_product_information.json")
        self.get_product_map = self.read_json("get_product_map.json")
        self.recipes = self.read_json("recipes.json")
        self.summarize_recipe = self.read_json("summarize_recipe.json")

        self.recipes = dict()
        self.ingredients = dict()
        self.grocery_items = dict()
        self.tags = dict()
        self.ingredient_substitutes = list()
        self.recipe_ingredients = list()
        self.tag_recipes = list()
        self.tag_ingredients = list()
        self.tag_grocery_items = dict()


    def read_json(self, filename):
        path = self.data_dir / filename
        return json.loads(path.read_text())


    @property
    def session(self):
        return self.database.session

    def commit(self):

        iters = list()
        iters.append(self.recipes.values())
        iters.append(self.ingredients.values())
        iters.append(self.grocery_items.values())
        iters.append(self.tags.values())
        iters.append(self.tag_grocery_items.values())

        iters.append(iter(self.ingredient_substitutes))
        iters.append(iter(self.recipe_ingredients))
        iters.append(iter(self.tag_recipes))
        iters.append(iter(self.tag_ingredients))

        for it in iters:
            for row in it:
                self.session.add(row)

        self.session.commit()

    def run(self):
        """
        Run the importation process.
        """

        recipes = self.read_json("recipes.json")

        for str_id in recipes:
            int_id = int(str_id)
            self.recipe(int_id, recipes[str_id])

        self.commit()

    def recipe_tag(self, recipe_id, spoon_name):
        tag_name = tag_names[spoon_name]
        if tag_name not in self.tags:
            image_url = tag_image_urls[spoon_name]
            description = tag_descriptions[spoon_name]
            self.tags[tag_name] = models.Tag(tag_name, image_url, description)

        self.tag_recipes.append(models.TagRecipe(tag_name, recipe_id))

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
        self.recipes[recipe_id] = recipe

        for flag in self.recipe_tag_flags:
            if recipe_data.get(flag, False):
                self.recipe_tag(recipe_id, flag)

        for cuisine in recipe_data.get("cuisines", {}):
            self.recipe_tag(recipe_id, cuisine)

        for dish_type in recipe_data.get("dishTypes", {}):
            self.recipe_tag(recipe_id, dish_type)

        for ingredient_data in recipe_data.get("extendedIngredients", list()):
            self.ingredient(recipe_id, ingredient_data)


    def ingredient(self, recipe_id, ingredient_data):
        ingredient_id = ingredient_data.get("id", 0)
        if ingredient_id <= 0:
            return

        if ingredient_id not in self.ingredients:

            name = ingredient_data.get("name", None)
            assert(name != None)

            aisle = ingredient_data.get("aisle", None)
            assert(aisle != None)

            self.ingredients[ingredient_id] = (models.Ingredient(ingredient_id, name, "", aisle))

            for subst in self.get_ingredient_substitutes.get(str(ingredient_id), {}).get("substitutes", []):
                self.ingredient_substitutes.append(models.IngredientSubstitute(ingredient_id, subst))

            products = self.get_product_map.get(str(ingredient_id), None)
            if products:
                products = products[0].get("products", [])[:5]
                for product_data in products:
                    self.product(ingredient_id, product_data)

        verbal_quantity = ingredient_data.get("originalString", None)
        assert(verbal_quantity != None)

        self.recipe_ingredients.append(models.RecipeIngredient(recipe_id, ingredient_id, verbal_quantity))


    def product_tag(self, ingredient_id, product_id, spoon_name):
        tag_name = tag_names[spoon_name]
        if tag_name not in self.tags:
            image_url = tag_image_urls.get(spoon_name, "")
            description = tag_descriptions.get(spoon_name, "")
            self.tags[tag_name] = models.Tag(tag_name, image_url, description)

        key = (ingredient_id, product_id, tag_name)
        if key not in self.tag_grocery_items:
            self.tag_grocery_items[key] = models.TagGroceryItem(tag_name, ingredient_id, product_id)
        else:
            print("Ingredient {} product {} has multiple of tag {}.".format(ingredient_id, product_id, tag_name))

    def product(self, ingredient_id, product_data):
        product_id = product_data.get("id", None)
        assert(product_id != None)

        product_info = self.get_product_information[str(product_id)]

        name = product_data["title"]
        upc = product_data["upc"]
        image_url = product_info["images"][1]

        key = (ingredient_id, product_id)
        if key not in self.grocery_items:
            self.grocery_items[key] = models.GroceryItem(product_id, ingredient_id, name, image_url, upc)

            for badge in product_info.get("badges", []):
                self.product_tag(ingredient_id, product_id, badge)
        else:
            print("Ingredient {} contains multiple grocery product {}.".format(ingredient_id, product_id))



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
        self.assertEqual(ingredient.image_url, "")
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
        query = query.filter_by(tag_name="Gluten-free")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(101323, recipe_ids)
        self.assertIn(119007, recipe_ids)
        self.assertIn(125858, recipe_ids)

    def test_tag_cuisine(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="American")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(119007, recipe_ids)
        self.assertIn(165522, recipe_ids)
        self.assertIn(176208, recipe_ids)

    def test_tag_dishtype(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="Lunch")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = (recipe.recipe_id for recipe in recipes)
        self.assertIn(204569, recipe_ids)
        self.assertIn(229298, recipe_ids)
        self.assertIn(270874, recipe_ids)

    def test_tag_badge(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="No artificial colors")
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

    def test_similar_recipes(self):
        query = self.database.session.query(models.Recipe)
        query = query.filter_by(recipe_id=628541)
        recipe = query.first()
        self.assertIsNotNone(recipe)

        expected = {556891, 556749, 557212, 615561, 562151, 556672, 556970, 512186, 512186}

        recipes = recipe.similar_recipes
        actual = {recipe.recipe_id for recipe in recipes}

        self.assertEqual(actual, expected)

    def test_similar_grocery_items(self):
        query = self.database.session.query(models.GroceryItem)
        query = query.filter_by(grocery_id=199371)
        grocery_item = query.first()
        self.assertIsNotNone(grocery_item)

        expected = {410889, 194508, 217511, 141916}

        grocery_items = grocery_item.similar_grocery_items
        actual = {grocery_item.grocery_id for grocery_item in grocery_items}

        self.assertEqual(actual, expected)

    def test_strip_html(self):
        actual = strip_html("<a href=\"google.com\">WOWOWWWOW</a>")
        expected = "WOWOWWWOW"
        self.assertEqual(actual, expected)



def main():
    unittest.main()

if __name__ == "__main__":
    main()
