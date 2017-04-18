
"""
Perform searches with multi-word queries using an index.
"""
# pylint: disable=missing-docstring
# pylint: disable=global-statement
# pylint: disable=invalid-name


import re
import pickle
from app.project_root import get_path_to_file
from app.api.models import Recipe, Ingredient, GroceryItem, Tag
from typing import List

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
    except FileNotFoundError as error:  # pragma: no cover
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
    def __init__(self, model, item_id, terms, is_and):
        self.model = model
        self.item_id = item_id
        self.terms = terms
        self.contexts = None
        self.is_and = is_and

    @staticmethod
    def tag_description(desc: str, terms_to_tag: List[str]) -> str:
        """
        Given a string, replace all occurences of each tag term with that tag
        term wrapped in span tags.
        """
        for term in terms_to_tag:
            desc = re.sub(term, """<span class="search-context">""" + term +
                          "</span>", desc, flags=re.IGNORECASE)
        return desc

    def contextualize(self):
        """
        Build a list of substrings from the description that frame the search
        context.
        """
        assert self.model != None

        item = self.model.get(self.item_id)
        desc = item.describe().replace("\n", " ").replace("\r", " ")
        desc = re.sub(r"\.([A-Z])", r". \1", desc)
        desc = SearchResult.tag_description(desc, self.terms)

        matches = []
        for term in self.terms:
            matches.append(re.search(term, desc,
                                     flags=re.IGNORECASE | re.DOTALL))

        matches.sort(key=lambda match: match.start())

        def make_section(start, end):
            return (max(start, 0), min(end, len(desc)))

        num_leading_chars = 50 + len("""<span class="search-context">""")
        num_following_chars = 50 + len("</span>")
        sections = []
        section = make_section(matches[0].start() - num_leading_chars,
                               matches[0].end() + num_following_chars)
        for match in matches[1:]:
            if match.start() <= section[1]:
                section = make_section(section[0], match.end() + num_following_chars)
            else:
                sections.append(section)
                section = make_section(match.start() - num_leading_chars,
                                       match.end() + num_following_chars)
        if section:
            sections.append(section)

        self.contexts = [desc[section[0]:section[1]]
                         for section in sections]


    def __repr__(self):  # pragma: no cover
        return "<{} id={} terms={}>".format(self.model.__tablename__,
                                            self.item_id, self.terms)

def split_query(query):
    return list(re.compile(r"[^\s]+").findall(query))

def search_model(query, model, terms_to_search_results_map):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    # init_search_index must be called prior
    assert SEARCH_INDICES != None
    assert query != ""

    query_terms = split_query(query.lower())

    # Build a dictionary mapping recipes to a list of terms they contain.
    id_to_terms_map = dict()
    for term in query_terms:
        if term not in SEARCH_INDICES[model.__tablename__]:
            continue
        for elem_id in SEARCH_INDICES[model.__tablename__][term]:
            if elem_id not in id_to_terms_map:
                id_to_terms_map[elem_id] = []
            id_to_terms_map[elem_id].append(term)

    # Flip recipe_terms to get a terms -> recipes dictionary.
    for elem_id, terms in id_to_terms_map.items():
        result = SearchResult(model, elem_id, tuple(terms),
                              len(terms) == len(query_terms))
        if result.terms not in terms_to_search_results_map:
            terms_to_search_results_map[result.terms] = []
        terms_to_search_results_map[result.terms].append(result)

    return terms_to_search_results_map

def sorted_results_keys(search_results_map):
    return [key[1] for key in
            sorted([(len(terms), terms) for terms in search_results_map.keys()],
                   reverse=True)]

def page_search(query, page_number, page_size):
    """
    Performs a search on all models and their attributes. Returns a list of
    SearchResult objects.
    """

    search_results_map = search_model(query, Recipe, dict())
    search_results_map = search_model(query, Ingredient, search_results_map)
    search_results_map = search_model(query, GroceryItem, search_results_map)
    search_results_map = search_model(query, Tag, search_results_map)

    start = page_number * page_size
    end = start + page_size
    sorted_keys = sorted_results_keys(search_results_map)
    search_results = [result
                      for key in sorted_keys
                      for result in search_results_map[key]]

    return search_results[start:end], len(search_results)
