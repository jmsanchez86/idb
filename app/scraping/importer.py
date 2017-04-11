
# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=pointless-string-statement
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals

"""
Imports json data into the database.
"""

import json
import re
from pathlib import Path
from app.api import models
from app.scraping.tag_translations import tags


def strip_html(html):
    """
    Remove all html tags from a string.
    """
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


class Importer:
    """
    Imports json data from a directory into a databse.
    """

    recipe_tag_flags = ["cheap", "dairyFree", "glutenFree", "ketogenic",
                        "lowFodmap", "sustainable", "vegan", "vegeterian",
                        "veryHealthy", "veryPopular", "whole30"]

    # Recipe tags that make sense to propogate down to ingredients.
    propogate_flags = ["lowFodmap", "ketogenic",
                       "veryHealthy", "vegan", "whole30", "dairyFree"]

    def __init__(self, data_dir: str, database) -> None:
        """
        data_dir - a directory containing the necessary json files.
        database       - a SQLAlchemy database instance.
        """

        self.database = database
        self.data_dir = Path(data_dir)

        self.find_similar_recipes = self.read_json("find_similar_recipes.json")
        self.get_ingredient_substitutes = \
            self.read_json("get_ingredient_substitutes.json")
        self.get_product_information = \
            self.read_json("get_product_information.json")
        self.get_product_map = self.read_json("get_product_map.json")
        self.recipes = self.read_json("recipes.json")
        self.summarize_recipe = self.read_json("summarize_recipe.json")

        self.recipes = dict()  # type: dict
        self.ingredients = dict()  # type: dict
        self.grocery_items = dict()  # type: dict
        self.tags = dict()  # type: dict
        self.ingredient_substitutes = list()  # type: list
        self.recipe_ingredients = list()  # type: list
        self.tag_recipes = dict()  # type: dict
        self.tag_ingredients = dict()  # type: dict
        self.tag_grocery_items = dict()  # type: dict
        self.similar_recipes = list()  # type: list
        self.similar_grocery_items = list()  # type: list

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
        iters.append(self.tag_recipes.values())
        iters.append(self.tag_ingredients.values())

        iters.append(iter(self.ingredient_substitutes))
        iters.append(iter(self.recipe_ingredients))
        iters.append(iter(self.similar_recipes))
        iters.append(iter(self.similar_grocery_items))

        for itr in iters:
            for row in itr:
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

        # We need to have inserted all the recipes before going through similar
        # recipes because there are many similar recipes that we do not have in
        # our database and we don't want to include that relationship if it does
        # not exist.
        for str_id in recipes:
            int_id = int(str_id)
            similar_recipes = self.find_similar_recipes.get(str_id, [])
            for similar in similar_recipes:
                similar_id = similar["id"]
                if similar_id not in self.recipes:
                    continue
                self.similar_recipes.append(
                    models.SimilarRecipe(int_id, similar["id"]))

        self.commit()

    def recipe_tag(self, recipe_id, spoon_name):
        tag_info = tags[spoon_name]
        tag_name = tag_info["name"]
        image_url = tag_info["image_url"]
        description = tag_info["description"]

        if tag_name not in self.tags:
            self.tags[tag_name] = models.Tag(tag_name, image_url, description)

        key = (tag_name, recipe_id)
        if key not in self.tag_recipes:
            self.tag_recipes[key] = models.TagRecipe(tag_name, recipe_id)

    def recipe(self, recipe_id, recipe_data):
        name = recipe_data.get("title", "")
        image_url = recipe_data.get("image", "")
        instructions = strip_html(recipe_data.get("instructions", "") or "")
        ready_time = recipe_data.get("readyInMinutes", 0)
        servings = recipe_data.get("servings", 0)

        summary_data = self.summarize_recipe.get(str(recipe_id), None)
        summary = (summary_data and strip_html(summary_data.get("summary", ""))
                   or "")

        recipe = models.Recipe(recipe_id, name, image_url, instructions,
                               summary, ready_time, servings,
                               recipe_data["sourceUrl"])
        self.recipes[recipe_id] = recipe

        ingredient_flags = []
        for flag in self.recipe_tag_flags:
            if recipe_data.get(flag, False):
                self.recipe_tag(recipe_id, flag)

                if flag in self.propogate_flags:
                    ingredient_flags.append(flag)

        for cuisine in recipe_data.get("cuisines", {}):
            self.recipe_tag(recipe_id, cuisine)

        for dish_type in recipe_data.get("dishTypes", {}):
            self.recipe_tag(recipe_id, dish_type)

        for ingredient_data in recipe_data.get("extendedIngredients", list()):
            self.ingredient(recipe_id, ingredient_data, ingredient_flags)

    def ingredient_tag(self, ingredient_id, spoon_name):
        tag_info = tags[spoon_name]
        tag_name = tag_info["name"]
        image_url = tag_info["image_url"]
        description = tag_info["description"]

        # TODO: Just thinking about it, we don't need to add tags here since
        # we have all the tags in tag_translations.py. This exact code is
        # in recipe_tag and grocery_tag.
        if tag_name not in self.tags:
            self.tags[tag_name] = models.Tag(tag_name, image_url, description)

        key = (tag_name, ingredient_id)
        if key not in self.tag_ingredients:
            self.tag_ingredients[key] = models.TagIngredient(
                tag_name, ingredient_id)

    def ingredient(self, recipe_id, ingredient_data, flags):
        ingredient_id = ingredient_data.get("id", 0)
        if ingredient_id <= 0:
            return

        for flag in flags:
            self.ingredient_tag(ingredient_id, flag)

        if ingredient_id not in self.ingredients:

            name = ingredient_data.get("name", None)
            assert name != None

            aisle = ingredient_data.get("aisle", None)
            assert aisle != None

            self.ingredients[ingredient_id] = (
                models.Ingredient(ingredient_id, name, "", aisle))

            for subst in self.get_ingredient_substitutes\
                             .get(str(ingredient_id), {})\
                             .get("substitutes", []):
                self.ingredient_substitutes.append(
                    models.IngredientSubstitute(ingredient_id, subst))

            products = self.get_product_map.get(str(ingredient_id), None)
            if products:
                products = products[0].get("products", [])[:5]
                for product_data in products:
                    self.product(ingredient_id, product_data, products)

        verbal_quantity = ingredient_data.get("originalString", None)
        assert verbal_quantity != None

        self.recipe_ingredients.append(models.RecipeIngredient(
            recipe_id, ingredient_id, verbal_quantity))

    def product_tag(self, ingredient_id, product_id, spoon_name):
        tag_info = tags[spoon_name]
        tag_name = tag_info["name"]
        image_url = tag_info["image_url"]
        description = tag_info["description"]

        if tag_name not in self.tags:
            self.tags[tag_name] = models.Tag(tag_name, image_url, description)

        key = (ingredient_id, product_id, tag_name)
        if key not in self.tag_grocery_items:
            self.tag_grocery_items[key] = models.TagGroceryItem(
                tag_name, ingredient_id, product_id)
        else:
            print("Ingredient {} product {} has multiple of tag {}.".format(
                ingredient_id, product_id, tag_name))

    def product(self, ingredient_id, product_data, other_products):
        product_id = product_data.get("id", None)
        assert product_id != None

        for other in other_products:
            other_id = other.get("id", None)
            assert other_id != None

            if other_id == product_id:
                continue

            self.similar_grocery_items.append(
                models.SimilarGroceryItem(ingredient_id, product_id, other_id))

        product_info = self.get_product_information[str(product_id)]

        name = product_data["title"]
        upc = product_data["upc"]
        image_url = product_info["images"][1]

        key = (ingredient_id, product_id)
        if key not in self.grocery_items:
            self.grocery_items[key] = models.GroceryItem(
                product_id, ingredient_id, name, image_url, upc)

            for badge in product_info.get("badges", []):
                self.product_tag(ingredient_id, product_id, badge)
        else:
            print("Ingredient {} contains multiple grocery product {}.".format(
                ingredient_id, product_id))
