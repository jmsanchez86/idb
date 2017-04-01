#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=pointless-string-statement

from unittest import main, TestCase

import sqlalchemy
import flask_sqlalchemy
from flask import Flask

from app.api.models import Ingredient, Tag, Recipe, GroceryItem, db
from app.api.test.test_data import mock_data


class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print("sqlalchemy version: %s" % sqlalchemy.__version__)
        print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

        cls.app = Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.config["SQLALCHEMY_ECHO"] = False
        db.init_app(cls.app)
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

        mock_data(db)

        query = db.session.query(Ingredient).filter_by(name="licorice")
        cls.licorice = query.first()

        query = db.session.query(Recipe).filter_by(name="sandwich")
        cls.sandwich = query.first()

        query = db.session.query(GroceryItem).filter_by(name="Jake's bread")
        cls.jakes_bread = query.first()

        query = db.session.query(Tag).filter_by(tag_name="natural")
        cls.tag = query.first()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_ingredient(self):
        # Ingredient by name.
        self.assertIsNotNone(self.licorice)
        self.assertEqual(self.licorice.ingredient_id, 1)
        self.assertEqual(repr(self.licorice), "<Ingredient 1 licorice>")

    def test_ingredient_nutrition(self):
        # Nutrition data of an ingredient.
        nutrients = self.licorice.nutrients
        nutrient_data = set((n.category, n.unit, n.quantity)
                            for n in nutrients)
        self.assertEqual(nutrient_data, {("sugar", "kilograms", 100),
                                         ("calories", "calories", 9001),
                                         ("iron", "grams", 123)})
        self.assertEqual({repr(ingn) for ingn in self.licorice.nutrients},
                         {"<IngredientNutrient 1 sugar>",
                          "<IngredientNutrient 1 calories>",
                          "<IngredientNutrient 1 iron>"})

    def test_recipe(self):
        # Recipe by name.
        self.assertIsNotNone(self.sandwich)
        self.assertEqual(self.sandwich.recipe_id, 2)
        self.assertEqual(repr(self.sandwich), "<Recipe 2 sandwich>")

    def test_recipe_nutrition(self):
        # Nutrition data for recipe.
        nutrients = self.sandwich.nutrients
        nutrient_data = set((n.category, n.unit, n.quantity)
                            for n in nutrients)
        self.assertEqual(nutrient_data, {("sugar", "meters", 82),
                                         ("calories", "calories", 23),
                                         ("iron", "micrograms", 166)})
        self.assertEqual({repr(rn) for rn in self.sandwich.nutrients},
                         {"<RecipeNutrient 2 sugar>",
                          "<RecipeNutrient 2 calories>",
                          "<RecipeNutrient 2 iron>"})

    def test_recipe_ingredients(self):
        # Ingredients of a recipe.
        ingredients = self.sandwich.ingredients
        ingredient_data = set((i.ingredient_id, i.unit, i.quantity)
                              for i in ingredients)
        self.assertEqual(ingredient_data, {
            (2, "grams", 50), (3, "grams", 100)})
        self.assertEqual({repr(ri) for ri in self.sandwich.ingredients},
                         {"<RecipeIngredient 2 2>", "<RecipeIngredient 2 3>"})

    def test_grocery_item(self):
        # Grocery item by name.
        self.assertIsNotNone(self.jakes_bread)
        self.assertEqual(self.jakes_bread.grocery_id, 2)
        self.assertEqual(repr(self.jakes_bread),
                         "<Grocery item 2 Jake's bread>")

    def test_grocery_item_ingredients(self):
        # Ingredients of a grocery item.
        ingredients = self.jakes_bread.ingredients
        ingredient_data = set((i.ingredient_id, i.unit, i.quantity)
                              for i in ingredients)
        self.assertEqual(ingredient_data, {(3, "slices", 12)})
        self.assertEqual({repr(gii) for gii in self.jakes_bread.ingredients},
                         {"<GroceryItemIngredient 2 3>"})

    def test_tag(self):
        # Tag by name
        self.assertEqual(self.tag.image_url, "industrial.jpg")
        self.assertEqual(repr(self.tag), "<Tag natural>")

    def test_tag_ingredients(self):
        # Tag ingredients
        ingredients = self.tag.ingredients
        ingredient_data = set(i.ingredient_id for i in ingredients)
        self.assertEqual(ingredient_data, {2, 3})
        self.assertEqual({repr(ti) for ti in self.tag.tag_ingredient_assocs},
                         {"<TagIngredient natural 2>",
                          "<TagIngredient natural 3>"})

    def test_tag_recipes(self):
        # Tag recipes
        recipes = self.tag.recipes
        recipe_data = set(r.recipe_id for r in recipes)
        self.assertEqual(recipe_data, {2})
        self.assertEqual({repr(tr) for tr in self.tag.tag_recipe_assocs},
                         {"<TagRecipe natural 2>"})

    def test_tag_grocery_items(self):
        # Tag grocery items
        items = self.tag.grocery_items
        item_data = set(i.grocery_id for i in items)
        self.assertEqual(item_data, {1, 2})
        self.assertEqual({repr(tgi) for tgi in self.tag.tag_grocery_item_assocs},
                         {"<TagGroceryItem natural 1>",
                          "<TagGroceryItem natural 2>"})


if __name__ == "__main__":  # pragma: no cover
    main()
