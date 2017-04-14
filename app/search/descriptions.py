
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

