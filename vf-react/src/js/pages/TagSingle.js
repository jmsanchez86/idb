import React from "react";
import { IndexLink, Link } from "react-router";


export default class TagSingle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ingredients  : [],
      grocery_items: [],
      recipes : [],

      blurb : '',
      image : '',
      name : '',
      id : this.props.params.id,

    };
    this.requestData();
  }

  requestData() {

    var _this = this;

    var _ingredients = [];
    var _grocery_items = [];
    var _recipes = [];
  
    var _blurb = '';
    var _image = '';
    var _name = '';

    const requestString = 'http://api.vennfridge.appspot.com/tags/' + _this.state.id;
    console.log(requestString);
    // call api with new query params
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
            const temp_recipes = responseData.recipes;
            const temp_grocery_items = responseData.grocery_items;
            const temp_ingredients = responseData.ingredients;

            for (var id in temp_recipes) {
              _recipes.push(temp_recipes[id]);
            }
            for (var id in temp_grocery_items) {
              _grocery_items.push(temp_grocery_items[id]);
            }
         
            for (var id in temp_ingredients) {
              _ingredients.push(temp_ingredients[id]);
            }

            _blurb = responseData.blurb;
            _image = responseData.image;
            _name = responseData.name;

            _this.setState({
                ingredients : _ingredients,
                grocery_items : _grocery_items,
                recipes : _recipes,

                blurb : _blurb,
                image : _image,
                name : _name,
            });

        });
      })
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  render() {
    
    const name = this.state.name;
    const blurb = this.state.blurb;
    const image = this.state.image;


    var ingredients = this.state.ingredients.map(function(ingredient){
      return(
        <div key={ingredient.id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient.id}>{ingredient.name}</Link></p>
        </div>);
    });

    var recipes = this.state.recipes.map(function(recipe){
      return(
        <div key={recipe.id} class="list-group-item">
          <p><Link to={"recipes/" + recipe.id}>{recipe.name}</Link></p>
        </div>);
    });

    var grocery_items = this.state.grocery_items.map(function(gi){
      return(
        <div key={gi.id} class="list-group-item">
          <p><Link to={"grocery_items/" + gi.id}>{gi.name}</Link></p>
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
