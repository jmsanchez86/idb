
"""
Perform searches with multi-word queries using an index.
"""
# pylint: disable=missing-docstring
# pylint: disable=global-statement
# pylint: disable=invalid-name


import re
import pickle
from app.project_root import get_path_to_file
from app.api import models

SEARCH_INDICES = None

def init_search_index():
    global SEARCH_INDICES
    try:
        current_file = "<no file>"
        SEARCH_INDICES = dict()
        for model in ["recipe", "ingredient", "grocery_item", "tag"]:
            index_file_path = get_path_to_file("search", "search_indices",
                                               model + "_index.p")
            current_file = index_file_path
            with open(index_file_path, "rb") as index_file:
                SEARCH_INDICES[model] = pickle.load(index_file)
    except FileNotFoundError as error:
        raise FileNotFoundError(str(error) + "\n\n" +
                                "Index file {} not found.\n"
                                "Must build the search indices\n"
                                "\tpython main.py build\n".format(current_file))

# Possible improvements
#   > Turn words into their lexemes to handle plurality and tenses of words.
#   > Promote search results where search terms show up together in the same
#     order.
#   > Weight index items based on word hit counts and other stats.
#   > Throw away stop words (and, or, with, of)
#   > Handle unicode characters.

class SearchResult:
    # pylint: disable=too-few-public-methods
    def __init__(self, model, item_id, terms):
        self.model = model
        self.item_id = item_id
        self.terms = terms
        self.contexts = None

    def contextualize(self):
        """
        Build a list of substrings from the description that frame the search
        context.
        """
        if self.model.__tablename__:
            item = self.model.get(self.item_id)
            desc = item.describe().replace("\n", " ").replace("\r", " ")
            desc = re.sub(r"\.([A-Z])", r". \1", desc)

            matches = []
            for term in self.terms:
                matches.append(re.search(term, desc,
                                         flags=re.IGNORECASE | re.DOTALL))

            matches.sort(key=lambda match: match.start())

            def make_section(start, end):
                return (max(start, 0), min(end, len(desc)))

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

            self.contexts = [desc[section[0]:section[1]]
                             for section in sections]


    def __repr__(self):
        return "<{} id={} terms={}>".format(self.model.__tablename__,
                                            self.item_id, self.terms)

def split_query(query):
    return list(re.compile(r"[^\s]+").findall(query))

def search(query):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    # init_search_index must be called prior
    assert SEARCH_INDICES != None
    assert query != ""

    args = split_query(query.lower())

    # Build a dictionary mapping recipes to a list of terms they contain.
    recipe_terms = dict()
    for term in args:
        if term not in SEARCH_INDICES["recipe"]:
            continue
        for recipe_id in SEARCH_INDICES["recipe"][term]:
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
