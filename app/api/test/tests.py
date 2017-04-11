# pylint: disable=missing-docstring
# pylint: disable=fixme

import time
import unittest
from app.scraping.importer import strip_html
from app.api import models
from app.api.models import Recipe, Ingredient, GroceryItem, Tag
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
            self.assertTrue(ingredients[0].name >= ingredients[1].name)

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

    def test_get_ingredient(self):
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

    def test_ingredient_grocery_items(self):
        ing = Ingredient.get(93653)
        grocery_items = ing.get_grocery_items()
        self.assertEqual(set(g.grocery_id for g in grocery_items),
                         set((131706, 21194, 195045)))

    def test_get_all_groceryitem(self):
        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=1"):
            query, table_size_query = GroceryItem.get_all([], "alpha", 0, 1)
            item_0 = next(iter(query))
            self.assertEqual(item_0.grocery_id, 95469)
            self.assertEqual(table_size_query.fetchone()[0], 2157)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query, table_size_query = GroceryItem.get_all([], "alpha", 0, 16)
            items = list(query)
            self.assertEqual(len(items), 16)
            # TODO sqlite correction
            self.assertEqual(items[15].grocery_id, 182146)
            self.assertEqual(table_size_query.fetchone()[0], 2157)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query, table_size_query = GroceryItem.get_all([], "alpha", 2, 16)

            items = list(query)
            self.assertEqual(len(items), 16)
            # TODO sqlite correction
            self.assertEqual(items[15].grocery_id, 176079)

        with self.subTest(msg="No tags; alpha rev; Page=2; Pagesize=16"):
            query, table_size_query = GroceryItem.get_all([], "alpha_reverse",
                                                          2, 16)
            items = list(query)
            # TODO sqlite correction
            self.assertEqual(items[15].grocery_id, 407084)
            self.assertTrue(items[0].name >= items[1].name)

        with self.subTest(msg="Pescetarian, Peanut-free, MSG-free; alpha rev; "
                              "Page=0; Pagesize=16"):
            tag_set = set(("Pescetarian", "Peanut-free", "MSG-free"))
            query, table_size_query = GroceryItem.get_all(list(tag_set),
                                                          "alpha_reverse", 0, 16)
            last_item = list(query)[15]
            _last_item_query = GroceryItem.get(last_item.grocery_id)
            last_item_tags = set(t.tag_name for t in _last_item_query.tags)
            # TODO sqlite correction
            self.assertEqual(last_item.grocery_id, 219930)
            self.assertTrue(last_item_tags.issuperset(tag_set))
            self.assertEqual(table_size_query.fetchone()[0], 1831)

    def test_get_groceryitem(self):
        ing = GroceryItem.get(412409)
        self.assertEqual(ing.grocery_id, 412409)
        self.assertEqual(ing.name, "Yucatan Avocado Halves")
        self.assertEqual(ing.image_url, "https://spoonacular.com/productImages"
                                        "/412409-636x393.jpg")
        self.assertEqual(ing.upc, "767119103205")
        self.assertEqual(set(g.grocery_id for g in ing.similar_grocery_items),
                         set((207299, 181939, 191636, 192435)))
        self.assertEqual(set(t.tag_name for t in ing.tags),
                         set(("Gluten-free", "No preservatives", "Vegetarian",
                              "Grain-free", "Pescetarian", "Soy-free",
                              "MSG-free", "Nut-free", "Dairy-free", "Corn-free",
                              "Peanut-free", "Sugar-free", "Sulfite-free",
                              "Wheat-free", "Vegan", "No artificial ingredients",
                              "No artificial colors", "No additives",
                              "No artificial flavors", "Egg-free")))

    def test_get_all_tag(self):
        with self.subTest(msg="No min; Alpha; Page=0; Pagesize=1"):
            query, table_size = Tag.get_all(0, "alpha", 0, 1)
            tag_0 = next(iter(query))
            self.assertEqual(tag_0.tag_name, "American")
            self.assertEqual(table_size, 72)

        with self.subTest(msg="No min; Alpha; Page=0; Pagesize=16"):
            query, table_size = Tag.get_all(0, "alpha", 0, 16)
            tags = list(query)
            self.assertEqual(len(tags), 16)
            # TODO sqlite correction
            self.assertEqual(tags[15].tag_name, "European")
            self.assertEqual(table_size, 72)

        with self.subTest(msg="No min; Alpha; Page=2; Pagesize=16"):
            query = Tag.get_all(0, "alpha", 2, 16)[0]

            tags = list(query)
            self.assertEqual(len(tags), 16)
            # TODO sqlite correction
            self.assertEqual(tags[15].tag_name, "Organic")

        with self.subTest(msg="No min; alpha rev; Page=2; Pagesize=16"):
            query = Tag.get_all(0, "alpha_reverse", 2, 16)[0]
            tags = list(query)
            # TODO sqlite correction
            self.assertEqual(tags[15].tag_name, "Hormone-free")
            self.assertTrue(tags[0].tag_name >= tags[1].tag_name)

        with self.subTest(msg="min 30; alpha rev; Page=0; Pagesize=16"):
            query, table_size = Tag.get_all(30, "alpha_reverse", 0, 16)
            last_tag = list(query)[15]
            # TODO sqlite correction
            self.assertEqual(last_tag.tag_name, "Antipasto")
            self.assertEqual(table_size, 17)

    def test_get_tag(self):
        tag = Tag.get("Dessert")
        self.assertEqual(tag.tag_name, "Dessert")
        self.assertEqual(tag.description,
                         "A sweet dish usually served at the end of a meal.")
        self.assertEqual(tag.image_url, "Dessert.png")
        self.assertEqual(len(set(tag.ingredients)), 0)
        self.assertEqual(len(set(tag.grocery_items)), 0)

        recipe_set = set(r.recipe_id for r in tag.recipes)
        self.assertEqual(len(recipe_set), 80)
        self.assertEqual(recipe_set,
                         set((53235, 55423, 60909, 62998, 67162, 67282, 73294,
                              139944, 141807, 144066, 158655, 159245, 173136,
                              200432, 202648, 220435, 292277, 298055, 385501,
                              472420, 474497, 477341, 478320, 488980, 495427,
                              495478, 506482, 510562, 518993, 519894, 522532,
                              522946, 530398, 532997, 540557, 542484, 547768,
                              548324, 549698, 549981, 554362, 556672, 556749,
                              556891, 566617, 568570, 570378, 570953, 573568,
                              575640, 581235, 583788, 586254, 590142, 590387,
                              590545, 592010, 604931, 609554, 613127, 615561,
                              619185, 623812, 624132, 628541, 628699, 629026,
                              629041, 629825, 705048, 711303, 733472, 738124,
                              751116, 755750, 758662, 765471, 822427, 826828,
                              831524)))

def resp_to_dict(resp):
    return flask.json.loads(resp.data)

class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app.api.routes import API_BP
        cls.app = flask.Flask(__name__)
        cls.app.register_blueprint(API_BP)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.config["SQLALCHEMY_ECHO"] = False
        cls.database = models.db
        cls.database.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        cls.client = cls.app.test_client()

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
            query = resp_to_dict(RouteTests.client.get('/recipes?page_size=1'))
            self.assertEqual(query["data"][0]["id"], 557212)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/recipes?page_size=16'))
            recipes = query["data"]
            self.assertEqual(recipes[0]["id"], 557212)
            self.assertEqual(len(recipes), 16)
            self.assertEqual(recipes[15]["id"], 547264)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/recipes?page_size=16'
                                                       '&page=2'))
            recipes = query["data"]
            self.assertEqual(len(recipes), 16)
            # TODO: fix and replace sqlite so that we get the correct response
            # should be 101323, but sqlite is dumb
            self.assertEqual(recipes[15]["id"], 493614)

        with self.subTest(msg="No tags; Ready time rev; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/recipes?page_size=16'
                                                       '&page=2'
                                                       '&sort=ready_time_desc'))
            recipes = query["data"]
            # TODO: dumb sqlite should be 474497 but sqlite is dumb
            self.assertEqual(recipes[15]["id"], 539503)
            self.assertTrue(recipes[0]["ready_time"] >= recipes[1]["ready_time"])

        with self.subTest(msg="Vegan Beverage; Ready time rev; "
                              "Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/recipes?page_size=16'
                                                       '&page=0'
                                                       '&sort=ready_time_desc'
                                                       '&tags=Vegan,Beverage'))
            recipes = query["data"]
            tag_set = set(("Vegan", "Beverage"))
            last_recipe = recipes[15]
            _last_recipe_query = Recipe.get(last_recipe["id"])
            last_recipe_tags = set(t.tag_name for t in _last_recipe_query.tags)
            # TODO: dumb sqlite should be 493245 but sqlite is dumb
            self.assertEqual(last_recipe["id"], 578431)
            self.assertTrue(last_recipe_tags.issuperset(tag_set))

    def test_get_recipe(self):
        query = resp_to_dict(RouteTests.client.get('/recipes/9344'))
        self.assertEqual(query["id"], 9344)
        self.assertTrue(query["instructions"] != "" and
                        query["instructions"] is not None)
        self.assertTrue(query["servings"], 4)
        self.assertTrue(query["ready_time"], 45)
        self.assertTrue(query["source_url"], "http://www.bonappetit.com/recipes/"
                                             "2011/08/beet-carrot-and-apple-juic"
                                             "e-with-ginger")
        self.assertEqual(query["image"], "https://spoonacular.com/recipeImag"
                                         "es/beet_carrot_and_apple_juice_wit"
                                         "h_ginger-9344.jpg")
        # TODO: fix when migrate away from sqlite
        self.assertEqual(set(i["id"] for i in query["ingredient_list"]),
                         set((9003, 9152, 11080, 11124, 11216, 1029003)))
        # TODO: fix when migrate away from sqlite
        self.assertEqual(set(r["id"] for r in query["related_recipes"]),
                         set((9739, 233626, 472371, 488159, 500633, 620307)))
        self.assertEqual(set(t["name"] for t in query["tags"]),
                         set(("Beverage", "Vegan", "Gluten-free", "Whole30",
                              "Dairy-free", "Vegetarian")))


    def test_get_all_ingredient(self):
        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=1"):
            query = resp_to_dict(RouteTests.client.get('/ingredients?'
                                                       'page_size=1'))
            self.assertEqual(query["data"][0]["id"], 1102047)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/ingredients?'
                                                       'page_size=16'))
            ingredients = query["data"]
            self.assertEqual(len(ingredients), 16)
            self.assertEqual(ingredients[15]["id"], 9016)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/ingredients?'
                                                       'page_size=16&page=2'))
            ingredients = query["data"]
            self.assertEqual(len(ingredients), 16)
            # TODO sqlite correction
            self.assertEqual(ingredients[15]["id"], 1002030)

        with self.subTest(msg="No tags; alpha rev; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/ingredients?'
                                                       'page_size=16&page=2'
                                                       '&sort=alpha_reverse'))
            ingredients = query["data"]
            # TODO sqlite correction
            self.assertEqual(ingredients[15]["id"], 10020081)
            self.assertTrue(ingredients[0]["name"] >= ingredients[1]["name"])

        with self.subTest(msg="Dairy-free; alpha rev; "
                              "Page=0; Pagesize=16"):
            tag_set = set(("Dairy-free",))
            query = resp_to_dict(RouteTests.client.get('/ingredients?'
                                                       'page_size=16'
                                                       '&sort=alpha_reverse'
                                                       '&tags=Dairy-free'))
            last_ing = query["data"][15]
            _last_ing_query = Ingredient.get(last_ing["id"])
            last_ing_tags = set(t.tag_name for t in _last_ing_query.tags)
            # TODO sqlite correction
            self.assertEqual(last_ing["id"], 10611282)
            self.assertTrue(last_ing_tags.issuperset(tag_set))

    def test_get_ingredient(self):
        query = resp_to_dict(RouteTests.client.get('/ingredients/9070'))
        self.assertEqual(query["id"], 9070)
        self.assertEqual(query["name"], "cherries")
        self.assertEqual(query["image"],
                         "https://storage.googleapis.com/vennfridge/saved_ingre"
                         "dient_images%2F9070.jpg")
        self.assertEqual(query["aisle"], "Produce")
        self.assertEqual(set(ri["id"] for ri in query["related_recipes"]),
                         set((199872, 758662, 73294, 151512, 616762)))
        self.assertEqual(set(g["id"] for g in query["related_grocery_items"]),
                         set((56980, 209417, 177259, 201700, 173789)))
        self.assertEqual(set(t["name"] for t in query["tags"]),
                         set(("Dairy-free", "Vegetarian", "Vegan")))

    def test_get_all_groceryitem(self):
        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=1"):
            query = resp_to_dict(RouteTests.client.get('/grocery_items?'
                                                       'page_size=1'))
            self.assertEqual(query["data"][0]["id"], 95469)

        with self.subTest(msg="No tags; Alpha; Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/grocery_items?'
                                                       'page_size=16'))
            items = query["data"]
            self.assertEqual(len(items), 16)
            # TODO sqlite correction
            self.assertEqual(items[15]["id"], 182146)

        with self.subTest(msg="No tags; Alpha; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/grocery_items?'
                                                       'page_size=16&page=2'))
            items = query["data"]
            self.assertEqual(len(items), 16)
            # TODO sqlite correction
            self.assertEqual(items[15]["id"], 176079)

        with self.subTest(msg="No tags; alpha rev; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/grocery_items?'
                                                       'page_size=16&page=2'
                                                       '&sort=alpha_reverse'))
            items = query["data"]
            # TODO sqlite correction
            self.assertEqual(items[15]["id"], 407084)
            self.assertTrue(items[0]["name"] >= items[1]["name"])

        with self.subTest(msg="Pescetarian, Peanut-free, MSG-free; alpha rev; "
                              "Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/grocery_items?'
                                                       'page_size=16&page=0'
                                                       '&sort=alpha_reverse'
                                                       '&tags=Pescetarian,'
                                                       'Peanut-free,MSG-free'))
            tag_set = set(("Pescetarian", "Peanut-free", "MSG-free"))
            last_item = query["data"][15]
            _last_item_query = GroceryItem.get(last_item["id"])
            last_item_tags = set(t.tag_name for t in _last_item_query.tags)
            # TODO sqlite correction
            self.assertEqual(last_item["id"], 219930)
            self.assertTrue(last_item_tags.issuperset(tag_set))

    def test_get_groceryitem(self):
        query = resp_to_dict(RouteTests.client.get('/grocery_items/412409'))
        self.assertEqual(query["id"], 412409)
        self.assertEqual(query["name"], "Yucatan Avocado Halves")
        self.assertEqual(query["image"], "https://spoonacular.com/productImages"
                                        "/412409-636x393.jpg")
        self.assertEqual(query["upc"], "767119103205")
        self.assertEqual(set(g["id"] for g in query["related_grocery_items"]),
                         set((207299, 181939, 191636, 192435)))
        self.assertEqual(set(t["name"] for t in query["tags"]),
                         set(("Gluten-free", "No preservatives", "Vegetarian",
                              "Grain-free", "Pescetarian", "Soy-free",
                              "MSG-free", "Nut-free", "Dairy-free", "Corn-free",
                              "Peanut-free", "Sugar-free", "Sulfite-free",
                              "Wheat-free", "Vegan", "No artificial ingredients",
                              "No artificial colors", "No additives",
                              "No artificial flavors", "Egg-free")))

    def test_get_all_tag(self):
        with self.subTest(msg="No min; Alpha; Page=0; Pagesize=1"):
            query = resp_to_dict(RouteTests.client.get('/tags?page_size=1'))
            self.assertEqual(query["data"][0]["name"], "American")

        with self.subTest(msg="No min; Alpha; Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/tags?page_size=16'))
            tags = query["data"]
            self.assertEqual(len(tags), 16)
            # TODO sqlite correction
            self.assertEqual(tags[15]["name"], "European")

        with self.subTest(msg="No min; Alpha; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/tags?page_size=16'
                                                       '&page=2'))
            tags = query["data"]
            self.assertEqual(len(tags), 16)
            # TODO sqlite correction
            self.assertEqual(tags[15]["name"], "Organic")

        with self.subTest(msg="No min; alpha rev; Page=2; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/tags?page_size=16'
                                                       '&page=2'
                                                       '&sort=alpha_reverse'))
            tags = query["data"]
            # TODO sqlite correction
            self.assertEqual(tags[15]["name"], "Hormone-free")
            self.assertTrue(tags[0]["name"] >= tags[1]["name"])

        with self.subTest(msg="min 30; alpha rev; Page=0; Pagesize=16"):
            query = resp_to_dict(RouteTests.client.get('/tags?page_size=16'
                                                       '&min=30'
                                                       '&sort=alpha_reverse'))
            last_tag = query["data"][15]
            # TODO sqlite correction
            self.assertEqual(last_tag["name"], "Antipasto")
    """

    def test_get_tag(self):
        tag = Tag.get("Dessert")
        self.assertEqual(tag.tag_name, "Dessert")
        self.assertEqual(tag.description,
                         "A sweet dish usually served at the end of a meal.")
        self.assertEqual(tag.image_url, "Dessert.png")
        self.assertEqual(len(set(tag.ingredients)), 0)
        self.assertEqual(len(set(tag.grocery_items)), 0)

        recipe_set = set(r.recipe_id for r in tag.recipes)
        self.assertEqual(len(recipe_set), 80)
        self.assertEqual(recipe_set,
                         set((53235, 55423, 60909, 62998, 67162, 67282, 73294,
                              139944, 141807, 144066, 158655, 159245, 173136,
                              200432, 202648, 220435, 292277, 298055, 385501,
                              472420, 474497, 477341, 478320, 488980, 495427,
                              495478, 506482, 510562, 518993, 519894, 522532,
                              522946, 530398, 532997, 540557, 542484, 547768,
                              548324, 549698, 549981, 554362, 556672, 556749,
                              556891, 566617, 568570, 570378, 570953, 573568,
                              575640, 581235, 583788, 586254, 590142, 590387,
                              590545, 592010, 604931, 609554, 613127, 615561,
                              619185, 623812, 624132, 628541, 628699, 629026,
                              629041, 629825, 705048, 711303, 733472, 738124,
                              751116, 755750, 758662, 765471, 822427, 826828,
                              831524)))
    """


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
