import React from "react";
import { IndexLink, Link} from "react-router";

var data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const recipes = data.recipes;
const grocery_items = data.grocery_items;
const tags = data.tags;

export default class TagSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var tag = tags[id];
    var ingredientList = tag.ingredients.map(function(ingredient){
      var ingre = ingredients[ingredient];
      return (
        <div key={ingredient} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient}>{ingre.name}</Link></p>
        </div>);
    });
    var recipeList = tag.recipes.map(function(recipe){
      var recp = recipes[recipe];
      return (
        <div key={recipe} class="list-group-item">
          <p><Link to={"recipes/" + recipe}>{recp.name}</Link></p>
        </div>);
    });
    var groceryList = tag.grocery_items.map(function(item){
      var groceryItem = grocery_items[item];
      return (
        <div key={item} class="list-group-item">
          <p><Link to={"grocery-items/" + item}>{groceryItem.name}</Link></p>
        </div>);
    });
    return (
      <div id="unique-content">

          <div class="container">
            <h2>{tag.name}</h2>
            <p>{tag.blurb}</p><br/>
          </div>

          <div class="col-sm-6 list-group-container">
             <h4>Ingredients</h4>
              {ingredientList}
          </div>

          <div class="col-sm-6 list-group-container">
              <h4>Recipes</h4>
              {recipeList}
          </div>

          <div class="col-sm-6 list-group-container">
              <h4>Grocery Items</h4>
              {groceryList}
          </div>


      </div>

    );
  }
}
