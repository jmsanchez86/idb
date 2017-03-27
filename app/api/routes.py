# pylint: disable=missing-docstring

from functools import wraps
import flask
from app.api import food_data

API_BP = flask.Blueprint('api', __name__)


################
# Browse Views #
################

"""
This temporary mock variable exists to simulate that we have 50 items
for each entry. In reality we will just simulate having 50 items for
each by looping the lists over and over
"""
MOCK_DATA_MAX_SIZE = 50

"""
This function will make a mock list from looping a source list up to a maxsize

PARAMS:
li       a list to loop
page     the row of results to return
pagesize the size of the row to return
maxsize  the size of the mocked out loop list
"""
def mock_loop_list(li, page, pagesize, maxsize):
    # pylint: disable=invalid-name
    assert page >= 0
    assert pagesize > 0
    assert maxsize > 0
    assert page * pagesize < maxsize

    first_entry = (page * pagesize) % len(li)
    resultlist = li[first_entry : min(first_entry + pagesize, len(li))]
    entries_left = max(0, pagesize - len(resultlist))
    while entries_left > 0:
        entries_to_add = min(len(li), entries_left)
        resultlist += li[:entries_to_add]
        entries_left = entries_left - entries_to_add

    assert len(resultlist) > 0
    return resultlist

def continuation_route(route_fn):
    from flask import request as req
    @wraps(route_fn)
    def wrapped_route_function(*args, **kwargs):
        page = int(req.args.get("page")) if "page" in req.args else 0
        psize = int(req.args.get("pagesize")) if "pagesize" in req.args else 10
        return route_fn(page, psize, *args, **kwargs)
    return wrapped_route_function


@API_BP.route('/ingredients')
@continuation_route
def get_all_ingredients(page: int, pagesize: int):
    mock_data = mock_loop_list(food_data.ingredients, page, pagesize,
                               MOCK_DATA_MAX_SIZE)
    return flask.json.jsonify({"data": mock_data})

@API_BP.route('/recipes')
@continuation_route
def get_all_recipes(page: int, pagesize: int):
    mock_data = mock_loop_list(food_data.recipes, page, pagesize,
                               MOCK_DATA_MAX_SIZE)
    return flask.json.jsonify({"data": mock_data})

@API_BP.route('/grocery_items/')
@continuation_route
def get_all_grocery_items(page: int, pagesize: int):
    mock_data = mock_loop_list(food_data.grocery_items, page, pagesize,
                               MOCK_DATA_MAX_SIZE)
    return flask.json.jsonify({"data": mock_data})

@API_BP.route('/tags')
@continuation_route
def get_all_tags(page: int, pagesize: int):
    mock_data = mock_loop_list(food_data.tags, page, pagesize,
                               MOCK_DATA_MAX_SIZE)
    return flask.json.jsonify({"data": mock_data})


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
