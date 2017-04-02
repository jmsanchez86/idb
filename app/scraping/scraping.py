# pylint: disable=invalid-name
# pylint: disable=missing-docstring

"""
Read data from soure API and write json results to files.
"""

from functools import reduce
import requests
from config import api_key

spoonacular_domain = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com"
spoonacular_headers = {
    "Accept": "application/json",
    "X-Mashape-Key": api_key}


def get_request_json(path):
    """
    Make a get request for a resource described by path and returns the
    response object.
    """

    path = spoonacular_domain + "/" + path
    res = requests.get(path, headers=spoonacular_headers)
    res.raise_for_status()
    return res.json()

def post_request_json(path, *, post_data=None, json_data=None):
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
    res.raise_for_status()

    return res.json()


write_queue = {}

def product(grocery_data):
    grocery_id = grocery_data["id"]
    product_data = get_request_json("food/products/" + str(grocery_id))
    write_queue["get_product_information/" +
                str(grocery_id) + ".json"] = product_data

def ingredient(ingredient_data):
    ingredient_id = ingredient_data["id"]
    substitute_data = get_request_json("food/ingredients/" +
                                       str(ingredient_id) + "/substitutes")
    write_queue["get_ingredient_substitute/" +
                str(ingredient_id) + ".json"] = substitute_data

    grocery_list_data = post_request_json("food/ingredients/map", json_data={
        "ingredients": [ingredient_data["name"]],
        "servings": 1})

    if len(grocery_list_data) > 0:
        for grocery_data in grocery_list_data[0]["products"]:
            product(grocery_data)
            break

def recipe(recipe_data):
    recipe_id = recipe_data["id"]

    write_queue["get_random_recipes/" + str(recipe_id) + ".json"] = recipe_data
    ingredient_names = [i["name"] for i in recipe_data["extendedIngredients"]]
    cuisine_data = post_request_json("recipes/cuisine", post_data={
        "ingredientList": reduce(lambda a, b: a + "\n" + b, ingredient_names),
        "title": recipe_data["title"]})

    write_queue["classify_cuisine/" + str(recipe_id) + ".json"] = cuisine_data

    summary_data = get_request_json("recipes/" + str(recipe_id) + "/summary")
    write_queue["summarize_recipe/" + str(recipe_id) + ".json"] = summary_data

    similar_recipes_data = get_request_json("recipes/" + str(recipe_id) +
                                            "/similar")
    write_queue["find_similar_recipes/" + str(recipe_id) +
                ".json"] = similar_recipes_data

    for ingredient_data in recipe_data["extendedIngredients"]:
        ingredient(ingredient_data)
        break

def start():
    recipe_list = get_request_json("recipes/random?limitLicense=false&number=1")

    for recipe_data in recipe_list["recipes"]:
        recipe(recipe_data)
        # safety first!
        break


if __name__ == "__main__":
    start()
