# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=global-statement

"""
Read data from soure pixabay and write json results to file.
"""

import json
from functools import reduce
#import os
import requests
from keyfile import key

pixabay_domain = "https://pixabay.com/api/?key=" + key + "&image_type=photo&pretty=true&min_width=300&min_height=300&q="

count = 0

def get_image(name):
    """
    Make a get request for the given name and return its image url
    """
    global count
    count += 1
    split_name = name.split()
    formatted_name = reduce((lambda x, y: x + "+" + y), split_name)
    print("getting image " + str(count) + " " + name)
    path = pixabay_domain + formatted_name
    res = requests.get(path)
    res_dict = res.json()
    if res_dict["totalHits"] > 0:
        return res_dict["hits"][0]["webformatURL"]
    else:
        return ""
    

def start():

    with open('recipes.json') as data_file:    
        data = json.load(data_file)
        
    #ingredients = set()
    ids_found = set()
    id_ingredient_pairs = set()
    for recipe in data:
        ingredient_list = data[recipe]["extendedIngredients"]
        for ingredient in ingredient_list:
            if "id" in ingredient and "name" in ingredient:
                if str(ingredient["id"]) not in ids_found:
                    ids_found.add(str(ingredient["id"]))
                    #ingredients.add(ingredient["name"])
                    id_ingredient_pairs.add(( str(ingredient["id"]) , ingredient["name"] ))
            
    #print(id_ingredient_pairs)
    print ("size is " + str(len(id_ingredient_pairs)))
    
    results = {}
    
    
    for (a, b) in id_ingredient_pairs:
        #results[a] = "img"
        results[a] = get_image(b)
    
    
    #results["1"] = get_image("ace of spades")
    #results["2"] = get_image("dog food")
    #results["3"] = get_image("candy cane")
    
    file = open("images", 'w')
    file.write(json.dumps(results))
    file.close()
        
    """    
    res = requests.get(path, headers=spoonacular_headers)    

    recipe_list = get_request_json("recipes/random?limitLicense=false&number=10")
    recipe_queue.extend([recipe["id"] for recipe in recipe_list["recipes"]])
    print("Requests start: {}".format(requests_left + 10))

    while len(recipe_queue) != 0 and not hit_requests_soft_limit:
        recipe(recipe_queue.popleft())

    print("Requests left: {}".format(requests_left))
    print("recipes in deque {}".format(len(recipe_queue)))
    """

if __name__ == "__main__":
    start()