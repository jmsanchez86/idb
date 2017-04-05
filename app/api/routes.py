# pylint: disable=missing-docstring
# pylint: disable=invalid-sequence-index


from copy import deepcopy
from functools import wraps
import math

import flask

from app.api.models import db, Ingredient, TagIngredient, Tag, Recipe,\
                           GroceryItem, get_table_size
from app.api import food_data, models
from typing import Any, Callable, List, Tuple
from sqlalchemy import and_, or_

API_BP = flask.Blueprint('api', __name__)


################
# Browse Views #
################

class QueryParams:
    # pylint: disable=too-few-public-methods
    def __init__(self, page: int, page_size: int, tag_filters: List[str],
                 sort_key: str) -> None:
        self.page = page
        self.page_size = page_size
        self.tag_filters = tag_filters
        self.sort_key = sort_key


def get_continuation_links(base_url: str, maxsize: int,
                           query_params: QueryParams):
    # pylint: disable=too-many-arguments
    page = query_params.page
    psize = query_params.page_size
    tag_filters = query_params.tag_filters
    sort_param = query_params.sort_key

    total_pages = int(math.ceil(maxsize / psize))
    last_page = max(0, total_pages - 1)
    prev_page = min(last_page, max(0, page - 1))
    next_page = min(last_page, max(0, page + 1))
    url_template = base_url + "?page={p}&page_size={ps}&sort={s}"
    first_link = url_template.format(p=0, ps=psize, s=sort_param)
    prev_link = url_template.format(p=prev_page, ps=psize, s=sort_param)
    next_link = url_template.format(p=next_page, ps=psize, s=sort_param)
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
            "last": last_link,
            "active": page}
    # last page
    elif page == last_page:
        return {
            "first": first_link,
            "prev": prev_link,
            "active": page}
    else:
        return {
            "first": first_link,
            "prev": prev_link,
            "next": next_link,
            "last": last_link,
            "active": page}


def continuation_route(route_fn: Callable[[QueryParams], flask.Response]):
    from flask import request as req

    @wraps(route_fn)
    def wrapped_route_function():
        page = int(req.args.get("page")) if "page" in req.args else 0
        psize = int(req.args.get("page_size")) if "page_size" in req.args \
            else 16
        sort_param = req.args.get("sort") if "sort" in req.args \
            else "alpha"
        tags = req.args.get("tags").split(
            ",") if "tags" in req.args else []
        query_params = QueryParams(page=page, page_size=psize,
                                   tag_filters=tags, sort_key=sort_param)
        resp = flask.json.loads(route_fn(query_params).data)
        data = resp["data"]
        table_size = resp["table_size"]
        links = get_continuation_links(req.base_url, table_size, query_params)
        return flask.json.jsonify({"data": data, "links": links})
    return wrapped_route_function


@API_BP.route('/ingredients')
@continuation_route
def get_all_ingredients(query_params: QueryParams):
    query, table_size_query = Ingredient.get_all_sorted_filtered_paged(query_params.tag_filters,
                                                     query_params.sort_key,
                                                     query_params.page,
                                                     query_params.page_size)
    return flask.json.jsonify({"data": [{"id": iq.ingredient_id,
                                "name": iq.name,
                                "image": iq.image_url}
                               for iq in query],
                               "table_size": table_size_query.fetchone()[0]})


@API_BP.route('/recipes')
@continuation_route
def get_all_recipes(query_params: QueryParams):
    mock_data = []
    return flask.json.jsonify(mock_data)


@API_BP.route('/grocery_items')
@continuation_route
def get_all_grocery_items(query_params: QueryParams):
    mock_data = []
    return flask.json.jsonify(mock_data)


@API_BP.route('/tags')
@continuation_route
def get_all_tags(query_params: QueryParams):
    mock_data = []
    return flask.json.jsonify(mock_data)


################
# Detail Views #
################


@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    return flask.json.jsonify({})


@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return flask.json.jsonify({})

@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    return flask.json.jsonify({})

@API_BP.route('/tags/<int:tag_id>')
def get_tag(tag_id: int):
    return flask.json.jsonify({})
