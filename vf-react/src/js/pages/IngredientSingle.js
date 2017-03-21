import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const recipes = data.recipes;
const grocery_items = data.grocery_items;

export default class IngredientSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var ingredient = ingredients[id];
    console.log(ingredient);
    var recipeList = ingredient["recipes"].map(function(recipe){
      var recp = recipes[recipe];
      return (
        <div key={recipe} class="list-group-item">
          <p><Link to={"recipes/" + recipe}>{recp["name"]}</Link></p>
        </div>);
    });
   
    return (
      <div id="unique-content">

          <div class="container">
            <h2>{ingredient.name}</h2>
            <div class="col-sm-6 thumbnail text-center">
              <img src={ingredient.image}/>
            </div>

            <div class="col-sm-6 list-group-container">
              <h4>Recipes</h4>
              {recipeList}
            </div>
          </div>


      </div>

    );
  }
}
