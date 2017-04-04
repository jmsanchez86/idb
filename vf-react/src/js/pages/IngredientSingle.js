import React from "react";
import { IndexLink, Link } from "react-router";

import OptionalList from "../components/layout/OptionalList";


const data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const recipes = data.recipes;
const grocery_items = data.grocery_items;
const tags = data.tags;

export default class IngredientSingle extends React.Component {
  requestQuery(requestString) {

    var _this = this;
    var _ingredients = {}
    var _links = {}
    // call api with new query params
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
          for (var id in responseData.data){
            _ingredients[id] = responseData.data[id];
          }
          for (var id in responseData.links){
            _links[id] = responseData.links[id];
          }

          _this.state.response.data = _ingredients;
          _this.state.response.links = _links;
          _this.forceUpdate();

        });
      })
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });

    this.forceUpdate();
  }
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
          <p><Link to={"grocery_items/" + item}>{groceryItem.name}</Link></p>
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
          <div class="col-lg-offset-1 col-lg-5 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                  <p>
                    <img class="img-rounded img-responsive" src={image} />
                  </p>
              </div>
            </div>
          </div>
          <div class="col-lg-5 col-md-6 col-sm-6 col-xs-12">
            <OptionalList
              title="Related Recipes"
              list={recipes}
              />
            <OptionalList
              title="Grocery Items"
              list={grocery_items}
              />
            <OptionalList
              title="Tags"
              list={tags}
              />
          </div>
        </div>

      </div>

    );
  }
}
