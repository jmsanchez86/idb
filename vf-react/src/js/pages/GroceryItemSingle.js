import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;
const groceryItems = data.grocery_items;
const tags = data.tags;

export default class GroceryItemSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    var groceryItem = groceryItems[id];
    var tagList = groceryItem.tags.map(function(tagID){
      const tag = tags[tagID];
      return(
        <div key={tag.name} class="list-group-item">
          <p><Link to={"tags/" + tagID}>{tag.name}</Link></p>
        </div>);
    });
    return (
      <div class="container">
        <div class="media hidden-xs">
          <h3>{groceryItem.name}</h3>
          <div class="media-left">
            <img class="media-object" id="image-single" src={groceryItem.image} alt="..." />
          </div>
          <div class="media-body hidden-xs">
          <h4>Related Ingredient:</h4>
          <div class="list-group-item">
            <p><Link to={"ingredients/" + groceryItem.ingredient}>{ingredients[groceryItem.ingredient].name}</Link></p>
          </div>

          <h4>Tags:</h4>
          {tagList}

          <h4>UPC:</h4>
          <div class="list-group-item">
            <p>{groceryItem.upc}</p>
          </div>

          </div>

        </div>

        <div class="container hidden-sm hidden-md hidden-lg">
          <div class="row">
            <div>
              <h4>{groceryItem.name}</h4>
            </div>
          </div>

          <div class="row">
            <img class="image1" id="image-single-sm" src={groceryItem.image} alt="..." />
          </div>

          <h4>Related Ingredient:</h4>
          <div class="list-group-item">
            <p><Link to={"ingredients/" + groceryItem.ingredient}>{ingredients[groceryItem.ingredient].name}</Link></p>
          </div>

          {tagList.length > 0 ? (<h4 class="media-heading">Tags:</h4>) : (<h4 class="no">Tags:</h4>)}
          {tagList}

          <h4>UPC:</h4>
          <div class="list-group-item">
            <p>{groceryItem.upc}</p>
          </div>

          </div>

        </div>





    );
  }
}
