import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;
console.log(ingredients[1].name);
const tags = data.tags;


export default class TagSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var tag = tags[id];


    var ingredientList = tag.ingredients.map(function(ingredient_id){
      return(
        <div key={ingredient_id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient_id}>{ingredients[ingredient_id].name}</Link></p>
        </div>);
    });

    console.log(ingredientList);

    var recipeList = tag.recipes.map(function(recipe_id){
      return(
        <div key={recipe_id} class="list-group-item">
          <p><Link to={"recipes/" + recipe_id}>{recipes[recipe_id][name]}</Link></p>
        </div>);
    });

    return (
      <div id="unique-content">
          <div class="container">
            <h2>{tag.name}</h2>
            <div class="col-sm-6 thumbnail">
              <div class="caption">
                <p>{tag.blurb}</p>
              </div>
            </div>
          <div class="col-sm-6 list-group container">
            <h4>Ingredients with this Tag</h4>
            {ingredientList}
          </div>
          <div class="col-sm-6 list-group container">
            <h4>Recipes  with this Tag</h4>
            {recipeList}
          </div>
        </div>
      </div>

    );
  }
}
