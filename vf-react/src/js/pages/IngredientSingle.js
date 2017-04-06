import React from "react";
import { IndexLink, Link } from "react-router";

import OptionalList from "../components/layout/OptionalList";


export default class IngredientSingle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sub_ingredients : [],
      grocery_items: [],
      recipes : [],
      tags : [],

      image : '',
      name : '',
      id : this.props.params.id,

    };
    this.requestData();
  }

  requestData() {

    var _this = this;

    const requestString = 'http://api.vennfridge.appspot.com/ingredients/' + _this.state.id;
    console.log(requestString);

    // Fetch singleton's required data.
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {

            _this.setState({
                sub_ingredients : responseData.substitute_ingredients,
                grocery_items : responseData.related_grocery_items,
                recipes : responseData.related_recipes,
                tags : responseData.tags,

                image : responseData.image,
                name : responseData.name,
            });

        });
      })
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  render() {
    const image = this.state.image;
    const name = this.state.name;

    const recipes = this.state.recipes.map(function(recipe){
      return (
        <div key={recipe.id} class="list-group-item">
          <p><Link to={"recipes/" + recipe.id}>{recipe.name}</Link></p>
        </div>);
    });
    const grocery_items = this.state.grocery_items.map(function(item){
      return (
        <div key={item.id} class="list-group-item">
          <p><Link to={"grocery_items/" + item.id}>{item.name}</Link></p>
        </div>);
    });
    const tags = this.state.tags.map(function(tag){
      return (
        <div key={tag.name} class="center-block col-lg-2 col-md-2 col-sm-3 col-xs-3">
          <Link to={"tags/" + tag.name}><img class="img-responsive" src={tag.image} /></Link>
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
              title={"Recipes with " + name }
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
