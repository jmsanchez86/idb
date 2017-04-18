"""
Build a search index of the database.
"""

import re
import pickle


def build_index(model, index_filename):
    """
    Given a model and an index file it, create the search index for the model
    model a model
    index_filename the index's filename
    """

    index = dict()

    def add_to_index(model_id, text):
        """
        Add the terms for a model instance's description to the index
        model_id the id of the model instance
        text the description text to index
        """
        terms = [t.lower() for t in re.compile(r"[\w\'\-]+").findall(text)]
        for term in terms:
            if term in index:
                index[term].add(model_id)
            else:
                index[term] = {model_id}

    count = model.query.count()
    status_freq = count // 10
    rows = model.query.all()

    for i, row in enumerate(rows):
        index_text = row.describe()
        model_id = row.get_id()
        add_to_index(model_id, index_text)

        if i % status_freq == 0:
            print("Progress: {:.1f}%".format((i / count) * 100))

    with open(index_filename, "wb") as index_file:
        pickle.dump(index, index_file)
