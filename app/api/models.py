"""
Database models described with SQLAlchemy.
"""

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=bad-whitespace
# pylint: disable=too-many-arguments

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()  # type: SQLAlchemy

class Recipe(db.Model):
    """
    Table of recipes.
    """

    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image_url = db.Column(db.String(100))
    instructions = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    ready_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)

    def __init__(self, recipe_id, name, image_url, instructions, description,
                 ready_time, servings):
        self.recipe_id = recipe_id
        self.name = name
        self.image_url = image_url
        self.instructions = instructions
        self.description = description
        self.ready_time = ready_time
        self.servings = servings

    def __repr__(self):
        return "<Recipe %d %s>" % (self.recipe_id, self.name)

class Ingredient(db.Model):
    """
    Table of ingredients.
    """

    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image_url = db.Column(db.String(100))
    aisle = db.Column(db.String(20))

    def __init__(self, ingredient_id, name, image_url, aisle):
        self.ingredient_id = ingredient_id
        self.name = name
        self.image_url = image_url
        self.aisle = aisle

    def __repr__(self):
        return "<Ingredient %d %s>" % (self.ingredient_id, self.name)


class IngredientSubstitutes(db.Model):
    """
    Table of ingredient substitutes.
    """

    __tablename__ = "ingredient_substitutes"

    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id"),
                              primary_key=True)
    substitutions = db.Column(db.String(100))

    ingredient = db.relationship("Ingredient", back_populates="substitutes")

    def __init__(self, ingredient_id, substitutes):
        self.ingredient_id = ingredient_id
        self.substitutes = substitutes

    def __repr__(self):
        return "<Ingredient Substitute %d %s>" % (self.ingredient_id,
                                                  self.substitute)

Ingredient.substitutes = db.relationship("IngredientSubstitutes",
                                         back_populates="ingredient")


class GroceryItem(db.Model):
    """
    Table of Grocery Items.
    """

    __tablename__ = "grocery_item"

    grocery_id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image_url = db.Column(db.String(100))
    upc = db.Column(db.String(20))

    def __init__(self, grocery_id, ingredient_id, name, image_url, upc):
        self.grocery_id = grocery_id
        self.name = name
        self.image_url = image_url
        self.upc = upc

    def __repr__(self):
        return "<Grocery item %d %s>" % (self.grocery_id, self.name)


class Tag(db.Model):
    """
    Table of tags.
    """

    __tablename__ = "tag"

    tag_name = db.Column(db.String(20), primary_key=True)
    image_url = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, tag_name, image_url, description):
        self.tag_name = tag_name
        self.image_url = image_url
        self.description = description

    def __repr__(self):
        return "<Tag %s>" % (self.tag_name)

class RecipeIngredient(db.Model):
    """
    Ingredients and quantities contained in a recipe.
    """

    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),
                          primary_key=True)
    ingredient_id = db.Column(db.Integer, primary_key=True)
    verbal_quantity = db.Column(db.String(100))

    recipe = db.relationship("Recipe", back_populates="ingredients")

    def __init__(self, recipe_id, ingredient_id, verbal_quantity):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.verbal_quantity = verbal_quantity

    def __repr__(self):
        return "<RecipeIngredient %d %d>" % (
            self.recipe_id,
            self.ingredient_id)


Recipe.ingredients = db.relationship("RecipeIngredient",
                                     back_populates="recipe")

class TagIngredient(db.Model):
    """
    Association table for tags to ingredients.
    """

    __tablename__ = "tag_ingredient"

    tag_name = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),
                         primary_key=True)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id"),
                              primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_ingredient_assocs")
    ingredient = db.relationship("Ingredient",
                                 back_populates="tag_ingredient_assocs")

    def __init__(self, tag_name, ingredient_id):
        self.tag_name = tag_name
        self.ingredient_id = ingredient_id

    def __repr__(self):
        return "<TagIngredient %s %d>" % (self.tag_name, self.ingredient_id)


Ingredient.tag_ingredient_assocs = db.relationship("TagIngredient",
                                                   back_populates="ingredient")
Tag.tag_ingredient_assocs = db.relationship("TagIngredient",
                                            back_populates="tag")
Ingredient.tags = association_proxy("tag_ingredient_assocs", "tag")
Tag.ingredients = association_proxy("tag_ingredient_assocs", "ingredient")


class TagRecipe(db.Model):
    """
    Association table for tags to recipes.
    """

    __tablename__ = "tag_recipe"

    tag_name = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),
                         primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),
                          primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_recipe_assocs")
    recipe = db.relationship("Recipe", back_populates="tag_recipe_assocs")

    def __init__(self, tag_name, recipe_id):
        self.tag_name = tag_name
        self.recipe_id = recipe_id

    def __repr__(self):
        return "<TagRecipe %s %d>" % (self.tag_name, self.recipe_id)


Recipe.tag_recipe_assocs = db.relationship(
    "TagRecipe", back_populates="recipe")
Tag.tag_recipe_assocs = db.relationship("TagRecipe", back_populates="tag")
Recipe.tags = association_proxy("tag_recipe_assocs", "tag")
Tag.recipes = association_proxy("tag_recipe_assocs", "recipe")


class TagGroceryItem(db.Model):
    """
    Association table for tags to grocery items.
    """

    __tablename__ = "tag_grocery_item"

    tag_name = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),
                         primary_key=True)
    grocery_id = db.Column(db.Integer,
                           db.ForeignKey("grocery_item.grocery_id"),
                           primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_grocery_item_assocs")
    grocery_item = db.relationship("GroceryItem",
                                   back_populates="tag_grocery_item_assocs")

    def __init__(self, tag_name, grocery_id):
        self.tag_name = tag_name
        self.grocery_id = grocery_id

    def __repr__(self):
        return "<TagGroceryItem %s %d>" % (self.tag_name, self.grocery_id)


GroceryItem.tag_grocery_item_assocs = (
    db.relationship("TagGroceryItem", back_populates="grocery_item"))
Tag.tag_grocery_item_assocs = db.relationship("TagGroceryItem",
                                              back_populates="tag")
GroceryItem.tags = association_proxy("tag_grocery_item_assocs", "tag")
Tag.grocery_items = association_proxy(
    "tag_grocery_item_assocs", "grocery_item")


# Pylint Report
#
# ======
#
# 166 statements analysed.
#
#
#
# Statistics by type
#
# ------------------
#
#
# +---------+-------+-----------+-----------+------------+---------+
# |type     |number |old number |difference |%documented |%badname |
# +=========+=======+===========+===========+============+=========+
# |module   |1      |1          |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |class    |11     |11         |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |method   |22     |22         |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |function |0      |0          |=          |0           |0        |
# +---------+-------+-----------+-----------+------------+---------+
#
#
#
#
#
#
# External dependencies
#
# ---------------------
#
# ::
#
#
#     flask_sqlalchemy (app.models)
#
#     sqlalchemy
#
#       \-ext
#
#         \-associationproxy (app.models)
#
#
#
#
#
#
#
# Raw metrics
#
# -----------
#
#
# +----------+-------+------+---------+-----------+
# |type      |number |%     |previous |difference |
# +==========+=======+======+=========+===========+
# |code      |196    |61.83 |196      |=          |
# +----------+-------+------+---------+-----------+
# |docstring |36     |11.36 |36       |=          |
# +----------+-------+------+---------+-----------+
# |comment   |5      |1.58  |5        |=          |
# +----------+-------+------+---------+-----------+
# |empty     |80     |25.24 |80       |=          |
# +----------+-------+------+---------+-----------+
#
#
#
#
#
#
# Duplication
#
# -----------
#
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
#
#
#
# Messages by category
#
# --------------------
#
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
#
#
#
# Global evaluation
#
# -----------------
#
# Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
