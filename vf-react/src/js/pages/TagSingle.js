import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;
const grocery_items = data.grocery_items;
const ingredients = data.ingredients;
const tags = data.tags;


export default class TagSingle extends React.Component {
  render() {
    console.log(ingredients);
    const id = this.props.params.id;
    var tag = tags[id];

    const name = tag.name;
    const blurb = tag.blurb;
    const image = tag.image;


    var ingredients = tag.ingredients.map(function(ingredient_id){
      return(
        <div key={ingredient_id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient_id}>{data.ingredients[ingredient_id].name}</Link></p>
        </div>);
    });

    var recipes = tag.recipes.map(function(recipe_id){
      return(
        <div key={recipe_id} class="list-group-item">
          <p><Link to={"recipes/" + recipe_id}>{data.recipes[recipe_id].name}</Link></p>
        </div>);
    });

    var grocery_items = tag.grocery_items.map(function(gi_id){
      return(
        <div key={gi_id} class="list-group-item">
          <p><Link to={"grocery_items/" + gi_id}>{data.grocery_items[gi_id].name}</Link></p>
        </div>);
    });

    return (
      <div class="single container-fluid">
        <div class="row">
          <div class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
            <h2>
              {name}
            </h2>
          </div>
        </div>
        <div class="row">
          <div id="blurb" class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
            <p>
            {blurb}
            </p>
          </div>
        </div>
        <div class="row gutter-20">
          <div class="col-lg-offset-1 col-lg-4 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
              <div class="row">
                <p>
                  <img class="img-rounded img-responsive" src={image} />
                </p>
              </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h4 disabled={!ingredients.length}>Ingredients with this tag</h4>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {ingredients}
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h4 disabled={!recipes.length}>Recipes with this tag</h4>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {recipes}
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h4 disabled={!grocery_items.length}>Products with this tag</h4>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {grocery_items}
              </div>
            </div>

          </div>
        </div>
      </div>
    );
  }
}
