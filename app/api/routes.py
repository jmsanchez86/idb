# pylint: disable=missing-docstring

from functools import wraps
import flask
from app.api import food_data

API_BP = flask.Blueprint('api', __name__)

"""
This temporary mock variable exists to simulate that we have 50 items
for each entry. In reality we will just simulate having 50 items for
each by looping the lists over and over
"""
MOCK_DATA_MAX_SIZE = 50

################
# Browse Views #
################

def continuation_route(route_fn):
    from flask import request
    @wraps(route_fn)
    def wrapped_route_function(*args, **kwargs):
        page = request.args.get("page") if "page" in request.args else 0
        psize = request.args.get("page_size") if "page_size" in request.args else 0
        return route_fn(page, psize, *args, **kwargs)
    return wrapped_route_function


@API_BP.route('/ingredients')
@continuation_route
def get_all_ingredients(page, page_size):
    return flask.json.jsonify({"page": page, "page_size": page_size,
                               "type": "ingredients"})
@API_BP.route('/recipes')
@continuation_route
def get_all_recipes(page, page_size):
    return flask.json.jsonify({"page": page, "page_size": page_size,
                               "type": "recipes"})

@API_BP.route('/grocery_items/')
@continuation_route
def get_all_grocery_items(page, page_size):
    return flask.json.jsonify({"page": page, "page_size": page_size,
                               "type": "grocery items"})

@API_BP.route('/tags')
@continuation_route
def get_all_tags(page, page_size):
    return flask.json.jsonify({"page": page, "page_size": page_size,
                               "type": "tags"})


################
# Detail Views #
################

@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    return flask.json.jsonify(food_data.ingredients[ingredient_id - 1])

@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return flask.json.jsonify(food_data.recipes[recipe_id - 1])

@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    return flask.json.jsonify(food_data.grocery_items[grocery_item_id - 1])

@API_BP.route('/tags/<int:tag_id>')
def get_tag(tag_id: int):
    return flask.json.jsonify(food_data.tags[tag_id - 1])
