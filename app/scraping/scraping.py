

"""
<Get Random Recipe>
{
    id
    title
    image (download)
    instructions
    readyInMinutes

    tags: [vegeterian, ketogenic, veryPopular, dairyFree, vegan,
           flutenFree, cheap, sustainable, veryHealth, lowFoodmap]
          <Classify Cuisine>: [african, chinese, japanese, korean,
                               vietnamese, thai, indian, british, irish,
                               french, italian, mexican, spanish,
                               middleEastern, jewish, american, cajun,
                               southern, greek, german, nordic,
                               easternEuropean, carribean, latinAmerican]

    description: <Summarize Recipe>
    ingredients: [
        id
        amount
        unit
        originalString
    ]
}

<Find Similar Recipes>
id = recipe id
[
    {
        id
        title
        readyInMinutes
    }
]

<Get Food Information>
{
    image
}

<Get Ingredient Substitutes by Id>
{
    status
    substitutes: [
        substitute:string,
        ...
    ]
}

<Map Ingredients to Grocery Products>
[
    {
        id
        upc
        title
    }
]

<Get Product Information>
{
    images: [something, somethingElse, somethingElseElse]
    badges: ["stuff", "stuff2", ...]
}
"""


"""
start:
    <Get Random Recipe>
    limitLicense = false
    number = 1
    tags = ""
    # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1
    <Classify Cuisine>
        {
            "ingredientList" = newline concatanation of ingredients originalString
            "title" = recipe title
        }
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/cuisine
    <Summarize Recipe>
        id = recipeId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{id}/summary
    <Find Similar Recipes>
        id = recipeId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{id}/similar
    for each ingredientId
        call ingredient(ingredientId)


ingredient:
    <Get Food Information>
        id = ingredientId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/{id}/information

    <Get Ingredient Substitute by Id>
        id = ingredientId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/{id}/substitutes
    <Map Ingredients to Grocery Products>
        {
            "ingredients": [ingredientName],
            "servings": 1,
        }
        # POST https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/map
    for each groceryId
        call product(groceryId)

product:
    <Get Product Information>
        id = groceryId
        # https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/products/{id}

    call tag()

tag:
    Give human names
    Custom images
    Custom descriptions


"""

