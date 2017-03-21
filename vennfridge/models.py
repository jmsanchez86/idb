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
from sqlalchemy.ext.associationproxy import association_proxy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)



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

    def __init__(self, recipe_id, spoonacular_id, name, image_url, instructions):
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

    ingredient_id     = db.Column(db.Integer, db.ForeignKey("ingredient.ingredient_id"), primary_key=True)
    category          = db.Column(db.String(10), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Float)

    ingredient = db.relationship("Ingredient", back_populates="nutrients")

    def __init__(self, ingredient_id, category, quantity_unit, quantity):
        self.ingredient_id = ingredient_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<IngredientNutrient %d %s>" % (self.ingredient_id, self.category)

Ingredient.nutrients = db.relationship("IngredientNutrient", back_populates="ingredient")

class RecipeNutrient(db.Model):
    __tablename__ = "recipe_nutrient"

    recipe_id         = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), primary_key=True)
    category          = db.Column(db.String(10), primary_key=True)
    quantity_unit     = db.Column(db.String(10))
    quantity          = db.Column(db.Float)

    recipe = db.relationship("Recipe", back_populates="nutrients")

    def __init__(self, recipe_id, category, quantity_unit, quantity):
        self.recipe_id = recipe_id
        self.category = category
        self.quantity_unit = quantity_unit
        self.quantity = quantity

    def __repr__(self):
        return "<RecipeNutrient %d %s>" % (self.recipe_id, self.category)

Recipe.nutrients = db.relationship("RecipeNutrient", back_populates="recipe")


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id       = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    quantity_unit   = db.Column(db.String(20))
    quantity        = db.Column(db.Float)
    quantity_verbal = db.Column(db.String(100))

    recipe = db.relationship("Recipe", back_populates="ingredients")

    def __init__(self, recipe_id, ingredient_id, quantity_unit, quantity,
                 quantity_verbal):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity_unit = quantity_unit
        self.quantity = quantity
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<RecipeIngredient %d %d>" % (self.recipe_id, self.ingredient_id)

Recipe.ingredients = db.relationship("RecipeIngredient", back_populates="recipe")


class GroceryItemIngredient(db.Model):
    __tablename__ = "grocery_item_ingredient"

    grocery_id      = db.Column(db.Integer, db.ForeignKey("grocery_item.grocery_id"), primary_key=True)
    ingredient_id   = db.Column(db.Integer, primary_key=True)
    quantity_unit   = db.Column(db.String(20))
    quantity        = db.Column(db.Float)
    quantity_verbal = db.Column(db.String(100))

    grocery_item = db.relationship("GroceryItem", back_populates="ingredients")

    def __init__(self, grocery_id, ingredient_id, quantity_unit, quantity,
                 quantity_verbal):
        self.grocery_id = grocery_id
        self.ingredient_id = ingredient_id
        self.quantity_unit = quantity_unit
        self.quantity = quantity
        self.quantity_verbal = quantity_verbal

    def __repr__(self):
        return "<GroceryItemIngredient %d %d>" % (self.grocery_id, self.ingredient_id)

GroceryItem.ingredients = db.relationship("GroceryItemIngredient", back_populates="grocery_item")

class TagIngredient(db.Model):
    __tablename__ = "tag_ingredient"

    tag_name      = db.Column(db.String(20), db.ForeignKey("tag.tag_name"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.ingredient_id"), primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_ingredient_assocs")
    ingredient = db.relationship("Ingredient", back_populates="tag_ingredient_assocs")

    def __init__(self, tag_name, ingredient_id):
        self.tag_name = tag_name
        self.ingredient_id = ingredient_id

    def __repr__(self):
        return "<TagIngredient %s %d>" % (self.tag_name, self.ingredient_id)

Ingredient.tag_ingredient_assocs = db.relationship("TagIngredient", back_populates="ingredient")
Tag.tag_ingredient_assocs = db.relationship("TagIngredient", back_populates="tag")
Ingredient.tags = association_proxy("tag_ingredient_assocs", "tag")
Tag.ingredients = association_proxy("tag_ingredient_assocs", "ingredient")

class TagRecipe(db.Model):
    __tablename__ = "tag_recipe"

    tag_name  = db.Column(db.String(20), db.ForeignKey("tag.tag_name"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), primary_key=True)

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

    tag_name   = db.Column(db.String(20), db.ForeignKey("tag.tag_name"), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey("grocery_item.grocery_id"), primary_key=True)

    tag = db.relationship("Tag", back_populates="tag_grocery_item_assocs")
    grocery_item = db.relationship("GroceryItem", back_populates="tag_grocery_item_assocs")

    def __init__(self, tag_name, grocery_id):
        self.tag_name = tag_name
        self.grocery_id = grocery_id

    def __repr__(self):
        return "<TagGroceryItem %s %d>" % (self.tag_name, self.grocery_id)


GroceryItem.tag_grocery_item_assocs = db.relationship("TagGroceryItem", back_populates="grocery_item")
Tag.tag_grocery_item_assocs = db.relationship("TagGroceryItem", back_populates="tag")
GroceryItem.tags = association_proxy("tag_grocery_item_assocs", "tag")
Tag.grocery_items = association_proxy("tag_grocery_item_assocs", "grocery_item")


if __name__ == "__main__":

    print("sqlalchemy version: %s" % sqlalchemy.__version__)
    print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

    db.create_all()

    data = Ingredient(1, 1337, "licorice", "licorice.jpg")
    db.session.add(data)
    data = Ingredient(2, 11784, "lettuce", "lettuce.jpg")
    db.session.add(data)
    data = Ingredient(3, 900, "bread", "bread.jpg")
    db.session.add(data)

    data = IngredientNutrient(1, "surgar", "kilograms", 100)
    db.session.add(data)
    data = IngredientNutrient(1, "calories", "calories", 9001)
    db.session.add(data)
    data = IngredientNutrient(1, "iron", "grams", 123)
    db.session.add(data)

    data = IngredientNutrient(2, "surgar", "grams", 50)
    db.session.add(data)
    data = IngredientNutrient(2, "calories", "joules", 1001)
    db.session.add(data)
    data = IngredientNutrient(2, "iron", "miligrams", 150)
    db.session.add(data)

    data = Recipe(1, 981, "licorlettuce", "licorlettuce.jpg",
        "Blend licorice and lettuce to a liquid consistency. Serve.")
    db.session.add(data)
    data = Recipe(2, 322, "sandwich", "sandwich.jpg",
        "Insert lettuce between two slices of bread.")
    db.session.add(data)

    data = RecipeNutrient(1, "surgar", "kilograms", 1)
    db.session.add(data)
    data = RecipeNutrient(1, "calories", "calories", 2)
    db.session.add(data)
    data = RecipeNutrient(1, "iron", "grams", 3)
    db.session.add(data)

    data = RecipeIngredient(1, 1, "grams", 50, "50 grams of licorice")
    db.session.add(data)
    data = RecipeIngredient(1, 2, "grams", 100, "100 grams of lettuce")
    db.session.add(data)

    data = RecipeNutrient(2, "surgar", "meters", 82)
    db.session.add(data)
    data = RecipeNutrient(2, "calories", "calories", 23)
    db.session.add(data)
    data = RecipeNutrient(2, "iron", "micrograms", 166)
    db.session.add(data)

    data = RecipeIngredient(2, 2, "grams", 50, "1 leaf of lettuce")
    db.session.add(data)
    data = RecipeIngredient(2, 3, "grams", 100, "2 slices of bread")
    db.session.add(data)

    data = GroceryItem(1, 999, "Tom's lettuce", "toms_lettuce.jpg", 141645278962)
    db.session.add(data)
    data = GroceryItem(2, 4321, "Jake's bread", "jakes_bread.jpg", 1234567890)
    db.session.add(data)

    data = GroceryItemIngredient(1, 2, "kilograms", 2, "2 kilograms of lettuce")
    db.session.add(data)
    data = GroceryItemIngredient(2, 3, "slices", 12, "a dozen slices of bread")
    db.session.add(data)

    data = Tag("candy", "caramel_apple.jpg", "Candy foods and snacks.")
    db.session.add(data)
    data = Tag("natural", "industrial.jpg", "Non-artificial.")
    db.session.add(data)

    data = TagIngredient("candy", 1)
    db.session.add(data)
    data = TagIngredient("natural", 2)
    db.session.add(data)
    data = TagIngredient("natural", 3)
    db.session.add(data)

    data = TagRecipe("candy", 1)
    db.session.add(data)
    data = TagRecipe("natural", 2)
    db.session.add(data)

    data = TagGroceryItem("natural", 1)
    db.session.add(data)
    data = TagGroceryItem("natural", 2)
    db.session.add(data)

    db.session.commit()

    # Ingredient by name.
    query = db.session.query(Ingredient).filter_by(name="licorice")
    licorice = query.first()
    assert(licorice.ingredient_id == 1)

    # Nutrition data of an ingredient.
    nutrients = licorice.nutrients
    nutrient_data = set((n.category, n.quantity_unit, n.quantity)
                        for n in nutrients)
    assert(nutrient_data == {("surgar", "kilograms", 100),
                             ("calories", "calories", 9001),
                             ("iron", "grams", 123)})

    # Recipe by name.
    query = db.session.query(Recipe).filter_by(name="sandwich")
    sandwich = query.first()
    assert(sandwich.recipe_id == 2)

    # Nutrition data for recipe.
    nutrients = sandwich.nutrients
    nutrient_data = set((n.category, n.quantity_unit, n.quantity)
                        for n in nutrients)
    assert(nutrient_data == {("surgar", "meters", 82),
                             ("calories", "calories", 23),
                             ("iron", "micrograms", 166)})

    # Ingredients of a recipe.
    ingredients = sandwich.ingredients
    ingredient_data = set((i.ingredient_id, i.quantity_unit, i.quantity)
                          for i in ingredients)
    assert(ingredient_data == {(2, "grams", 50), (3, "grams", 100)})

    # Grocery item by name.
    query = db.session.query(GroceryItem).filter_by(name="Jake's bread")
    jakes_bread = query.first()
    assert(jakes_bread.grocery_id == 2)

    # Ingredients of a grocery item.
    ingredients = jakes_bread.ingredients
    ingredient_data = set((i.ingredient_id, i.quantity_unit, i.quantity)
                          for i in ingredients)
    assert(ingredient_data == {(3, "slices", 12)})

    # Tag by name
    query = db.session.query(Tag).filter_by(tag_name="natural")
    tag = query.first()
    assert(tag.image_url == "industrial.jpg")

    # Tag ingredients
    ingredients = tag.ingredients
    ingredient_data = set(i.ingredient_id for i in ingredients)
    assert(ingredient_data == {2, 3})

    # Tag recipes
    recipes = tag.recipes
    recipe_data = set(r.recipe_id for r in recipes)
    assert(recipe_data == {2})

    # Tag grocery items
    items = tag.grocery_items
    item_data = set(i.grocery_id for i in items)
    assert(item_data == {1, 2})

    print("sqlalchemy version: %s" % sqlalchemy.__version__)
    print("flask_sqlalchemy version: %s" % flask_sqlalchemy.__version__)

