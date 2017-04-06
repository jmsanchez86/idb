"""
Database models described with SQLAlchemy.
"""

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=bad-whitespace
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()  # type: SQLAlchemy

class Recipe(db.Model):
    """
    Table of recipes.
    """

    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    image_url = db.Column(db.Text)
    instructions = db.Column(db.Text)
    description = db.Column(db.Text)
    ready_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    source_url = db.Column(db.Text)

    def __init__(self, recipe_id, name, image_url, instructions, description,
                 ready_time, servings, source_url):
        self.recipe_id = recipe_id
        self.name = name
        self.image_url = image_url
        self.instructions = instructions
        self.description = description
        self.ready_time = ready_time
        self.servings = servings
        self.source_url = source_url

    def __repr__(self):
        return "<Recipe %d %s>" % (self.recipe_id, self.name)

    @staticmethod
    def get_all(filters, order, page, page_size):
        orders = {"alpha": ("name", True), "alpha_reverse": ("name", False),
                  "ready_time_asc": ("ready_time", True),
                  "ready_time_desc": ("ready_time", False)}
        order_param, asc = orders[order]
        counter = " SELECT COUNT (*) FROM ({subquery}) AS cnt;"
        sort_clause = (" ORDER BY {order_param} {asc} ").format(
            order_param=order_param, asc="ASC" if asc else "DESC")
        page_clause = (" LIMIT {size} OFFSET {start}").format(
            start=page_size*page, size=page_size)
        if len(filters) > 0:
            tagclause = ' OR '.join(["tag_name='{}'".format(t) for t in filters])
            filter_clause = (" SELECT recipe_id, name, image_url, description, "
                             "ready_time FROM (SELECT recipe_id, name, image_url, "
                             " description, ready_time, COUNT(recipe_id) AS cnt "
                             "FROM (SELECT r.recipe_id, r.name, r.image_url, "
                             "r.description, r.ready_time, "
                             "t.tag_name FROM recipe r JOIN tag_recipe"
                             " t ON r.recipe_id = t.recipe_id WHERE "
                             "{tags} ) AS fst GROUP BY recipe_id, name, "
                             "image_url, description, ready_time) AS scnd WHERE cnt = "
                             "{tag_count} ")\
                            .format(tags=tagclause, tag_count=len(filters)) +\
                            sort_clause
            count_clause = counter.format(subquery=filter_clause)
            return (db.engine.execute(filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))
        else:
            no_filter_clause = ("SELECT recipe_id, name, image_url, description"
                                ", ready_time FROM recipe " + sort_clause)
            count_clause = counter.format(subquery=no_filter_clause)
            return (db.engine.execute(no_filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))

    @staticmethod
    def get(recipe_id):
        return db.session.query(Recipe).get(recipe_id)

class Ingredient(db.Model):
    """
    Table of ingredients.
    """

    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    image_url = db.Column(db.Text)
    aisle = db.Column(db.Text)

    def __init__(self, ingredient_id, name, image_url, aisle):
        self.ingredient_id = ingredient_id
        self.name = name
        self.image_url = image_url
        self.aisle = aisle

    def __repr__(self):
        return "<Ingredient %d %s>" % (self.ingredient_id, self.name)

    @staticmethod
    def get(ing_id):
        main_ingredient = db.session.query(Ingredient).get(ing_id)
        substitutes = db.session.query(IngredientSubstitute).join(Ingredient)\
                                .filter_by(ingredient_id=ing_id).all()
        related_grocery_items = db.session.query(GroceryItem).join(Ingredient)\
                                          .filter_by(ingredient_id=ing_id).all()
        tags = db.session.query(Tag).join(TagIngredient).join(Ingredient)\
                         .filter_by(ingredient_id=ing_id).all()
        return (main_ingredient, substitutes, related_grocery_items, tags)

    @staticmethod
    def get_all(filters, order, page, page_size):
        orders = {"alpha": ("name", True), "alpha_reverse": ("name", False)}
        order_param, asc = orders[order]
        counter = " SELECT COUNT (*) FROM ({subquery}) AS cnt;"
        sort_clause = (" ORDER BY {order_param} {asc} ").format(
            order_param=order_param, asc="ASC" if asc else "DESC")
        page_clause = (" LIMIT {size} OFFSET {start}").format(
            start=page_size*page, size=page_size)
        if len(filters) > 0:
            tagclause = ' OR '.join(["tag_name='{}'".format(t) for t in filters])
            filter_clause = (" SELECT ingredient_id, name, image_url FROM "
                             "(SELECT ingredient_id, name, image_url, "
                             "COUNT(ingredient_id) AS cnt FROM "
                             "(SELECT i.ingredient_id, i.name, i.image_url, "
                             "t.tag_name FROM ingredient i JOIN tag_ingredient"
                             " t ON i.ingredient_id = t.ingredient_id WHERE "
                             "{tags} ) AS fst GROUP BY ingredient_id, name, "
                             "image_url) AS scnd WHERE cnt = {tag_count} ")\
                            .format(tags=tagclause, tag_count=len(filters)) +\
                            sort_clause
            count_clause = counter.format(subquery=filter_clause)
            return (db.engine.execute(filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))
        else:
            no_filter_clause = ("SELECT ingredient_id, name, image_url FROM "
                                "ingredient " + sort_clause)
            count_clause = counter.format(subquery=no_filter_clause)
            return (db.engine.execute(no_filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))

class IngredientSubstitute(db.Model):
    """
    Table of ingredient substitutes.
    """

    __tablename__ = "ingredient_substitute"

    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id"),
                              primary_key=True)
    substitute = db.Column(db.Text, primary_key=True)

    ingredient = db.relationship("Ingredient", back_populates="substitutes")

    def __init__(self, ingredient_id, substitute):
        self.ingredient_id = ingredient_id
        self.substitute = substitute

    def __repr__(self):
        return "<Ingredient Substitute %d %s>" % (self.ingredient_id,
                                                  self.substitute)

Ingredient.substitutes = db.relationship("IngredientSubstitute",
                                         back_populates="ingredient")


class GroceryItem(db.Model):
    """
    Table of Grocery Items.
    """

    __tablename__ = "grocery_item"

    grocery_id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id"),
                              primary_key=True)
    name = db.Column(db.Text)
    image_url = db.Column(db.Text)
    upc = db.Column(db.String(20))

    def __init__(self, grocery_id, ingredient_id, name, image_url, upc):
        self.grocery_id = grocery_id
        self.ingredient_id = ingredient_id
        self.name = name
        self.image_url = image_url
        self.upc = upc

    def __repr__(self):
        return "<Grocery item %d %s>" % (self.grocery_id, self.name)

    @staticmethod
    def get(grocery_id):
        query = db.session.query(GroceryItem).filter_by(grocery_id=grocery_id)
        return query.first()

    @staticmethod
    def get_all(filters, order, page, page_size):
        orders = {"alpha": ("name", True), "alpha_reverse": ("name", False)}
        order_param, asc = orders[order]
        counter = " SELECT COUNT (*) FROM ({subquery}) AS cnt;"
        sort_clause = (" ORDER BY {order_param} {asc} ").format(
            order_param=order_param, asc="ASC" if asc else "DESC")
        page_clause = (" LIMIT {size} OFFSET {start}").format(
            start=page_size*page, size=page_size)
        if len(filters) > 0:
            tagclause = ' OR '.join(["tag_name='{}'".format(t) for t in filters])
            filter_clause = (" SELECT distinct grocery_id, name, image_url FROM "
                             "(SELECT grocery_id, ingredient_id, name, image_url, "
                             "COUNT(grocery_id) AS cnt FROM "
                             "(SELECT g.grocery_id, g.ingredient_id, g.name, "
                             "g.image_url, "
                             "t.tag_name FROM grocery_item g JOIN tag_grocery_item "
                             "t ON (g.ingredient_id = t.ingredient_id and "
                             "g.grocery_id = t.grocery_id and g.name IS NOT NULL) WHERE "
                             "{tags} ) AS fst GROUP BY grocery_id, "
                             "ingredient_id, name, "
                             "image_url) AS scnd WHERE cnt = {tag_count} ")\
                            .format(tags=tagclause, tag_count=len(filters)) +\
                            sort_clause
            count_clause = counter.format(subquery=filter_clause)
            return (db.engine.execute(filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))
        else:
            no_filter_clause = ("SELECT distinct grocery_id, name, "
                                "image_url FROM "
                                "( SELECT grocery_id, name, image_url "
                                "FROM grocery_item WHERE name IS NOT NULL) "
                                "as fst " + sort_clause)
            count_clause = counter.format(subquery=no_filter_clause)
            return (db.engine.execute(no_filter_clause + page_clause + ";"),
                    db.engine.execute(count_clause))


class Tag(db.Model):
    """
    Table of tags.
    """

    __tablename__ = "tag"

    tag_name = db.Column(db.String(50), primary_key=True)
    image_url = db.Column(db.Text)
    description = db.Column(db.Text)

    def __init__(self, tag_name, image_url, description):
        self.tag_name = tag_name
        self.image_url = image_url
        self.description = description

    def __repr__(self):
        return "<Tag %s>" % (self.tag_name)

    @staticmethod
    def get(tag_name):
        query = db.session.query(Tag).filter_by(tag_name=tag_name)
        return query.first()


    @staticmethod
    def get_all(min_occurences, order, page, page_size):
        count_recipe_query = db.engine.execute\
                             ("SELECT tag.tag_name, tag.description, "
                              "tag.image_url, COUNT(tag_recipe.recipe_id) "
                              "AS cnt FROM tag LEFT JOIN tag_recipe ON "
                              "(tag.tag_name = tag_recipe.tag_name) GROUP BY "
                              "tag.tag_name;")
        orders = {"alpha": False,
                  "alpha_reverse": True}
        filtered_tags = [pair for pair in count_recipe_query\
                         if pair.cnt >= min_occurences]
        sorted_tags = sorted(filtered_tags,
                             key=lambda e: e.tag_name,
                             reverse=orders[order])

        return (sorted_tags[page * page_size: page * page_size + page_size],
                len(sorted_tags))

class RecipeIngredient(db.Model):
    """
    Ingredients and quantities contained in a recipe.
    """

    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),
                          primary_key=True)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id"),
                              primary_key=True)
    verbal_quantity = db.Column(db.Text, primary_key=True)

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

    tag_name = db.Column(db.String(50), db.ForeignKey("tag.tag_name"),
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

    tag_name = db.Column(db.String(50), db.ForeignKey("tag.tag_name"),
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

    tag_name = db.Column(db.String(50), db.ForeignKey("tag.tag_name"),
                         primary_key=True)
    ingredient_id = db.Column(db.Integer, primary_key=True)
    grocery_id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([ingredient_id, grocery_id],
                                              [GroceryItem.ingredient_id,
                                               GroceryItem.grocery_id]), {})

    tag = db.relationship("Tag", back_populates="tag_grocery_item_assocs")
    grocery_item = db.relationship("GroceryItem",
                                   back_populates="tag_grocery_item_assocs")

    def __init__(self, tag_name, ingredient_id, grocery_id):
        self.tag_name = tag_name
        self.ingredient_id = ingredient_id
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

class SimilarRecipe(db.Model):
    """
    Association table of recipes to similar recipes.
    """

    __tablename__ = "similar_recipe"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),
                          primary_key=True)
    similar_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"),
                           primary_key=True)

    recipe = db.relationship("Recipe", back_populates="similar_recipe_assocs",
                             foreign_keys=[recipe_id])
    similar = db.relationship("Recipe", foreign_keys=[similar_id])

    def __init__(self, recipe_id, similar_id):
        self.recipe_id = recipe_id
        self.similar_id = similar_id

Recipe.similar_recipe_assocs =\
        db.relationship("SimilarRecipe",
                        back_populates="recipe",
                        foreign_keys=[SimilarRecipe.recipe_id])
Recipe.similar_recipes = association_proxy("similar_recipe_assocs", "similar")

class SimilarGroceryItem(db.Model):
    """
    Association table of grocery items to similar grocery items.
    """

    __tablename__ = "similar_grocery_item"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    grocery_id = db.Column(db.Integer, primary_key=True)
    similar_id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([ingredient_id, grocery_id],
                                              [GroceryItem.ingredient_id,
                                               GroceryItem.grocery_id]),
                      db.ForeignKeyConstraint([ingredient_id, similar_id],
                                              [GroceryItem.ingredient_id,
                                               GroceryItem.grocery_id]), {})

    grocery_item = db.relationship("GroceryItem",
                                   back_populates="similar_grocery_item_assocs",
                                   foreign_keys=[ingredient_id, grocery_id])
    similar = db.relationship("GroceryItem",
                              foreign_keys=[ingredient_id, similar_id])

    def __init__(self, ingredient_id, grocery_id, similar_id):
        self.ingredient_id = ingredient_id
        self.grocery_id = grocery_id
        self.similar_id = similar_id

GroceryItem.similar_grocery_item_assocs =\
        db.relationship("SimilarGroceryItem", back_populates="grocery_item",
                        foreign_keys=[SimilarGroceryItem.grocery_id])
GroceryItem.similar_grocery_items =\
        association_proxy("similar_grocery_item_assocs", "similar")


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
