

"""
<Get Random Recipe>
{
    id
    title
    image (download)
    instructions
    readyInMinutes

    tags: [vegeterian, ketogenic, veryPopular, dairyFree, vegan,
           flutenFree, cheap, sustainable, veryHealth, lowFoodmap]
          <Classify Cuisine>: [african, chinese, japanese, korean,
                               vietnamese, thai, indian, british, irish,
                               french, italian, mexican, spanish,
                               middleEastern, jewish, american, cajun,
                               southern, greek, german, nordic,
                               easternEuropean, carribean, latinAmerican]

    description: <Summarize Recipe>
    ingredients: [
        id
        amount
        unit
        originalString
    ]
}

<Find Similar Recipes>
id = recipe id
[
    {
        id
        title
        readyInMinutes
    }
]

<Get Food Information>
{
    image
}

<Get Ingredient Substitutes by Id>
{
    status
    substitutes: [
        substitute:string,
        ...
    ]
}

<Map Ingredients to Grocery Products>
[
    {
        id
        upc
        title
    }
]

<Get Product Information>
{
    images: [something, somethingElse, somethingElseElse]
    badges: ["stuff", "stuff2", ...]
}
"""


"""
start:
    <Get Random Recipe>
    limitLicense = false
    number = 1
    tags = ""
    # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1
    <Classify Cuisine>
        {
            "ingredientList" = newline concatanation of ingredients originalString
            "title" = recipe title
        }
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/cuisine
    <Summarize Recipe>
        id = recipeId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{id}/summary
    <Find Similar Recipes>
        id = recipeId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{id}/similar
    for each ingredientId
        call ingredient(ingredientId)


ingredient:
    <Get Food Information>
        id = ingredientId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/{id}/information

    <Get Ingredient Substitute by Id>
        id = ingredientId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/{id}/substitutes
    <Map Ingredients to Grocery Products>
        {
            "ingredients": [ingredientName],
            "servings": 1,
        }
        # POST https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/map
    for each groceryId
        call product(groceryId)

product:
    <Get Product Information>
        id = groceryId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/products/{id}

    call tag()

tag:
    Give human names
    Custom images
    Custom descriptions


"""

import json
from http.client import HTTPSConnection

class ConnectionException(Exception):
    """
    Raised when a Connection object has an unexpected error.
    """

    def __init__(self, connection, message):
        self.connection = connection
        self.message = message

class Connection:
    """
    Light wrapper over an HTTP connection for making consecutive
    requests to a restful API.
    """

    def __init__(self, domain_url):
        self.connection = HTTPSConnection(domain_url)


    def request(self, path, post_headers=None):
        """
        Make a request for a resource described by path and returns the
        response object.
        """

        if post_headers == None:
            self.connection.request("GET", path)
            res = self.connection.getresponse()

            if res.status != 200:
                msg = "Request %s returned status %d with reason: %s."
                msg = msg % (path, res.status, res.reason)
                raise ConnectionException(self, msg)

            return res

        else:

            self.connection.request("POST", path, post_headers)
            res = self.connection.getresponse()

            if res.status != 200:
                msg = "Request %s returned status %d with reason: %s."
                msg = msg % (path, res.status, res.reason)
                raise ConnectionException(self, msg)

            return res


if __name__ == "__main__":

    conn = Connection("jsonplaceholder.typicode.com")

    data = conn.request("/posts/1").read()

    print(json.loads(data))



