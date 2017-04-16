
"""
Perform searches with multi-word queries using an index.
"""
# pylint: disable=missing-docstring


from app.project_root import get_path_to_file
import os
import re
import pickle
from app.search.descriptions import describe_item
from app.api import models

# Possible improvements
#   > Turn words into their lexemes to handle plurality and tenses of words.
#   > Promote search results where search terms show up together in the same 
#     order.
#   > Weight index items based on word hit counts and other stats.
#   > Throw away stop words (and, or, with, of)
#   > Handle unicode characters.

class SearchResult:

    def __init__(self, model, item_id, terms):
        self.model = model
        self.item_id = item_id
        self.terms = terms
        self.contexts = None

    def contextualize(self, db):
        """
        Build a list of substrings from the description that frame the search
        context.
        """
        if self.model.__tablename__:
            res = db.engine.execute("SELECT recipe_id, name, servings, "
                                    "ready_time, description, instructions "
                                    "FROM recipe WHERE recipe_id = {recipe_id}"
                                    "".format(recipe_id=self.item_id))
            description = (describe_item("recipe", res.fetchone())
                           .replace("\n", " ").replace("\r", " "))
            description = re.sub(r"\.([A-Z])", r". \1", description)

            matches = []
            for term in self.terms:
                matches.append(re.search(term, description,
                                         flags=re.IGNORECASE | re.DOTALL))

            matches.sort(key=lambda match: match.start())

            def make_section(start, end):
                return (max(start, 0), min(end, len(description)))

            sections = []
            section = make_section(matches[0].start() - 50,
                                   matches[0].end() + 50)
            for match in matches[1:]:
                if match.start() <= section[1]:
                    section = make_section(section[0], match.end() + 50)
                else:
                    sections.append(section)
                    section = make_section(match.start() - 50,
                                           match.end() + 50)
            if section:
                sections.append(section)

            self.contexts = [description[section[0]:section[1]]
                             for section in sections]


    def __repr__(self):
        return "<{} id={} terms={}>".format(self.model.__tablename__,
                                            self.item_id, self.terms)

def split_query(query):
    return list(re.compile("([^\s]+)").findall(query))

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
        index = pickle.load(open(get_path_to_file("search", "index.p"), "rb"))
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
        result = SearchResult(models.Recipe, recipe_id, tuple(terms))
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

    total_result_count = 0
    for _, result_set in terms_recipes.items():
        total_result_count += len(result_set)

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



    return search_results, total_result_count



