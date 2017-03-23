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
        <div key={tag} class="col-lg-2 col-md-2 col-sm-2 col-xs-3">
          <Link to={"tags/" + tag}><img id="tag-single" src={tagItem.image} /></Link>
        </div>);
    });
    return (

      <div class="container">
        <div class="media hidden-sm hidden-xs">
          <h2>{ingredient.name}</h2>
          <div id="media-left" class="media-left">
            <img class="media-object" id="image-single-lg" src={ingredient.image} alt="..." />
            {tagList}
          </div>
          <div class="media-body">
            {recipeList.length > 0 ? (<h4 class="media-heading">Recipes with this Ingredient</h4>) : (<h4 class="no">Recipes with this Ingredient</h4>)}
            {recipeList}
            <br />
            {groceryList.length > 0 ? (<h4 class="media-heading">Related Grocery Items</h4>) : (<h4 class="no">Related Grocery Items</h4>)}
            {groceryList}
          </div>
        </div>

        <div class="container hidden-md hidden-lg">
          <div class="row">
            <div>
              <h3>{ingredient.name}</h3>
            </div>
          </div>

            <div class="row">
              <img class="image1" id="image-single-sm" src={ingredient.image} alt="..." />
            </div>
            <div class="row">
              <div class="col-sm-12 col-xs-12">
                  {tagList}
              </div>
            </div>

          <div id="ingSingleList" class="row">
            <div class="col">
            {recipeList.length > 0 ? (<h4 class="media-heading">Recipes with this Ingredient</h4>) : (<h4 class="no">Recipes with this Ingredient</h4>)}
            {recipeList}
            </div>
          </div>
          <div id="ingSingleList" class="row">
            <div class="col">
            {groceryList.length > 0 ? (<h4 class="media-heading">Related Grocery Items</h4>) : (<h4 class="no">Related Grocery Items</h4>)}
            {groceryList}
            </div>
          </div>
      </div>

    </div>

    );
  }
}
