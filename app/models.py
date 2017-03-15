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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    ingredient_id     = db.Column(db.Integer, primary_key=True)
    category          = db.Column(db.Enum(NutrientCategory), primary_key=True)
    unit              = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    def __init__(self, ingredient_id, category, quantity):
        self.ingredient_id = ingredient_id
        self.category = category
        self.quantity = quantity

    def __repr__(self):
        return "<Ingredient Nutrient %d %s>" % (self.ingredient_id, self.category)

class RecipeNutrient(db.Model):
    recipe_id         = db.Column(db.Integer, primary_key=True)
    category          = db.Column(db.Enum(NutrientCategory), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    def __init__(self, ingredient_id, category, quantity):
        self.recipe_id = recipe_id
        self.category = category
        self.quantity = quantity

    def __repr__(self):
        return "<Recipe Nutrient %d %s>" % (self.recipe_id, self.category)


class Ingredient(db.Model):
    ingredient_id  = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    # Does name need to be unique? Is there a possibility for name collision?
    name           = db.Column(db.String(20), unique=True)
    image_url      = db.Column(db.String(100))

    def __init__(self, spoonacular_id, name, image_url):
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image_url = image_url

    def __repr__(self):
        return "<Ingredient %d %s>" % (self.ingredient_id, self.name)

class RecipeIngredient(db.Model):
    recipe_id       = db.Column(db.Integer, primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    quantity_units  = db.Column(db.String(20))
    quantity        = db.Column(db.Integer)
    quantity_verbal = db.Column(db.String(100))

    def __init__(self, recipe_id, ingredient_id, quantity, quantity_units,
                 quantity_verbal):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.quantity_units = quantity_units
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<RecipeIngredient %d %d>" % (self.recipe_id, self.ingredient_id)

class Recipe(db.Model):
    recipe_id      = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    name           = db.Column(db.String(20), unique=True)
    image_url      = db.Column(db.String(100), unique=True)
    instructions   = db.Column(db.String(1000), primary_key=True)

    def __init__(self, spoonacular_id, name, image_url, instructions):
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
        # Compute and return aggreate nutrition based on ingredients.
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
    tag_name  = db.Column(db.String(20), primary_key=True)
    item_type = db.Column(db.Enum(ItemType), primary_key=True)
    item_id   = db.Column(db.String(20))

    def __repr__(self):
        return "<Tag Item %s %s %d>" % (self.tag_name, self.item_type, self.item_id)

class Tag(db.Model):
    tag_name    = db.Column(db.String(20), primary_key=True)
    image_url   = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __repr__(self):
        return "<Tag %s>" % (self.tag_name)

class GroceryItem(db.Model):
    grocery_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(20))
    image_url  = db.Column(db.String(100))
    upc        = db.Column(db.String(20))

    def __repr__(self):
        return "<Grocery Item %d %s>" % (self.grocery_id, self.name)



