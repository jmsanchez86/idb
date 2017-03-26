# pylint: disable=missing-docstring

import flask
from app.api import food_data

API_BP = flask.Blueprint('api', __name__)

@API_BP.route('/ingredients')
def get_all_ingredients():
    return '{"result": "all ingredients"}'

@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    return flask.json.jsonify(food_data.ingredients[ingredient_id])

@API_BP.route('/recipes')
def get_all_recipes():
    return '{"result": "all recipes"}'

@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return flask.json.jsonify(food_data.recipes[recipe_id])

@API_BP.route('/grocery_items/')
def get_all_grocery_items():
    return '{"result": "all grocery items"}'

@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    return flask.json.jsonify(food_data.grocery_items[grocery_item_id])

@API_BP.route('/tags')
def get_all_tags():
    return '{"result": "all tags"}'

@API_BP.route('/tags/<int:tag_id>')
def get_tag(tag_id: int):
    return flask.json.jsonify(food_data.tags[tag_id])
