
from models import *

def mock_data(db):
    data = Ingredient(1, 1337, "licorice", "licorice.jpg")
    db.session.add(data)
    data = Ingredient(2, 11784, "lettuce", "lettuce.jpg")
    db.session.add(data)
    data = Ingredient(3, 900, "bread", "bread.jpg")
    db.session.add(data)

    data = IngredientNutrient(1, "surgar", "kilograms", 100)
    db.session.add(data)
    data = IngredientNutrient(1, "calories", "calories", 9001)
    db.session.add(data)
    data = IngredientNutrient(1, "iron", "grams", 123)
    db.session.add(data)

    data = IngredientNutrient(2, "surgar", "grams", 50)
    db.session.add(data)
    data = IngredientNutrient(2, "calories", "joules", 1001)
    db.session.add(data)
    data = IngredientNutrient(2, "iron", "miligrams", 150)
    db.session.add(data)

    data = Recipe(1, 981, "licorlettuce", "licorlettuce.jpg",
        "Blend licorice and lettuce to a liquid consistency. Serve.")
    db.session.add(data)
    data = Recipe(2, 322, "sandwich", "sandwich.jpg",
        "Insert lettuce between two slices of bread.")
    db.session.add(data)

    data = RecipeNutrient(1, "surgar", "kilograms", 1)
    db.session.add(data)
    data = RecipeNutrient(1, "calories", "calories", 2)
    db.session.add(data)
    data = RecipeNutrient(1, "iron", "grams", 3)
    db.session.add(data)

    data = RecipeIngredient(1, 1, "grams", 50, "50 grams of licorice")
    db.session.add(data)
    data = RecipeIngredient(1, 2, "grams", 100, "100 grams of lettuce")
    db.session.add(data)

    data = RecipeNutrient(2, "surgar", "meters", 82)
    db.session.add(data)
    data = RecipeNutrient(2, "calories", "calories", 23)
    db.session.add(data)
    data = RecipeNutrient(2, "iron", "micrograms", 166)
    db.session.add(data)

    data = RecipeIngredient(2, 2, "grams", 50, "1 leaf of lettuce")
    db.session.add(data)
    data = RecipeIngredient(2, 3, "grams", 100, "2 slices of bread")
    db.session.add(data)

    data = GroceryItem(1, 999, "Tom's lettuce", "toms_lettuce.jpg", 141645278962)
    db.session.add(data)
    data = GroceryItem(2, 4321, "Jake's bread", "jakes_bread.jpg", 1234567890)
    db.session.add(data)

    data = GroceryItemIngredient(1, 2, "kilograms", 2, "2 kilograms of lettuce")
    db.session.add(data)
    data = GroceryItemIngredient(2, 3, "slices", 12, "a dozen slices of bread")
    db.session.add(data)

    data = Tag("candy", "caramel_apple.jpg", "Candy foods and snacks.")
    db.session.add(data)
    data = Tag("natural", "industrial.jpg", "Non-artificial.")
    db.session.add(data)

    data = TagIngredient("candy", 1)
    db.session.add(data)
    data = TagIngredient("natural", 2)
    db.session.add(data)
    data = TagIngredient("natural", 3)
    db.session.add(data)

    data = TagRecipe("candy", 1)
    db.session.add(data)
    data = TagRecipe("natural", 2)
    db.session.add(data)

    data = TagGroceryItem("natural", 1)
    db.session.add(data)
    data = TagGroceryItem("natural", 2)
    db.session.add(data)

    db.session.commit()

