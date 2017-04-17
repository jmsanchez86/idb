
"""
Build a search index of the database.
"""

import os
import re
import pickle

def build_index(model, index_filename):
    index = dict()
    maximum_wordlength = 20
    def add_to_index(id, text):
        terms = [t.lower() for t in re.compile(r"[\w\'\-]+").findall(text)]
        for term in terms:
            if term in index:
                index[term].add(id)
            else:
                index[term] = {id}

    count = model.query.count()
    status_freq = count // 10
    rows = model.query.all()

    for i, row in enumerate(rows):
        index_text = row.describe()
        id = row.get_id()
        add_to_index(id, index_text)

        if i % status_freq == 0:
            print("Progress: {:.1f}%".format((i / count) * 100))

    with open(index_filename, "wb") as index_file:
        pickle.dump(index, index_file)
