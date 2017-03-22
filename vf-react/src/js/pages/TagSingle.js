import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;
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

    var recipeList = tag.recipes.map(function(recipe_id){
      return(
        <div key={recipe_id} class="list-group-item">
          <p><Link to={"recipes/" + recipe_id}>{recipes[recipe_id].name}</Link></p>
        </div>);
    });

    return (
      <div id="unique-content">
          <div class="container">
            <div class="text-center">
              <h2>{tag.name}</h2>
              <p>{tag.blurb}</p>
            </div>
            <div class="row">
              <div class="col-lg-6 list-group">
                <h4>Ingredients with this Tag</h4>
                {ingredientList}
              </div>
            </div>
            <div class="row">
              <div class="col-lg-6 list-group">
                <h4>Recipes  with this Tag</h4>
                {recipeList}
              </div>
            </div>

        </div>
      </div>
    );
  }
}
