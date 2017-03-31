# pylint: disable=missing-docstring
# pylint: disable=invalid-name

from app.models import Ingredient, Recipe, RecipeNutrient, GroceryItem,\
    GroceryItemIngredient, Tag, TagIngredient, TagRecipe,\
    TagGroceryItem, IngredientNutrient, RecipeIngredient


def mock_data(db):
    db.session.add(Ingredient(1, 1337, "licorice", "licorice.jpg"))
    db.session.add(Ingredient(2, 11784, "lettuce", "lettuce.jpg"))
    db.session.add(Ingredient(3, 900, "bread", "bread.jpg"))

    db.session.add(IngredientNutrient(1, "sugar", "kilograms", 100))
    db.session.add(IngredientNutrient(1, "calories", "calories", 9001))
    db.session.add(IngredientNutrient(1, "iron", "grams", 123))

    db.session.add(IngredientNutrient(2, "sugar", "grams", 50))
    db.session.add(IngredientNutrient(2, "calories", "joules", 1001))
    db.session.add(IngredientNutrient(2, "iron", "miligrams", 150))

    db.session.add(Recipe(1, 981, "licorlettuce", "licorlettuce.jpg",
                          "Blend licorice and lettuce. Serve."))
    db.session.add(Recipe(2, 322, "sandwich", "sandwich.jpg",
                          "Insert lettuce between two slices of bread."))

    db.session.add(RecipeNutrient(1, "sugar", "kilograms", 1))
    db.session.add(RecipeNutrient(1, "calories", "calories", 2))
    db.session.add(RecipeNutrient(1, "iron", "grams", 3))

    db.session.add(RecipeIngredient(1, 1, "grams", 50,
                                    "50 grams of licorice"))
    db.session.add(RecipeIngredient(1, 2, "grams", 100,
                                    "100 grams of lettuce"))

    db.session.add(RecipeNutrient(2, "sugar", "meters", 82))
    db.session.add(RecipeNutrient(2, "calories", "calories", 23))
    db.session.add(RecipeNutrient(2, "iron", "micrograms", 166))

    db.session.add(RecipeIngredient(2, 2, "grams", 50, "1 leaf of lettuce"))
    db.session.add(RecipeIngredient(2, 3, "grams", 100, "2 slices of bread"))

    db.session.add(GroceryItem(1, 999, "Tom's lettuce", "toms_lettuce.jpg",
                               141645278962))
    db.session.add(GroceryItem(2, 4321, "Jake's bread", "jakes_bread.jpg",
                               1234567890))

    db.session.add(GroceryItemIngredient(1, 2, "kilograms", 2,
                                         "2 kilograms of lettuce"))
    db.session.add(GroceryItemIngredient(2, 3, "slices", 12,
                                         "a dozen slices of bread"))

    db.session.add(Tag("candy", "caramel_apple.jpg",
                       "Candy foods and snacks."))
    db.session.add(Tag("natural", "industrial.jpg", "Non-artificial."))

    db.session.add(TagIngredient("candy", 1))
    db.session.add(TagIngredient("natural", 2))
    db.session.add(TagIngredient("natural", 3))

    db.session.add(TagRecipe("candy", 1))
    db.session.add(TagRecipe("natural", 2))

    db.session.add(TagGroceryItem("natural", 1))
    db.session.add(TagGroceryItem("natural", 2))

    db.session.commit()
