
"""
Build a search index from the database.
"""

import os
import sys
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
            print("Progress: {:.3g}%".format(index / recipe_count))



def cmd_text():
    database_connect(cmd_text_db)

def cmd_build():
    print("Build!")

if __name__ == "__main__":

    commands = {"text": cmd_text,
                "build": cmd_build}

    if len(sys.argv) <= 1 or sys.argv[1] not in commands:
        print("Possible options are:\n"
              "python index.py text  - generate text versions of database"
              " items and save them locally.\n"
              "python index.py build - builds the search index cache.")
    else:
        commands[sys.argv[1]]()

