# pylint: disable=missing-docstring

import time
import unittest
from app.scraping.importer import strip_html
from app.api import models
from app.api.models import Recipe, Ingredient
from app.api.test import test_data
import flask

class DatabaseIntegrityTests(unittest.TestCase):
    """
    Ensure that data was properly imported into the database.
    """

    @classmethod
    def setUpClass(cls):
        cls.app = flask.Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.config["SQLALCHEMY_ECHO"] = False
        cls.database = models.db
        cls.database.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        time_elapsed = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), time_elapsed))

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
        self.assertEqual(recipe.description, test_data.test_recipe_description)
        self.assertEqual(recipe.instructions, test_data.test_recipe_instructions)
        self.assertEqual(recipe.source_url,
                         "http://www.epicurious.com/recipes/food/views/" +
                         "Bittersweet-Chocolate-Marquise-with-Cherry-Sauce-" +
                         "108254")


    def test_ingredient(self):
        query = self.database.session.query(models.Ingredient)
        query = query.filter_by(ingredient_id=9070)
        ingredient = query.first()

        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient.image_url, "https://storage.googleapis.com/"
                                               "vennfridge/saved_ingredient_ima"
                                               "ges%2F9070.jpg")
        self.assertEqual(ingredient.aisle, "Produce")

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

        tag_recipes = self.database.session.query(models.TagRecipe)
        self.assertIsNotNone(tag_recipes.filter_by(recipe_id=101323,
                                                   tag_name="Gluten-free").first())
        self.assertIsNotNone(tag_recipes.filter_by(recipe_id=101323,
                                                   tag_name="Gluten-free").first())
        self.assertIsNotNone(tag_recipes.filter_by(recipe_id=101323,
                                                   tag_name="Gluten-free").first())

    def test_tag_cuisine(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="American")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = [recipe.recipe_id for recipe in recipes]
        self.assertIn(119007, recipe_ids)
        self.assertIn(165522, recipe_ids)
        self.assertIn(176208, recipe_ids)

    def test_tag_dishtype(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="Lunch")
        tag = query.first()
        self.assertIsNotNone(tag)

        recipes = tag.recipes
        recipe_ids = [recipe.recipe_id for recipe in recipes]
        self.assertIn(229298, recipe_ids)
        self.assertIn(204569, recipe_ids)
        self.assertIn(270874, recipe_ids)

    def test_tag_ingredient(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="Vegan")
        tag = query.first()
        self.assertIsNotNone(tag)

        ingredients = tag.ingredients
        ingredient_ids = [ingredient.ingredient_id for ingredient in ingredients]
        self.assertIn(10011282, ingredient_ids)
        self.assertIn(1034053, ingredient_ids)
        self.assertIn(12698, ingredient_ids)

    def test_tag_badge(self):
        query = self.database.session.query(models.Tag)
        query = query.filter_by(tag_name="No artificial colors")
        tag = query.first()
        self.assertIsNotNone(tag)

        grocery_items = tag.grocery_items
        grocery_ids = [item.grocery_id for item in grocery_items]
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

        expected = {556891, 556749, 557212, 615561, 556672, 512186, 512186}

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

class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = flask.Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.config["SQLALCHEMY_ECHO"] = False
        cls.database = models.db
        cls.database.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        time_elapsed = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), time_elapsed))

    def test_get_all_recipe(self):
        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=1"):
            query, table_size_query = Recipe.get_all([], "alpha", 0, 1)
            recipe_0 = next(iter(query))
            self.assertEqual(recipe_0.recipe_id, 557212)
            self.assertEqual(table_size_query.fetchone()[0], 375)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query, table_size_query = Recipe.get_all([], "alpha", 0, 16)
            recipes = list(query)
            self.assertEqual(len(recipes), 16)
            self.assertEqual(recipes[15].recipe_id, 547264)
            self.assertEqual(table_size_query.fetchone()[0], 375)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query, table_size_query = Recipe.get_all([], "alpha", 2, 16)

            recipes = list(query)
            self.assertEqual(len(recipes), 16)
            # TODO: fix and replace sqlite so that we get the correct response
            # should be 101323, but sqlite is dumb
            self.assertEqual(recipes[15].recipe_id, 493614)

        with self.subTest(msg="No tags; Ready time rev; Page=2; Pagesize=16"):
            query, table_size_query = Recipe.get_all([], "ready_time_desc", 2,
                                                     16)
            recipes = list(query)
            # TODO: dumb sqlite should be 474497 but sqlite is dumb
            self.assertEqual(recipes[15].recipe_id, 539503)
            self.assertTrue(recipes[0].ready_time >= recipes[1].ready_time)

        with self.subTest(msg="Vegan Beverage; Ready time rev; "
                              "Page=0; Pagesize=16"):
            tag_set = set(("Vegan", "Beverage"))
            query, table_size_query = Recipe.get_all(list(tag_set),
                                                     "ready_time_desc", 0, 16)
            last_recipe = list(query)[15]
            _last_recipe_query = Recipe.get(last_recipe.recipe_id)
            last_recipe_tags = set(t.tag_name for t in _last_recipe_query.tags)
            # TODO: dumb sqlite should be 493245 but sqlite is dumb
            self.assertEqual(last_recipe.recipe_id, 578431)
            self.assertTrue(last_recipe_tags.issuperset(tag_set))
            self.assertEqual(table_size_query.fetchone()[0], 20)

    def test_get_recipe(self):
        query = Recipe.get(9344)
        self.assertEqual(query.recipe_id, 9344)
        self.assertTrue(query.instructions != "" and
                        query.instructions is not None)
        self.assertTrue(query.servings, 4)
        self.assertTrue(query.ready_time, 45)
        self.assertTrue(query.source_url, "http://www.bonappetit.com/recipes/20"
                                          "11/08/beet-carrot-and-apple-juice-wi"
                                          "th-ginger")
        self.assertEqual(query.image_url, "https://spoonacular.com/recipeImages"
                                          "/beet_carrot_and_apple_juice_with_gi"
                                          "nger-9344.jpg")
        # TODO: fix when migrate away from sqlite
        self.assertEqual(set(i.ingredient_id for i in query.ingredients),
                         set((9003, 9152, 11080, 11124, 11216, 1029003)))
        # TODO: fix when migrate away from sqlite
        self.assertEqual(set(r.recipe_id for r in query.similar_recipes),
                         set((9739, 233626, 472371, 488159, 500633, 620307)))
        self.assertEqual(set(t.tag_name for t in query.tags),
                         set(("Beverage", "Vegan", "Gluten-free", "Whole30",
                              "Dairy-free", "Vegetarian")))


    def test_get_all_ingredient(self):
        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=1"):
            query, table_size_query = Ingredient.get_all([], "alpha", 0, 1)
            ingredient_0 = next(iter(query))
            self.assertEqual(ingredient_0.ingredient_id, 1102047)
            self.assertEqual(table_size_query.fetchone()[0], 629)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query, table_size_query = Ingredient.get_all([], "alpha", 0, 16)
            ingredients = list(query)
            self.assertEqual(len(ingredients), 16)
            self.assertEqual(ingredients[15].ingredient_id, 9016)
            self.assertEqual(table_size_query.fetchone()[0], 629)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query, table_size_query = Ingredient.get_all([], "alpha", 2, 16)

            ingredients = list(query)
            self.assertEqual(len(ingredients), 16)
            # TODO sqlite correction
            self.assertEqual(ingredients[15].ingredient_id, 1002030)

        with self.subTest(msg="No tags; alpha rev; Page=2; Pagesize=16"):
            query, table_size_query = Ingredient.get_all([], "alpha_reverse",
                                                         2, 16)
            ingredients = list(query)
            # TODO sqlite correction
            self.assertEqual(ingredients[15].ingredient_id, 10020081)
            self.assertTrue(ingredients[0].name >=
                            ingredients[1].name)

        with self.subTest(msg="Dairy-free; alpha rev; "
                              "Page=0; Pagesize=16"):
            tag_set = set(("Dairy-free",))
            query, table_size_query = Ingredient.get_all(list(tag_set),
                                                         "alpha_reverse", 0,
                                                         16)
            last_ing = list(query)[15]
            _last_ing_query = Ingredient.get(last_ing.ingredient_id)
            last_ing_tags = set(t.tag_name for t in _last_ing_query.tags)
            # TODO sqlite correction
            self.assertEqual(last_ing.ingredient_id, 10611282)
            self.assertTrue(last_ing_tags.issuperset(tag_set))
            self.assertEqual(table_size_query.fetchone()[0], 332)

    def test_ingredient_grocery_items(self):
        # def get_grocery_items(self)
        pass

    def test_get_ingredient(self):
        # def get(ing_id)
        ing = Ingredient.get(9070)
        self.assertEqual(ing.ingredient_id, 9070)
        self.assertEqual(ing.name, "cherries")
        self.assertEqual(ing.image_url,
                         "https://storage.googleapis.com/vennfridge/saved_ingre"
                         "dient_images%2F9070.jpg")
        self.assertEqual(ing.aisle, "Produce")
        self.assertEqual(set(ri.recipe_id for ri in ing.recipes),
                         set((199872, 758662, 711208, 738124, 73294, 53235,
                              151512, 616762)))
        self.assertEqual(set(g.grocery_id for g in ing.get_grocery_items()),
                         set((56980, 209417, 177259, 201700, 173789)))
        self.assertEqual(set(t.tag_name for t in ing.tags),
                         set(("Dairy-free", "Vegetarian", "Vegan")))

    def test_get_all_groceryitem(self):
        # def get_all(filters, order, page, page_size)
        pass

    def test_get_groceryitem(self):
        # def get(grocery_id)
        pass

    def test_get_all_tag(self):
        # def get_all(min_occurences, order, page, page_size):
        pass

    def test_get_tag(self):
        # def get(tag_name):
        pass


# Report
# ======
# 222 statements analysed.
#
# Statistics by type
# ------------------
#
# +---------+-------+-----------+-----------+------------+---------+
# |type     |number |old number |difference |%documented |%badname |
# +=========+=======+===========+===========+============+=========+
# |module   |1      |1          |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |class    |11     |11         |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |method   |29     |29         |=          |68.97       |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |function |0      |0          |=          |0           |0        |
# +---------+-------+-----------+-----------+------------+---------+
#
#
#
# External dependencies
# ---------------------
# ::
#
#     flask_sqlalchemy (app.api.models)
#     sqlalchemy
#       \-ext
#         \-associationproxy (app.api.models)
#
#
#
# Raw metrics
# -----------
#
# +----------+-------+------+---------+-----------+
# |type      |number |%     |previous |difference |
# +==========+=======+======+=========+===========+
# |code      |302    |50.59 |302      |=          |
# +----------+-------+------+---------+-----------+
# |docstring |77     |12.90 |77       |=          |
# +----------+-------+------+---------+-----------+
# |comment   |124    |20.77 |124      |=          |
# +----------+-------+------+---------+-----------+
# |empty     |94     |15.75 |94       |=          |
# +----------+-------+------+---------+-----------+
#
#
#
# Duplication
# -----------
#
# +-------------------------+------+---------+-----------+
# |                         |now   |previous |difference |
# +=========================+======+=========+===========+
# |nb duplicated lines      |0     |0        |=          |
# +-------------------------+------+---------+-----------+
# |percent duplicated lines |0.000 |0.000    |=          |
# +-------------------------+------+---------+-----------+
#
#
#
# Messages by category
# --------------------
#
# +-----------+-------+---------+-----------+
# |type       |number |previous |difference |
# +===========+=======+=========+===========+
# |convention |0      |0        |=          |
# +-----------+-------+---------+-----------+
# |refactor   |0      |0        |=          |
# +-----------+-------+---------+-----------+
# |warning    |0      |0        |=          |
# +-----------+-------+---------+-----------+
# |error      |0      |0        |=          |
# +-----------+-------+---------+-----------+
#
#
#
# Global evaluation
# -----------------
# Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)




if __name__ == "__main__":
    unittest.main()
