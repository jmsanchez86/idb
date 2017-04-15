#!/usr/bin/env python3

"""
Build a search index and use it to search through the command line.
"""

import sys
from app.api.database_connector import database_connect
from app.search.index import download_descriptions, build_index
from app.search.search import page_search, search, sorted_results_keys

def cmd_text(args):
    database_connect(download_descriptions)

def cmd_build(args):
    build_index()

def cmd_search(args):

    assert(len(args) >= 3)

    start = int(args[0])
    end = int(args[1])

    for idx, result in enumerate(page_search(" ".join(args[2:]), start, end)):
        print("{:3d}: {}".format(idx, result))

def cmd_searchall(args):
    terms_recipes = search(" ".join(args))

    print("\n")

    num_results = 0
    for terms in sorted_results_keys(terms_recipes):
        result_set = terms_recipes[terms]
        print("{} results containing {}".format(len(result_set), terms))
        print(", ".join(str(result.item_id) for result in result_set))
        print("\n")
        num_results += len(result_set)

    print("{num_results} results found.\n"
          .format(num_results=num_results))

def main():

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

