
"""
Perform searches with multi-word queries using an index.
"""

import re
import pickle

# Possible improvements
#   > Turn words into their lexemes to handle plurality and tenses of words.
#   > Promote search results where search terms show up together in the same 
#     order.
#   > Weight searches based on word hit counts and other stats.
#   > Throw away stop words (and, or, with, of)
#   > Handle unicode characters.

class SearchResult:

    def __init__(self, pillar, item_id, description, terms):
        self.pillar = pillar
        self.item_id = item_id
        self.description = description
        self.terms = terms

def split_query(query):
    return list(re.compile("([^\s]+)").findall(query))

def contextualize(description, query):
    args = split_query(query)

    # TODO: Search contextualization.

    return [description]

def search(query, page_number, page_size):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    args = split_query(query)

    if len(args) == 0:
        print("No search terms given.")
        return

    # TODO: Don't load pickle file, use database instead.
    try:
        # Loading the index takes a few seconds usually.
        index = pickle.load(open("index.p", "rb"))
    except FileNotFoundError as error:
        print("Index file index.p not found. You need to build the index"
              " first.\n"
              "\tpython index.py text\n"
              "\tpython index.py build\n")
        return

    # Build a dictionary mapping recipes to a set of terms they contain.
    recipe_termset = dict()
    for term in args:
        if term not in index:
            continue

        for recipe_id in index[term]:
            if recipe_id not in recipe_termset:
                recipe_termset[recipe_id] = set([term])
            else:
                recipe_termset[recipe_id].add(term)

    # No results found, exit early.
    if not recipe_termset:
        print("No results found.")

    # Flip recipe_termset to get a termset -> recipes dictionary.
    termset_recipes = dict()
    for recipe_id in recipe_termset:
        terms = tuple(recipe_termset[recipe_id])
        if terms not in termset_recipes:
            termset_recipes[terms] = set([recipe_id])
        else:
            termset_recipes[terms].add(recipe_id)

    # Display and count the results.

    start = page_number * page_size
    end = start + page_size
    set_n = 0
    total_index = 0
    search_results = []
    sorted_keys = sorted(termset_recipes.keys(),
                         key=lambda tup: len(tup),
                         reverse=True)

    # Find the first result set for the page.
    while set_n < len(termset_recipes):
        termset_results = termset_recipes[sorted_keys[set_n]]
        if total_index + len(termset_results) > start:
            break
        total_index += len(termset_results)
        set_n += 1

    result_index = start - total_index
    while (len(search_results) < end - start
           and set_n < len(termset_recipes)):
        termset_results = list(termset_recipes[sorted_keys[set_n]])
        while (len(search_results) < end - start
               and result_index < len(termset_results)):
            search_results.append(termset_results[result_index])
            result_index += 1
        result_index = 0
        set_n += 1

    return search_results

def searchall(query):
    args = split_query(query)

    if len(args) == 0:
        print("No search terms given.")
        return

    index = None
    try:
        index = pickle.load(open("index.p", "rb"))
    except FileNotFoundError as error:
        print("Index file index.p not found. You need to build the index"
              " first.\n"
              "\tpython index.py text\n"
              "\tpython index.py build\n")
        return

    # Build a dictionary mapping recipes to a set of terms they contain.
    recipe_termset = dict()
    for term in args:
        if term not in index:
            continue

        for recipe_id in index[term]:
            if recipe_id not in recipe_termset:
                recipe_termset[recipe_id] = set([term])
            else:
                recipe_termset[recipe_id].add(term)

    # No results found, exit early.
    if not recipe_termset:
        print("No results found.")

    # Flip recipe_termset to get a termset -> recipes dictionary.
    termset_recipes = dict()
    for recipe_id in recipe_termset:
        terms = tuple(recipe_termset[recipe_id])
        if terms not in termset_recipes:
            termset_recipes[terms] = set([recipe_id])
        else:
            termset_recipes[terms].add(recipe_id)

    # Display and count the results.
    results_count = 0
    for termset in sorted(termset_recipes.keys(),
                              key=lambda tup: len(tup),
                              reverse=True):
        print(termset)
        print(termset_recipes[termset])
        print("\n")
        results_count += len(termset_recipes[termset])

    print("{num_results} results found.\n"
          .format(num_results=results_count))

