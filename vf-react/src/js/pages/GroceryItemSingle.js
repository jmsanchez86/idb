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
      <div id="unique-content">
          
          <div class="container">
            <h2>{groceryItem.name}</h2>
            <div class="col-sm-6 thumbnail">
              <img src={groceryItem.image}/>
              <div class="caption">
                <p>UPC: {groceryItem.upc}</p>
              </div>
            </div>
          <div class="col-sm-6 list-group container">
            <h4>Tags</h4>
            {tagList}
          </div>
          <div class="container">
            <h4></h4>
            <p>{groceryItem.blurb}</p>
          </div>
        </div>
      </div>

    );
  }
}

