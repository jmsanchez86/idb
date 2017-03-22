import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;


export default class RecipeSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var recipe = recipes[id];
    var ingredientList = recipe.ingredient_amount.map(function(ingredient){
      return(
        <div key={ingredient.ingredient_id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient.ingredient_id}>{ingredient.original_string}</Link></p>
        </div>);
    });
    return (
      <div id="unique-content">
          
          <div class="container">
            <h2>{recipe.name}</h2>
            <div class="col-sm-6 thumbnail">
              <img src={recipe.image}/>
              <div class="caption">
                <p>{recipe.blurb}</p>
              </div>
            </div>
          <div class="col-sm-6 list-group container">
            <h4>Ingredients</h4>
            {ingredientList}
          </div>
          <div class="container">
            <h4>Instructions</h4>
            <p>{recipe.instructions}</p>
          </div>
        </div>
      </div>

    );
  }
}
