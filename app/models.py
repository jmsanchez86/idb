# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=bad-whitespace
# pylint: disable=too-many-arguments

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy() # type: SQLAlchemy

class Ingredient(db.Model):
    __tablename__ = "ingredient"

    ingredient_id  = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
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

    def __init__(self, recipe_id, spoonacular_id, name, image_url,
                 instructions):
        self.recipe_id = recipe_id
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image_url = image_url
        self.instructions = instructions

    def __repr__(self):
        return "<Recipe %d %s>" % (self.recipe_id, self.name)

class GroceryItem(db.Model):
    __tablename__ = "grocery_item"

    grocery_id     = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    name           = db.Column(db.String(20))
    image_url      = db.Column(db.String(100))
    upc            = db.Column(db.String(20))

    def __init__(self, grocery_id, spoonacular_id, name, image_url, upc):
        self.grocery_id = grocery_id
        self.spoonacular_id = spoonacular_id
        self.name = name
        self.image_url = image_url
        self.upc = upc

    def __repr__(self):
        return "<Grocery item %d %s>" % (self.grocery_id, self.name)

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





class IngredientNutrient(db.Model):
    __tablename__ = "ingredient_nutrient"

    ingredient_id     = db.Column(db.Integer,\
                                  db.ForeignKey("ingredient.ingredient_id"),\
                                  primary_key=True)
    category          = db.Column(db.String(10), primary_key=True)
    unit              = db.Column(db.String(10))
    quantity          = db.Column(db.Float)

    ingredient = db.relationship("Ingredient", back_populates="nutrients")

    def __init__(self, ingredient_id, category, unit, quantity):
        self.ingredient_id = ingredient_id
        self.category = category
        self.unit = unit
        self.quantity = quantity

    def __repr__(self):
        return "<IngredientNutrient %d %s>" % \
                (self.ingredient_id, self.category)

Ingredient.nutrients = db.relationship("IngredientNutrient",\
                                        back_populates="ingredient")

class RecipeNutrient(db.Model):
    __tablename__ = "recipe_nutrient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), \
                          primary_key=True)
    category  = db.Column(db.String(10), primary_key=True)
    unit      = db.Column(db.String(10))
    quantity  = db.Column(db.Float)

    recipe = db.relationship("Recipe", back_populates="nutrients")

    def __init__(self, recipe_id, category, unit, quantity):
        self.recipe_id = recipe_id
        self.category = category
        self.unit = unit
        self.quantity = quantity

    def __repr__(self):
        return "<RecipeNutrient %d %s>" % (self.recipe_id, self.category)

Recipe.nutrients = db.relationship("RecipeNutrient", \
                                    back_populates="recipe")


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id       = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),\
                                primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    unit            = db.Column(db.String(20))
    quantity        = db.Column(db.Float)
    quantity_verbal = db.Column(db.String(100))

    recipe = db.relationship("Recipe", back_populates="ingredients")

    def __init__(self, recipe_id, ingredient_id, unit, quantity,
                 quantity_verbal):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.unit = unit
        self.quantity = quantity
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<RecipeIngredient %d %d>" % (self.recipe_id, self.ingredient_id)

Recipe.ingredients = db.relationship("RecipeIngredient",\
                                      back_populates="recipe")


class GroceryItemIngredient(db.Model):
    __tablename__ = "grocery_item_ingredient"

    grocery_id      = db.Column(db.Integer,\
                                db.ForeignKey("grocery_item.grocery_id"),\
                                primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    unit            = db.Column(db.String(20))
    quantity        = db.Column(db.Float)
    quantity_verbal = db.Column(db.String(100))

    grocery_item = db.relationship("GroceryItem", back_populates="ingredients")

    def __init__(self, grocery_id, ingredient_id, unit, quantity,
                 quantity_verbal):
        self.grocery_id = grocery_id
        self.ingredient_id = ingredient_id
        self.unit = unit
        self.quantity = quantity
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<GroceryItemIngredient %d %d>" % \
                (self.grocery_id, self.ingredient_id)

GroceryItem.ingredients = db.relationship("GroceryItemIngredient",\
                                          back_populates="grocery_item")

class TagIngredient(db.Model):
    __tablename__ = "tag_ingredient"

    tag_name      = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),\
                              primary_key=True)
    ingredient_id = db.Column(db.Integer,\
                              db.ForeignKey("ingredient.ingredient_id"),\
                              primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_ingredient_assocs")
    ingredient = db.relationship("Ingredient",\
                                 back_populates="tag_ingredient_assocs")

    def __init__(self, tag_name, ingredient_id):
        self.tag_name = tag_name
        self.ingredient_id = ingredient_id

    def __repr__(self):
        return "<TagIngredient %s %d>" % (self.tag_name, self.ingredient_id)

Ingredient.tag_ingredient_assocs = db.relationship("TagIngredient",\
                                                   back_populates="ingredient")
Tag.tag_ingredient_assocs = db.relationship("TagIngredient",\
                                            back_populates="tag")
Ingredient.tags = association_proxy("tag_ingredient_assocs", "tag")
Tag.ingredients = association_proxy("tag_ingredient_assocs", "ingredient")

class TagRecipe(db.Model):
    __tablename__ = "tag_recipe"

    tag_name  = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),\
                          primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),\
                          primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_recipe_assocs")
    recipe = db.relationship("Recipe", back_populates="tag_recipe_assocs")

    def __init__(self, tag_name, recipe_id):
        self.tag_name = tag_name
        self.recipe_id = recipe_id

    def __repr__(self):
        return "<TagRecipe %s %d>" % (self.tag_name, self.recipe_id)

Recipe.tag_recipe_assocs = db.relationship("TagRecipe", back_populates="recipe")
Tag.tag_recipe_assocs = db.relationship("TagRecipe", back_populates="tag")
Recipe.tags = association_proxy("tag_recipe_assocs", "tag")
Tag.recipes = association_proxy("tag_recipe_assocs", "recipe")

class TagGroceryItem(db.Model):
    __tablename__ = "tag_grocery_item"

    tag_name   = db.Column(db.String(20), db.ForeignKey("tag.tag_name"),\
                           primary_key=True)
    grocery_id = db.Column(db.Integer,\
                           db.ForeignKey("grocery_item.grocery_id"),\
                           primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_grocery_item_assocs")
    grocery_item = db.relationship("GroceryItem",\
                                   back_populates="tag_grocery_item_assocs")

    def __init__(self, tag_name, grocery_id):
        self.tag_name = tag_name
        self.grocery_id = grocery_id

    def __repr__(self):
        return "<TagGroceryItem %s %d>" % (self.tag_name, self.grocery_id)


GroceryItem.tag_grocery_item_assocs = db.relationship("TagGroceryItem",\
                                                      back_populates="grocery_item")
Tag.tag_grocery_item_assocs = db.relationship("TagGroceryItem",\
                                              back_populates="tag")
GroceryItem.tags = association_proxy("tag_grocery_item_assocs", "tag")
Tag.grocery_items = association_proxy("tag_grocery_item_assocs", "grocery_item")
