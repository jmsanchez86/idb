
"""
Perform searches with multi-word queries using an index.
"""

import re
import pickle

# Possible improvements
#   > Turn words into their lexemes to handle plurality and tenses of words.
#   > Promote search results where search terms show up together in the same 
#     order.
#   > Weight index items based on word hit counts and other stats.
#   > Throw away stop words (and, or, with, of)
#   > Handle unicode characters.

class SearchResult:

    def __init__(self, pillar, item_id, terms):
        self.pillar = pillar
        self.item_id = item_id
        self.terms = terms

    def __repr__(self):
        return "<{} id={} terms={}>".format(self.pillar, self.item_id, self.terms)

def split_query(query):
    return list(re.compile("([^\s]+)").findall(query))

def contextualize(description, query):
    args = split_query(query)

    # TODO: Search contextualization.

    return [description]

def search(query):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    args = split_query(query)

    if len(args) == 0:
        return {}

    # TODO: Don't load pickle file here, we want to load it once.
    try:
        index = pickle.load(open("index.p", "rb"))
    except FileNotFoundError as error:
        print("Index file index.p not found. You need to build the index"
              " first.\n"
              "\tpython index.py text\n"
              "\tpython index.py build\n")
        return

    # Build a dictionary mapping recipes to a list of terms they contain.
    recipe_terms = dict()
    for term in args:
        if term not in index:
            continue
        for recipe_id in index[term]:
            if recipe_id not in recipe_terms:
                recipe_terms[recipe_id] = list([term])
            else:
                recipe_terms[recipe_id].append(term)

    # No results found, exit early.
    if not recipe_terms:
        return {}

    # Flip recipe_terms to get a terms -> recipes dictionary.
    terms_results = {}
    for recipe_id, terms in recipe_terms.items():
        result = SearchResult("recipe", recipe_id, tuple(terms))
        if result.terms not in terms_results:
            terms_results[result.terms] = list([result])
        else:
            terms_results[result.terms].append(result)

    return terms_results

def sorted_results_keys(terms_recipes):
    return [key[1] for key in 
            sorted([(len(terms), terms) for terms in terms_recipes.keys()],
                   reverse=True)]

def page_search(query, page_number, page_size):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    terms_recipes = search(query)

    start = page_number * page_size
    end = start + page_size
    set_n = 0
    total_index = 0
    search_results = []
    sorted_keys = sorted_results_keys(terms_recipes)

    # Find the first result set for the requested page.
    while set_n < len(terms_recipes):
        result_set = terms_recipes[sorted_keys[set_n]]
        if total_index + len(result_set) > start:
            break
        total_index += len(result_set)
        set_n += 1

    # Starting with the first result set of the page, fill search results
    # until the page size is met.
    result_index = start - total_index
    while (len(search_results) < end - start
           and set_n < len(terms_recipes)):
        result_set = list(terms_recipes[sorted_keys[set_n]])
        while (len(search_results) < end - start
               and result_index < len(result_set)):
            search_results.append(result_set[result_index])
            result_index += 1
        result_index = 0
        set_n += 1

    return search_results



