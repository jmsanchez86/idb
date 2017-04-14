# pylint: disable=missing-docstring
# pylint: disable=invalid-sequence-index
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-import


from functools import wraps
import math
import re

import flask
from flask import request as req

from app.api.models import Ingredient, Recipe, Tag, GroceryItem
from typing import Callable, List, Set

API_BP = flask.Blueprint('api', __name__)

tag_image_prefix = "/static/images/tags/"

def get_taglist_from_query(query_args: dict) -> List[str]:
    return query_args.get("tags").split(",") if "tags" in query_args else []

###################
# Browse Endpoint #
###################

def get_continuation_links(base_url: str, page: int, page_size: int,
                           req_args: dict, maxsize: int):
    # pylint: disable=too-many-locals
    total_pages = int(math.ceil(maxsize / page_size))
    last_page = max(0, total_pages - 1)
    url_template = base_url + "?page={p}"

    for key in (k for k in req_args if k != "page"):
        v = re.sub(' ', '+', req_args.get(key))
        url_template += "&{k}={v}".format(k=key, v=v)

    first_link = url_template.format(p=0)
    last_link = url_template.format(p=last_page, ps=page_size)
    prev_link = url_template.format(p=min(last_page, max(0, page - 1)))
    next_link = url_template.format(p=min(last_page, max(0, page + 1)))

    # first page
    link_dict = dict(active=page)
    if page != 0:
        link_dict["first"] = first_link  # type: ignore
        link_dict["prev"] = prev_link  # type: ignore

    if page != last_page:
        link_dict["next"] = next_link  # type: ignore
        link_dict["last"] = last_link  # type: ignore

    return link_dict


@API_BP.route('/ingredients')
def get_all_ingredients():
    page = int(req.args.get("page", 0))
    page_size = int(req.args.get("page_size", 16))
    sort_key = req.args.get("sort", "alpha")
    tags = get_taglist_from_query(req.args)

    query, table_size_query = Ingredient.get_all(tags, sort_key, page, page_size)
    links = get_continuation_links(req.base_url, page, page_size, req.args,
                                   table_size_query.fetchone()[0])

    return flask.json.jsonify({"data": [{"id": iq.ingredient_id,
                                         "name": iq.name,
                                         "image": iq.image_url}
                                        for iq in query],
                               "links": links})


@API_BP.route('/recipes')
def get_all_recipes():
    page = int(req.args.get("page", 0))
    page_size = int(req.args.get("page_size", 16))
    sort_key = req.args.get("sort", "alpha")
    tags = get_taglist_from_query(req.args)

    query, table_size_query = Recipe.get_all(tags, sort_key, page, page_size)
    links = get_continuation_links(req.base_url, page, page_size, req.args,
                                   table_size_query.fetchone()[0])
    return flask.json.jsonify({"data": [{"id": rq.recipe_id,
                                         "name": rq.name,
                                         "image": rq.image_url,
                                         "blurb": rq.description,
                                         "ready_time": rq.ready_time}
                                        for rq in query],
                               "links": links})


@API_BP.route('/grocery_items')
def get_all_grocery_items():
    page = int(req.args.get("page", 0))
    page_size = int(req.args.get("page_size", 16))
    sort_key = req.args.get("sort", "alpha")
    tags = get_taglist_from_query(req.args)

    query, table_size_query = GroceryItem.get_all(tags, sort_key, page,
                                                  page_size)
    links = get_continuation_links(req.base_url, page, page_size, req.args,
                                   table_size_query.fetchone()[0])
    return flask.json.jsonify({"data": [{"id": gq.grocery_id,
                                         "name": gq.name,
                                         "image": gq.image_url}
                                        for gq in query],
                               "links": links})


@API_BP.route('/tags')
def get_all_tags():
    page = int(req.args.get("page", 0))
    page_size = int(req.args.get("page_size", 16))
    sort_key = req.args.get("sort", "alpha")
    min_occurences = int(req.args.get("min", 0))

    data, table_size = Tag.get_all(min_occurences, sort_key, page, page_size)
    links = get_continuation_links(req.base_url, page, page_size, req.args,
                                   table_size)
    return flask.json.jsonify({"data":
                               [{"name": t.tag_name,
                                 "blurb": t.description,
                                 "image": tag_image_prefix + t.image_url}
                                for t in data],
                               "links": links})


###################
# Detail Endpoint #
###################

def filter_nulls(field, limit):
    for row in field:
        if row.name is not None:
            yield row
            limit -= 1
            if limit <= 0:
                return


@API_BP.route('/ingredients/<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    ing = Ingredient.get(ingredient_id)
    if not ing:
        return flask.abort(404)

    recipe_ing = ing.recipes
    subs = ing.substitutes
    items = ing.get_grocery_items()
    tags = ing.tags

    return flask.json.jsonify({
        "id": ing.ingredient_id,
        "name": ing.name,
        "image": ing.image_url,
        "aisle": ing.aisle,
        "related_recipes": [{"id": ri.recipe_id, "name": ri.recipe.name}
                            for ri in recipe_ing[:5]],
        "subsitute_ingredients": [s.substitute for s in subs],
        "related_grocery_items": [{"id": g.grocery_id, "name": g.name}
                                  for g in items],
        "tags": [{"name": t.tag_name,
                  "image": tag_image_prefix + t.image_url, } for t in tags]
    })


@API_BP.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id: int):
    recipe = Recipe.get(recipe_id)
    if not recipe:
        return flask.abort(404)
    else:
        return flask.json.jsonify(
            {
                "id": recipe.recipe_id,
                "name": recipe.name,
                "image": recipe.image_url,
                "servings": recipe.servings,
                "blurb": recipe.description,
                "instructions": recipe.instructions,
                "source_url": recipe.source_url,
                "ready_time": recipe.ready_time,
                "related_recipes": [{"id": r.recipe_id, "name": r.name}
                                    for r in recipe.similar_recipes],
                "tags": [{"name": t.tag_name,
                          "image": tag_image_prefix + t.image_url}
                         for t in recipe.tags],
                "ingredient_list": [{"id": i.ingredient_id,
                                     "original_string": i.verbal_quantity}
                                    for i in recipe.ingredients]
            })


@API_BP.route('/grocery_items/<int:grocery_item_id>')
def get_grocery_items(grocery_item_id: int):
    product = GroceryItem.get(grocery_item_id)
    if not product:
        return flask.abort(404)
    data = dict(id=product.grocery_id, name=product.name,
                image=product.image_url, upc=product.upc,
                ingredient_id=product.ingredient_id)
    data["tags"] = [{"name": t.tag_name,
                     "image": tag_image_prefix + t.image_url}
                    for t in product.tags]

    similar_items = []
    added = set()  # type: Set[int]
    for item in product.similar_grocery_items:
        if item.grocery_id not in added:
            added.add(item.grocery_id)
            similar_items.append(item)

    data["related_grocery_items"] = [{"id": p.grocery_id, "name": p.name}
                                     for p in similar_items]
    return flask.json.jsonify(data)


@API_BP.route('/tags/<string:tag_name>')
def get_tag(tag_name: str):
    tag = Tag.get(tag_name)
    if not tag:
        return flask.abort(404)
    limit = 10
    data = dict(name=tag.tag_name, blurb=tag.description,
                image=tag_image_prefix + tag.image_url)
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


###################
# Search Endpoint #
###################

@API_BP.route('/search')
def search():
    from app.api.helpers.test_cream_cheese_search_query import\
            get_test_search_query

    if "q" not in req.args:
        return flask.abort(400)

    MOCK_SEARCH_LOOP_SIZE = 30
    page = int(req.args.get("page", 0))
    page_size = int(req.args.get("page_size", 10))
    data = get_test_search_query(page, page_size, MOCK_SEARCH_LOOP_SIZE)
    links = get_continuation_links(req.base_url, page, page_size, req.args,
                                   MOCK_SEARCH_LOOP_SIZE)
    return flask.json.jsonify({'data': data, 'links': links})
