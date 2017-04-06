# pylint: disable=missing-docstring
# pylint: disable=invalid-sequence-index


from functools import wraps
import math

import flask

from app.api.models import Ingredient, Recipe, Tag, GroceryItem
from typing import Callable, List

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
    page = query_params.page
    psize = query_params.page_size
    tag_filters = query_params.tag_filters
    sort_param = query_params.sort_key

    total_pages = int(math.ceil(maxsize / psize))
    last_page = max(0, total_pages - 1)
    url_template = base_url + "?page={p}&page_size={ps}&sort={s}"
    first_link = url_template.format(p=0, ps=psize, s=sort_param)
    prev_link = url_template.format(p=min(last_page, max(0, page - 1)),
                                    ps=psize, s=sort_param)
    next_link = url_template.format(p=min(last_page, max(0, page + 1)),
                                    ps=psize, s=sort_param)
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
        page = int(req.args.get("page", 0))
        psize = int(req.args.get("page_size", 16))
        sort_param = req.args.get("sort", "alpha")
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
    query, table_size_query = Ingredient.get_all(query_params.tag_filters,
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
    query, table_size_query = Recipe.get_all(query_params.tag_filters,
                                             query_params.sort_key,
                                             query_params.page,
                                             query_params.page_size)
    return flask.json.jsonify({"data": [{"id": rq.recipe_id,
                                         "name": rq.name,
                                         "image": rq.image_url,
                                         "blurb": rq.description,
                                         "ready_time": rq.ready_time}
                                        for rq in query],
                               "table_size": table_size_query.fetchone()[0]})



@API_BP.route('/grocery_items')
@continuation_route
def get_all_grocery_items(query_params: QueryParams):
    query, table_size_query = GroceryItem.get_all(query_params.tag_filters,
                                                  query_params.sort_key,
                                                  query_params.page,
                                                  query_params.page_size)
    return flask.json.jsonify({"data": [{"id": gq.grocery_id,
                                         "name": gq.name,
                                         "image": gq.image_url}
                                        for gq in query],
                               "table_size": table_size_query.fetchone()[0]})


@API_BP.route('/tags')
@continuation_route
def get_all_tags(query_params: QueryParams):
    min_occurences = int(flask.request.args.get("min", 0))
    resp = Tag.get_all(min_occurences, query_params.sort_key, query_params.page,
                       query_params.page_size)
    return flask.json.jsonify({"data": [{"name": tq.tag_name,
                                         "blurb": tq.description,
                                         "image": tq.image_url,}
                                        for tq in resp[0]],
                               "table_size": resp[1]})


################
# Detail Views #
################


@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    (ing, subs, items, tags) = Ingredient.get(ingredient_id)
    if ing is None:
        return flask.json.jsonify({})
    else:
        return flask.json.jsonify({
            "id": ing.ingredient_id,
            "name": ing.name,
            "image": ing.image_url,
            "aisle": ing.aisle,
            "subsitute_ingredients": [s.substitute for s in subs],
            "related_grocery_items": [{"id": g.grocery_id, "name": g.name}
                                      for g in items],
            "tags": [{"name": t.tag_name,
                      "image": "/static/images/" + t.image_url,} for t in tags]
            })


@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return flask.json.jsonify({})

@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    return flask.json.jsonify({})

@API_BP.route('/tags/<string:tag_name>')
def get_tag(tag_name: str):
    tag = Tag.get(tag_name)
    if not tag:
        return flask.json.jsonify({})
    limit = 10
    data = dict(name=tag.tag_name, blurb=tag.description, image=tag.image_url)
    def filter_nulls(field, limit):
        for row in field:
            if row.name is not None:
                yield row
                limit -= 1
                if limit <= 0:
                    return
    data["related_recipes"] = [
        {"id": r.recipe_id,
         "name": r.name,
         "image": r.image_url}
        for r in filter_nulls(tag.recipes, limit)]
    data["related_ingredients"] = [
        {"id": r.ingredient_id,
         "name": r.name,
         "image": r.image_url}
        for r in filter_nulls(tag.ingredients, limit)]
    data["related_grocery_items"] = [
        {"id": r.grocery_id,
         "name": r.name,
         "image": r.image_url}
        for r in filter_nulls(tag.grocery_items, limit)]
    return flask.json.jsonify(data)
