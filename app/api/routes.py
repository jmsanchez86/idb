# pylint: disable=missing-docstring
# pylint: disable=invalid-sequence-index


from copy import deepcopy
from functools import wraps
import math

import flask

from app.api import food_data
from typing import Any, Callable, List, Tuple

API_BP = flask.Blueprint('api', __name__)


################
# Browse Views #
################

class QueryParams:
    # pylint: disable=too-few-public-methods
    def __init__(self,
                 page: int,
                 page_size: int,
                 tag_filters: List[int],
                 sort_key: Tuple[Callable[[Any], Any], bool, str]) -> None:
        self.page = page
        self.page_size = page_size
        self.tag_filters = tag_filters
        self.sort_key = sort_key


# This temporary mock variable exists to simulate that we have 50 items
# for each entry. In reality we will just simulate having 50 items for
# each by looping the lists over and over
MOCK_DATA_MAX_SIZE = 50  # type: int

"""
This function will make a mock list from looping a source list up to a maxsize

PARAMS:
li       a list to loop
page     the row of results to return
page_size the size of the row to return
maxsize  the size of the mocked out loop list
"""


def mock_loop_list(li: List[Any], page: int, page_size: int, maxsize: int):
    # pylint: disable=invalid-name
    assert page >= 0
    assert page_size > 0
    assert maxsize > 0
    assert page * page_size < maxsize

    first_entry = (page * page_size) % len(li)
    resultlist = li[first_entry: min(first_entry + page_size, len(li))]
    entries_left = max(0, page_size - len(resultlist))
    while entries_left > 0:
        entries_to_add = min(len(li), entries_left)
        resultlist += li[:entries_to_add]
        entries_left = entries_left - entries_to_add

    assert len(resultlist) > 0
    return resultlist


def loop_filter_sort(query_params: QueryParams, li: List[Any]):
    # pylint: disable=invalid-name

    def generate_tag_filter(tag_filters: List[int]):
        def filter_func(ele: Any):
            if len(tag_filters) == 0:
                return True

            for tag in tag_filters:
                if tag in ele["tags"]:
                    return True
            return False
        return filter_func

    li = sorted(li, key=query_params.sort_key[0],
                reverse=query_params.sort_key[1])
    li = mock_loop_list(li, query_params.page, query_params.page_size,
                        MOCK_DATA_MAX_SIZE)
    return list(filter(generate_tag_filter(query_params.tag_filters), li))


def get_continuation_links(base_url: str, maxsize: int,
                           query_params: QueryParams):
    # pylint: disable=too-many-arguments
    page = query_params.page
    psize = query_params.page_size
    tag_filters = [str(t) for t in query_params.tag_filters]
    sort_param = query_params.sort_key[2]

    total_pages = int(math.ceil(maxsize / psize))
    last_page = total_pages - 1
    url_template = base_url + "?page={p}&page_size={ps}&sort={s}"
    first_link = url_template.format(p=0, ps=psize, s=sort_param)
    prev_link = url_template.format(p=(page - 1), ps=psize, s=sort_param)
    next_link = url_template.format(p=(page + 1), ps=psize, s=sort_param)
    last_link = url_template.format(p=last_page, ps=psize, s=sort_param)

    if len(tag_filters) > 0:
        tag_query = "&tags={ts}".format(ts=",".join(tag_filters))
        first_link += tag_query
        prev_link += tag_query
        next_link += tag_query
        last_link += tag_query

    # first page
    if page == 0:
        return {
            "next": next_link,
            "last": last_link}
    # last page
    elif page == last_page:
        return {
            "first": first_link,
            "prev": prev_link}
    else:
        return {
            "first": first_link,
            "prev": prev_link,
            "next": next_link,
            "last": last_link}


def continuation_route(route_fn: Callable[[QueryParams], flask.Response]):
    from flask import request as req

    sort_functions = {
        "alpha":           (lambda e: e["name"], False, "alpha"),
        "alpha_reverse":   (lambda e: e["name"], True, "alpha_reverse"),
        "ready_time_asc":  (lambda e: e["ready_time"], False, "ready_time_asc"),
        "ready_time_desc": (lambda e: e["ready_time"], True, "ready_time_desc"),
        "unsorted":        (lambda e: 0, False, "unsorted")
    }

    @wraps(route_fn)
    def wrapped_route_function():
        page = int(req.args.get("page")) if "page" in req.args else 0
        psize = int(req.args.get("page_size")) if "page_size" in req.args \
            else 10
        if page * psize >= MOCK_DATA_MAX_SIZE:
            flask.abort(404)
        else:
            sort_param = req.args.get("sort") if "sort" in req.args \
                else "unsorted"
            tags = req.args.get("tags").split(
                ",") if "tags" in req.args else []
            query_params = QueryParams(page=page, page_size=psize,
                                       tag_filters=[int(tag) for tag in tags],
                                       sort_key=sort_functions[sort_param])
            data = flask.json.loads(route_fn(query_params).data)
            links = get_continuation_links(req.base_url, MOCK_DATA_MAX_SIZE,
                                           query_params)
            resp = flask.json.jsonify({"data": data, "links": links})
            resp.headers["Access-Control-Allow-Origin"] = "*"
            return resp
    return wrapped_route_function


@API_BP.route('/ingredients')
@continuation_route
def get_all_ingredients(query_params: QueryParams):
    mock_data = loop_filter_sort(query_params, food_data.ingredients)
    return flask.json.jsonify(mock_data)


@API_BP.route('/recipes')
@continuation_route
def get_all_recipes(query_params: QueryParams):
    mock_data = loop_filter_sort(query_params, food_data.recipes)
    return flask.json.jsonify(mock_data)


@API_BP.route('/grocery_items/')
@continuation_route
def get_all_grocery_items(query_params: QueryParams):
    mock_data = loop_filter_sort(query_params, food_data.grocery_items)
    return flask.json.jsonify(mock_data)


@API_BP.route('/tags')
@continuation_route
def get_all_tags(query_params: QueryParams):
    query_params.tag_filters = []
    mock_data = loop_filter_sort(query_params, food_data.tags)
    return flask.json.jsonify(mock_data)


################
# Detail Views #
################
####
# Notes: do a replace for REC tags (list comprehension)
# Notes: do a replace for GROCERY_ITEMS tags (list comprehension)
# Notes: TAG ING join, TAG REC join, TAG groc_item


@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    ing = food_data.ingredients
    grocery_items = food_data.grocery_items
    recipes = food_data.recipes
    tags = food_data.tags

    ingredient = deepcopy(ing[ingredient_id - 1])
    ingredient["related_grocery_items"] = [
        {"id": grocery_items[i - 1]["id"], "name": grocery_items[i - 1]["name"]}
        for i in ingredient["related_grocery_items"]]
    ingredient["related_recipes"] = [
        {"id": recipes[i - 1]["id"], "name": recipes[i - 1]["name"]}
        for i in ingredient["related_recipes"]]
    ingredient["tags"] = [
        {"id": tags[i - 1]["id"], "image": tags[i - 1]["image"]}
        for i in ingredient["tags"]]
    return flask.json.jsonify(ingredient)


@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return flask.json.jsonify(food_data.recipes[recipe_id - 1])


@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    return flask.json.jsonify(food_data.grocery_items[grocery_item_id - 1])


@API_BP.route('/tags/<int:tag_id>')
def get_tag(tag_id: int):
    return flask.json.jsonify(food_data.tags[tag_id - 1])
