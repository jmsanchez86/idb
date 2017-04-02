import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;
const grocery_items = data.grocery_items;
const tags = data.tags;

export default class GroceryItemSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    const grocery_item = data.grocery_items[id];
    console.log(grocery_item);
    const name = grocery_item.name;
    const image = grocery_item.image;
    const ing_id = grocery_item.ingredient;
    const ingredient = data.ingredients[ing_id];
    const upc = grocery_item.upc;

    const tags = grocery_item.tags.map(function(tag){
      const tagItem = data.tags[tag];
      return (
        <div key={tag} class="center-block col-lg-3 col-md-3 col-sm-3 col-xs-3">
        <Link to={"tags/" + tag}><img class="img-responsive" src={tagItem.image} /></Link>
        </div>);
      });
    return (

            <div class="grocery-item-single single container-fluid">
              <div class="row">
                <div class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
                  <h3>
                    {name}
                  </h3>
                </div>
              </div>
              <div class="row top-buffer gutter-20">
                <div class="col-lg-offset-1 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                  <div class="row">
                    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                      <div class="row">
                        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                          <p>
                            <img class="img-rounded img-responsive" src={image} />
                          </p>
                        </div>
                      </div>
                      <div id="upc" class="row">
                        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
                          <p>
                            UPC: {upc}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <h3 disabled={!ingredient}>Related Ingredient</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <div key={ing_id} class="list-group-item">
                        <p><Link to={"ingredients/" + ing_id}>{ingredient.name}</Link></p>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <h3 disabled={!tags.length}>Tags</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="panel-body">
                      {tags}
                    </div>
                  </div>

                </div>
              </div>

            </div>
    );
  }
}
