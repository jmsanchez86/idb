
"""
Generate description strings for items of pillars.
"""

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

def describe_item(pillar, item):
    """
    Generate a text description of an items attributes.
    """

    if pillar == "recipe":
        fmt = ("{name}\n"
               "Recipe id: {recipe_id}\n"
               "Servings: {servings}\n"
               "Ready in: {readyInMinutes}\n"
               "Decription: {description}\n"
               "Instructions: {instructions}")

        return fmt.format(name=item.name,
                          recipe_id=item.recipe_id,
                          servings=item.servings,
                          readyInMinutes=format_minutes(item.ready_time),
                          description=item.description,
                          instructions=item.instructions)

    raise Exception("Unknown pillar '{}'.".format(pillar))

def download_descriptions(db):
    """
    Download database data, generate descriptions, and save the descriptions
    locally.
    """

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
        text = desc.describe_item("recipe", recipe)

        path = "data/recipes/{}.txt".format(recipe.recipe_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as text_file:
            text_file.write(text)

        if index % status_freq == 0:
            print("Progress: {:.1f}%".format((index / recipe_count) * 100))

