import React from "react";
import { IndexLink, Link } from "react-router";

const data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const recipes = data.recipes;
const grocery_items = data.grocery_items;
const tags = data.tags;

export default class IngredientSingle extends React.Component {
  render() {
    console.log(data.recipes);
    const id = this.props.params.id;
    const ingredient = ingredients[id];
    const name = ingredient.name;
    const image = ingredient.image;
    const recipes = ingredient.recipes.map(function(recipe){
      const recp = data.recipes[recipe];
      return (
        <div key={recipe} class="list-group-item">
          <p><Link to={"recipes/" + recipe}>{recp.name}</Link></p>
        </div>);
    });
    const grocery_items = ingredient.grocery_items.map(function(item){
      const groceryItem = data.grocery_items[item];
      return (
        <div key={item} class="list-group-item">
          <p><Link to={"grocery-items/" + item}>{groceryItem.name}</Link></p>
        </div>);
    });
    const tags = ingredient.tags.map(function(tag){
      const tagItem = data.tags[tag];
      return (
        <div key={tag} class="center-block col-lg-2 col-md-2 col-sm-3 col-xs-3">
          <Link to={"tags/" + tag}><img class="img-responsive" src={tagItem.image} /></Link>
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
        <div class="row gutter-20">
          <div class="col-lg-offset-1 col-lg-4 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <div class="row">
                  <p>
                    <img class="img-rounded img-responsive" src={image} />
                  </p>
                </div>
                <div class="row ">
                    {tags}
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h3 disabled={!ingredient.recipes.length}>Related Recipes</h3>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {recipes}
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h3  disabled={!ingredient.grocery_items.length}>Grocery Items</h3>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <p>{grocery_items}</p>
              </div>
            </div>
          </div>
        </div>

      </div>

    );
  }
}
