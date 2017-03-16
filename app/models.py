# Currently this file is meant to run separately.
# The only two python modules necessary to run this are:
#     flask
#     flask_sqlalchemy
#
# Both of these can be installed with pip.
# pip install flask
# pip install flask_sqlalchemy
#
# For enumerations there's a funtion called enum.auto() that
# will generate a distinct value for each item but thinking about
# the underlying database I think it matters that we know what the
# values are so they don't change under our noses.

import enum

from flask import Flask
import sqlalchemy
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class NutrientCategory(enum.Enum):
    calories = 1
    calories_from_fat = 2
    fat = 3
    saturated_fat = 4
    trans_fat = 5
    cholesterol = 6
    sodium = 7
    carbohydrates = 8
    dietary_fiber = 9
    sugars = 10
    protein = 11
    vitamin_a = 12
    vitamin_c = 13
    calcium = 14
    iron = 15

class IngredientNutrient(db.Model):
    __tablename__ = "ingredient_nutrient"

    ingredient_id     = db.Column(db.Integer, primary_key=True)
    category          = db.Column(db.Enum(NutrientCategory), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    def __init__(self, ingredient_id, category, quantity_unit, quantity):
        self.ingredient_id = ingredient_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<Ingredient Nutrient %d %s>" % (self.ingredient_id, self.category)

class RecipeNutrient(db.Model):
    __tablename__ = "recipe_nutrient"

    recipe_id         = db.Column(db.Integer, primary_key=True)
    category          = db.Column(db.Enum(NutrientCategory), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    def __init__(self, ingredient_id, category, quantity):
        self.recipe_id = recipe_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<Recipe Nutrient %d %s>" % (self.recipe_id, self.category)


class Ingredient(db.Model):
    __tablename__ = "ingredient"

    ingredient_id  = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    # Does name need to be unique? Is there a possibility for name collision?
    name           = db.Column(db.String(20), unique=True)
    image_url      = db.Column(db.String(100))

    def __init__(self, ingredient_id, spoonacular_id, name, image_url):
        self.ingredient_id = ingredient_id
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image_url = image_url

    def __repr__(self):
        return "<Ingredient %d %s>" % (self.ingredient_id, self.name)

class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id       = db.Column(db.Integer, primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    quantity_unit   = db.Column(db.String(20))
    quantity        = db.Column(db.Integer)
    quantity_verbal = db.Column(db.String(100))

    def __init__(self, recipe_id, ingredient_id, quantity, quantity_unit,
                 quantity_verbal):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<RecipeIngredient %d %d>" % (self.recipe_id, self.ingredient_id)

class Recipe(db.Model):
    __tablename__ = "recipe"

    recipe_id      = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    name           = db.Column(db.String(20), unique=True)
    image_url      = db.Column(db.String(100))
    instructions   = db.Column(db.String(1000), primary_key=True)

    def __init__(self, recipe_id, spoonacular_id, name, image_url, instructions):
        self.recipe_id = recipe_id
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image_url = image_url
        self.instructions = instructions

    @property
    def ingredients(self):
        # Return a list of RecipeIngredients.
        pass

    @property
    def nutrition(self):
        # Fetch nutrition data.
        pass

    def __repr__(self):
        return "<Recipe %d %s>" % (self.recipe_id, self.name)

class ItemType(enum.Enum):
    """
    Enumerate items that tags can be associated with. This is necessary to
    distinguish the item_id field since it will not be unique
    on its own (i.e. some recipe_id and ingredient_id share the same value.)
    """
    recipe = 1
    ingredient = 2
    grocery_item = 3

class TagItem(db.Model):
    __tablename__ = "tag_item"

    tag_name  = db.Column(db.String(20), primary_key=True)
    item_type = db.Column(db.Enum(ItemType), primary_key=True)
    item_id   = db.Column(db.String(20))

    def __init__(self, tag_name, item_type, item_id):
        self.tag_name = tag_name
        self.item_type = item_type
        self.item_id = item_id

    def __repr__(self):
        return "<Tag item %s %s %d>" % (self.tag_name, self.item_type, self.item_id)

class Tag(db.Model):
    __tablename__ = "tag"

    tag_name    = db.Column(db.String(20), primary_key=True)
    image_url   = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, tag_name, image_url, description):
        self.tag_name = tag_name
        self.image_url = image_url
        self.description = description

    def __repr__(self):
        return "<Tag %s>" % (self.tag_name)

class GroceryItem(db.Model):
    __tablename__ = "grocery_item"

    grocery_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(20))
    image_url  = db.Column(db.String(100))
    upc        = db.Column(db.String(20))

    def __init__(self, grocery_id, name, image_url, upc):
        self.grocery_id = grocery_id
        self.name = name
        self.image_url = image_url
        self.upc = upc

    def __repr__(self):
        return "<Grocery item %d %s>" % (self.grocery_id, self.name)

if __name__ == "__main__":
    db.create_all()

    ingredient = Ingredient(1, 1337, "licorice", "licorice.jpg")
    print(ingredient)

    print("sqlalchemy version: %s" % sqlalchemy.__version__)
    print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

