#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Build a search index and use it to search through the command line.
"""

import os
import sys
from app.api.main import API_SERVICE
from app.api.models import Recipe, Ingredient, GroceryItem, Tag
from app.api.database_connector import database_connect
from app.search.descriptions import download_model_descriptions
from app.search.index import build_index
from app.search.search import page_search, search, sorted_results_keys

def cmd_text(args):
    """
    Download the model descriptions as text
    """
    # pylint: disable=unused-argument
    with API_SERVICE.app_context():
        for model in [Recipe, Ingredient, GroceryItem, Tag]:
            download_model_descriptions(model)

def cmd_build(args):
    """
    Build the index_cache_files from the database
    """
    # pylint: disable=unused-argument
    with API_SERVICE.app_context():
        for model in [Recipe, Ingredient, GroceryItem, Tag]:
            tablename = model.__tablename__
            print("Building index for {}...\n".format(tablename))
            index_path = os.path.join("search_indices", tablename + "_index.p")
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            build_index(model, index_path)

def cmd_search(args):
    """
    Perform a test search
    """
    assert len(args) >= 3

    page = int(args[0])
    page_size = int(args[1])

    def on_connect(db):
        """
        Perform the search after we've connected to our db
        """
        results, count = page_search(" ".join(args[2:]), page, page_size)
        print("\n{} results found.\n".format(count))
        for idx, result in enumerate(results):
            print("{:3d}: {}".format(idx, result))
            result.contextualize()
            for context in result.contexts:
                print("\t" + context)

    database_connect(on_connect)

def cmd_searchall(args):
    """
    Perform a searchall
    """

    terms_recipes = search(" ".join(args))
    num_results = 0
    print("\n")
    for terms in sorted_results_keys(terms_recipes):
        result_set = terms_recipes[terms]
        print("{} results containing {}".format(len(result_set), terms))
        print(", ".join(str(result.item_id) for result in result_set))
        print("\n")
        num_results += len(result_set)

    print("{num_results} results found.\n"
          .format(num_results=num_results))

def main():
    """
    Decide which function to execute and run it
    """
    commands = {"text": cmd_text,
                "build": cmd_build,
                "search": cmd_search,
                "searchall": cmd_searchall}

    if len(sys.argv) <= 1 or sys.argv[1] not in commands:
        descriptions = [("python main.py text",
                         "generate text descriptions of the site's data and"
                         " save them locally."),
                        ("python main.py build",
                         "builds a search index using locally saved"
                         " descriptions and saves the index as a pickle file"
                         " called index.p"),
                        ("python main.py search PAGE PAGESIZE TERMS",
                         "conduct a search with pagination and"
                         " contextualization."),
                        ("python main.py searchall TERMS",
                         "conduct a search and display all results.")]

        syntax_max_len = 0
        for syntax, desc in descriptions:
            syntax_max_len = max(syntax_max_len, len(syntax))

        for syntax, desc in descriptions:
            print("{}{} - {}".format(syntax,
                                     " "*(syntax_max_len - len(syntax)),
                                     desc))
    else:
        commands[sys.argv[1]](sys.argv[2:])

if __name__ == "__main__":
    main()
