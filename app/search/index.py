
"""
Build a search index from the database.
"""

import os
import sys
import time
import re
import pickle
from pathlib import Path
from app.api.database_connector import database_connect

# TODO: This does not belong here.
def format_minutes(ready_time):
    """
    Take an integral amount of minutes and return a human-readable text version.
    """

    minutes = ready_time % 60
    hours = (ready_time // 60) % 24
    days = ready_time // (60 * 24)

    unit_strs = []

    if days == 1:
        unit_strs.append("{} day".format(days))
    elif days > 1:
        unit_strs.append("{} days".format(days))

    if hours == 1:
        unit_strs.append("{} hour".format(hours))
    elif hours > 1:
        unit_strs.append("{} hours".format(hours))

    if minutes == 1:
        unit_strs.append("{} minute".format(minutes))
    elif minutes > 1:
        unit_strs.append("{} minutes".format(minutes))

    return ", ".join(unit_strs)

# TODO: This does not belong here.
def describe_recipe(recipe):
    """
    Generate a text description of a recipe's attributes.
    """

    fmt = ("{name}\n"
           "Recipe id: {recipe_id}\n"
           "Servings: {servings}\n"
           "Ready in: {readyInMinutes}\n"
           "Decription: {description}\n"
           "Instructions: {instructions}")

    return fmt.format(name=recipe.name,
                      recipe_id=recipe.recipe_id,
                      servings=recipe.servings,
                      readyInMinutes=format_minutes(recipe.ready_time),
                      description=recipe.description,
                      instructions=recipe.instructions)



def cmd_text_db(db):

    res = db.engine.execute("SELECT count(recipe_id) as cnt FROM recipe;")
    recipe_count = res.fetchone().cnt

    # Notify the user of the current progress every X recipes.
    status_freq = recipe_count // 10

    for index in range(0, recipe_count):
        res = db.engine.execute("SELECT recipe_id, name, servings, "
                                "ready_time, description, instructions "
                                "FROM recipe ORDER BY recipe_id "
                                "OFFSET {index} LIMIT 1;".format(index=index))

        recipe = res.fetchone()
        text = describe_recipe(recipe)

        path = "data/recipes/{}.txt".format(recipe.recipe_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as text_file:
            text_file.write(text)

        if index % status_freq == 0:
            print("Progress: {:.1f}%".format((index / recipe_count) * 100))

def cmd_text(args):
    database_connect(cmd_text_db)

def cmd_build(args):
    index = dict()

    # TODO: Move constant to an appropriate location.
    # Words longer than this are not indexed.
    maximum_wordlength = 20

    def add_to_index(recipe_id, text):
        # TODO: Match unicode letter characters.
        for term in re.compile(r"([a-zA-Z0-9\'\-]+)").findall(text):
            if term.lower() in index:
                index[term.lower()].add(recipe_id)
            else:
                index[term.lower()] = set([recipe_id])

    # This simplified routine only processes recipes so the generated index
    # lacks a distinction between types of data (ingredients vs recipes vs
    # tags vs ...).

    recipe_paths = list(Path("data/recipes").glob("*.txt"))
    recipe_count = len(recipe_paths)

    # Notify the user of the current progress every X recipes.
    status_freq = recipe_count // 10

    for r_index, recipe_path in enumerate(recipe_paths):
        text = recipe_path.read_text()

        recipe_id = int(recipe_path.name[:-4])

        add_to_index(recipe_id, text)

        if r_index % status_freq == 0:
            print("Progress: {:.1f}%".format((r_index / recipe_count) * 100))

    # TODO: Store index in database using association tables between terms and
    # pillars.
    pickle.dump(index, open("index.p", "wb"))

def cmd_search(args):
    if len(args) == 0:
        print("No search terms given.")
        return

    index = None
    try:
        start = time.perf_counter()
        # Loading the index takes a few seconds usually.
        index = pickle.load(open("index.p", "rb"))

        timediff = time.perf_counter() - start
        print("Index loaded in {:.4f} seconds.".format(timediff))
    except FileNotFoundError as error:
        print("Index file index.p not found. You need to build the index"
              " first.\n"
              "\tpython index.py text\n"
              "\tpython index.py build\n")
        return

    start_time = time.perf_counter()

    recipe_word_hits = dict()

    for term in args:
        if term not in index:
            continue

        for recipe_id in index[term]:
            if recipe_id not in recipe_word_hits:
                recipe_word_hits[recipe_id] = set([term])
            else:
                recipe_word_hits[recipe_id].add(term)

    if not recipe_word_hits:
        timediff = time.perf_counter() - start
        print("No results found. Took {:.6f} seconds".format(timediff))

    hit_group_recipes = dict()

    for recipe_id in recipe_word_hits:
        terms = tuple(recipe_word_hits[recipe_id])
        if terms not in hit_group_recipes:
            hit_group_recipes[terms] = set([recipe_id])
        else:
            hit_group_recipes[terms].add(recipe_id)

    results = hit_group_recipes
    timediff = time.perf_counter() - start
    print(results)
    print("\n\n{num_results} results found in {seconds:.6f} seconds.\n"
          .format(num_results=len(results),
                  seconds=timediff))

def main():

    commands = {"text": cmd_text,
                "build": cmd_build,
                "search": cmd_search}

    if len(sys.argv) <= 1 or sys.argv[1] not in commands:
        print("Possible commands are:\n"
              "python index.py text  - generate text versions of database"
              " items and save them locally.\n"
              "python index.py build - builds the search index cache."
              "python index.py search TERMS - conduct a search using a the"
              " index cache.")
    else:
        commands[sys.argv[1]](sys.argv[2:])

if __name__ == "__main__":
    main()

