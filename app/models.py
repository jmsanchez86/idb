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





class IngredientNutrient(db.Model):
    __tablename__ = "ingredient_nutrient"

    ingredient_id     = db.Column(db.Integer, db.ForeignKey("ingredient.ingredient_id"), primary_key=True)
    category          = db.Column(db.String(10), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    ingredient = db.relationship("Ingredient", back_populates="nutrients")

    def __init__(self, ingredient_id, category, quantity_unit, quantity):
        self.ingredient_id = ingredient_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<Ingredient Nutrient %d %s>" % (self.ingredient_id, self.category)

Ingredient.nutrients = db.relationship("IngredientNutrient", back_populates="ingredient")

class RecipeNutrient(db.Model):
    __tablename__ = "recipe_nutrient"

    recipe_id         = db.Column(db.Integer, primary_key=True)
    category          = db.Column(db.String(10), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Integer)

    def __init__(self, ingredient_id, category, quantity):
        self.recipe_id = recipe_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<Recipe Nutrient %d %s>" % (self.recipe_id, self.category)


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




if __name__ == "__main__":

    print("sqlalchemy version: %s" % sqlalchemy.__version__)
    print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

    db.create_all()

    licorice = Ingredient(1, 1337, "licorice", "licorice.jpg")
    db.session.add(licorice)

    query = db.session.query(Ingredient).filter_by(name="licorice")
    result = query.first()
    assert(result is licorice)
    assert(result == licorice)

    surgar = IngredientNutrient(1, "surgar", "kilograms", 100)
    db.session.add(surgar)
    calories = IngredientNutrient(1, "calories", "calories", 9001)
    db.session.add(calories)
    iron = IngredientNutrient(1, "iron", "grams", 123)
    db.session.add(iron)

    assert(set(licorice.nutrients) == {surgar, calories, iron})

    print("sqlalchemy version: %s" % sqlalchemy.__version__)
    print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

