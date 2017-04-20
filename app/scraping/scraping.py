# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=global-statement

"""
Read data from soure API and write json results to files.
"""

import json
import os
from collections import deque
import requests
from app.scraping.scrape_config import api_key

spoonacular_domain = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com"
spoonacular_headers = {
    "Accept": "application/json",
    "X-Mashape-Key": api_key}

hit_requests_soft_limit = False
requests_left = -1


def check_limit(resp):
    global hit_requests_soft_limit
    global requests_left
    requests_left = int(resp.headers['X-RateLimit-requests-Remaining'])
    hit_requests_soft_limit = requests_left < 250
    if requests_left < 50:
        raise Exception("Hard request limit reached :: requests left ({left})"
                        .format(left=requests_left))


def get_request_json(path):
    """
    Make a get request for a resource described by path and returns the
    response object.
    """

    path = spoonacular_domain + "/" + path
    res = requests.get(path, headers=spoonacular_headers)
    check_limit(res)
    res.raise_for_status()
    return res.json()


def post_request_json(path: str, *, post_data: dict=None, json_data: dict=None):
    """
    Make a post request for a resource described by path and returns the
    response object.
    """

    path = spoonacular_domain + "/" + path
    res = None
    if post_data:
        res = requests.post(path, headers=spoonacular_headers, data=post_data)
    else:
        res = requests.post(path, headers=spoonacular_headers, json=json_data)
    check_limit(res)
    res.raise_for_status()
    return res.json()


def data_exists(filename: str):
    return os.path.isfile("data/" + filename)


def write_json(filename: str, data: dict):
    with open("data/" + filename, 'w') as f:
        print("writing " + filename + "... {}".format(requests_left))
        f.write(json.dumps(data))


def product(grocery_data: dict):
    grocery_id = grocery_data["id"]
    filename = "get_product_information/" + str(grocery_id) + ".json"
    if data_exists(filename):
        return
    product_data = get_request_json("food/products/" + str(grocery_id))
    write_json(filename, product_data)


def ingredient(ingredient_data: dict):
    # sloppy jo mix showed that not every ingredient has an id field
    if "id" not in ingredient_data:
        if "name" not in ingredient_data:
            print("\n\n????  Ingredient <{}> ?????\n\n".format(
                str(ingredient_data)))
        else:
            print("\n\nIngredient <{}> didn't have ID\n\n".format(
                ingredient_data["name"]))
        return

    ingredient_id = ingredient_data["id"]
    filename = "get_ingredient_substitutes/" + str(ingredient_id) + ".json"
    if data_exists(filename):
        return
    substitute_data = get_request_json("food/ingredients/" +
                                       str(ingredient_id) + "/substitutes")
    write_json(filename, substitute_data)
    grocery_list_data = post_request_json("food/ingredients/map", json_data={
        "ingredients": [ingredient_data["name"]],
        "servings": 1})

    write_json("get_product_map/" + str(ingredient_id) +
               ".json", grocery_list_data)
    if len(grocery_list_data) > 0:
        for grocery_data in grocery_list_data[0]["products"][:5]:
            product(grocery_data)
    else:
        print("Ingredient <{}> returned empty from grocery products"
              .format(ingredient_data["name"]))


def recipe(recipe_id: int):
    filename = "recipes/" + str(recipe_id) + ".json"
    if data_exists(filename):
        return

    recipe_data = get_request_json("recipes/" + str(recipe_id) +
                                   "/information?includeNutrition=true")
    write_json(filename, recipe_data)
    summary_data = get_request_json("recipes/" + str(recipe_id) + "/summary")
    write_json("summarize_recipe/" + str(recipe_id) + ".json", summary_data)
    similar_recipes_data = get_request_json("recipes/" + str(recipe_id) +
                                            "/similar")
    for similar_recipe in similar_recipes_data[:4]:
        recipe_queue.append(similar_recipe["id"])
    write_json("find_similar_recipes/" + str(recipe_id) +
               ".json", similar_recipes_data)
    for ingredient_data in recipe_data["extendedIngredients"]:
        ingredient(ingredient_data)


recipe_queue = deque()  # type: deque[int]


def start():
    recipe_list = get_request_json(
        "recipes/random?limitLicense=false&number=10")
    recipe_queue.extend([recipe["id"] for recipe in recipe_list["recipes"]])
    print("Requests start: {}".format(requests_left + 10))

    while len(recipe_queue) != 0 and not hit_requests_soft_limit:
        recipe(recipe_queue.popleft())

    print("Requests left: {}".format(requests_left))
    print("recipes in deque {}".format(len(recipe_queue)))


if __name__ == "__main__":
    start()
