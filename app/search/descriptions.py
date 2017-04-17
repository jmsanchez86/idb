
"""
Generate description strings for items of pillars.
"""

import os

def download_model_descriptions(model):
    """
    Download database data, generate descriptions, and save the descriptions
    locally.
    """

    print("Downloading descriptions for {}s....".format(model.__tablename__))
    count = model.query.count()
    status_freq = count // 10
    rows = model.query.all()
    for index, row in enumerate(rows):
        description = row.describe()
        path = os.path.join("data", model.__tablename__,
                            str(row.get_id()) + ".txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as text_file:
            text_file.write(description)

        if index % status_freq == 0:
            print("Progress: {:.1f}%".format((index / count) * 100))
