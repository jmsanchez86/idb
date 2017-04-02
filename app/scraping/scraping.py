
"""
Read data from soure API and write json results to files.
"""

import json
import requests
from http.client import HTTPSConnection
from config import api_key
from functools import reduce

class ConnectionException(Exception):
    """
    Raised when a Connection object has an unexpected error.
    """

    def __init__(self, connection, message):
        self.connection = connection
        self.message = message

class Connection:
    """
    Lightweight class to make requests to a restful API.
    """

    def __init__(self, domain_url):
        self.domain_url = domain_url
        self.headers = {
            "Accept": "application/json",
            "X-Mashape-Key": api_key}


    def get_request_json(self, path):
        """
        Make a get request for a resource described by path and returns the
        response object.
        """

        path = self.domain_url + "/" + path

        res = requests.get(path, headers=self.headers)
        res.raise_for_status()

        # if res.status_code != 200:
        #     msg = "Request %s returned status %d with reason: %s."
        #     msg = msg % (path, res.status, res.reason)
        #     raise ConnectionException(self, msg)

        return res.json()

    def post_request_json(self, path, *, post_data=None, json_data=None):
        """
        Make a post request for a resource described by path and returns the
        response object.
        """

        path = self.domain_url + "/" + path

        res = None
        if post_data:
            res = requests.post(path, headers=self.headers, data=post_data)
        else:
            res = requests.post(path, headers=self.headers, json=json_data)

        res.raise_for_status()

        # if res.status != 200:
        #     msg = "Request %s returned status %d with reason: %s."
        #     msg = msg % (path, res.status, res.reason)
        #     raise ConnectionException(self, msg)

        return res.json()



SPOONACULAR_URL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com"

class SpoonacularConnection(Connection):

    def __init__(self):
        Connection.__init__(self, SPOONACULAR_URL)

conn = SpoonacularConnection()
write_queue = {}

def product(grocery_data):
    grocery_id = grocery_data["id"]

    product_data = conn.get_request_json("food/products/" + str(grocery_id))
    write_queue["get_product_information/" + str(grocery_id) + ".json"] = product_data

def ingredient(ingredient_data):
    ingredient_id = ingredient_data["id"]
    substitute_data = conn.get_request_json("food/ingredients/" + str(ingredient_id) + "/substitutes")
    write_queue["get_ingredient_substitute/" + str(ingredient_id) + ".json"] = substitute_data

    grocery_list_data = conn.post_request_json("food/ingredients/map", json_data={
        "ingredients": [ingredient_data["name"]],
        "servings": 1})

    if len(grocery_list_data) > 0:
        for grocery_data in grocery_list_data[0]["products"]:
            product(grocery_data)
            break

def recipe(recipe_data):
    recipe_id = recipe_data["id"]

    write_queue["get_random_recipes/" + str(recipe_id) + ".json"] = recipe_data
    ingredient_names = [ingredient["name"] for ingredient in recipe_data["extendedIngredients"]]
    cuisine_data = conn.post_request_json("recipes/cuisine", post_data={
        "ingredientList": reduce(lambda a, b: a + "\n" + b, ingredient_names),
        "title": recipe_data["title"]})

    write_queue["classify_cuisine/" + str(recipe_id) + ".json"] = cuisine_data

    summary_data = conn.get_request_json("recipes/" + str(recipe_id) + "/summary")
    write_queue["summarize_recipe/" + str(recipe_id) + ".json"] = summary_data

    similar_recipes_data = conn.get_request_json("recipes/" + str(recipe_id) + "/similar")
    write_queue["find_similar_recipes/" + str(recipe_id) + ".json"] = similar_recipes_data

    for ingredient_data in recipe_data["extendedIngredients"]:
        ingredient(ingredient_data)
        break

def start():
    recipe_list = conn.get_request_json("recipes/random?limitLicense=false&number=1")

    for recipe_data in recipe_list["recipes"]:
        recipe(recipe_data)
        # safety first!
        break


if __name__ == "__main__":
    start()


