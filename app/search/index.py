
"""
Build a search index of the database.
"""

import os
import re
import pickle
from pathlib import Path
import app.search.descriptions as desc

def build_index():
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


