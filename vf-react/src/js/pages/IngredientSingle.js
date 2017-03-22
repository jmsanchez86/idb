import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const recipes = data.recipes;
const grocery_items = data.grocery_items;
const tags = data.tags;

export default class IngredientSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var ingredient = ingredients[id];
    var recipeList = ingredient.recipes.map(function(recipe){
      var recp = recipes[recipe];
      return (
        <div key={recipe} class="list-group-item">
          <p><Link to={"recipes/" + recipe}>{recp.name}</Link></p>
        </div>);
    });
    var groceryList = ingredient.grocery_items.map(function(item){
      var groceryItem = grocery_items[item];
      return (
        <div key={item} class="list-group-item">
          <p><Link to={"grocery-items/" + item}>{groceryItem.name}</Link></p>
        </div>);
    });
    var tagList = ingredient.tags.map(function(tag){
      var tagItem = tags[tag];
      return (
        <div key={tag} class="list-group-item">
          <p><Link to={"tags/" + tag}>{tagItem.name}</Link></p>
        </div>);
    });
    return (
      <div id="unique-content">

          <div class="container">
            <h2>{ingredient.name}</h2>
            <div class="offset-4 col-lg-4 col-md-4 col-sm-4 thumbnail text-center">
              <img src={ingredient.image}/>
            </div>

            <div class="col-sm-6 list-group-container">
              <h4>Recipes</h4>
              {recipeList}
            </div>

            <div class="col-sm-6 list-group-container">
              <h4>Grocery Items</h4>
              {groceryList}
            </div>

            <div class="col-sm-6 list-group-container">
              <h4>Tags</h4>
              {tagList}
            </div>
          </div>


      </div>

    );
  }
}
