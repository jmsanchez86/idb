import React from "react";
import { IndexLink, Link } from "react-router";

import OptionalList from "../components/layout/OptionalList";

const data = require('json!../../data/food.json');
const recipes = data.recipes;
const ingredients = data.ingredients;
const tags = data.tags;
const recipe = {
  "blurb": "A cheese and tomato sandwich makes a healthy lunch option, especially when paired with a side salad.",
  "id": 1,
  "image": "http://akns-images.eonline.com/eol_images/Entire_Site/2013424/rs_1024x759-130524141502-1024.GrilledCheeseTomato.ms.052413.jpg",
  "ingredient_ams": [
    {
      "amount": 1.0,
      "ingredient_id": "3",
      "original_string": "1 stick plus 2 tablespoons butter",
      "unit": "stick"
    },
    {
      "amount": 2.0,
      "ingredient_id": "1",
      "original_string": "2 slices of tomatoes",
      "unit": "slice"
    },
    {
      "amount": 2.0,
      "ingredient_id": "9",
      "original_string": "2 slices of bread",
      "unit": "slice"
    }
  ],
  "instructions": "Directions: Spread both slices of bread with a light layer of mayo. Put slice of cheese on one piece of bread. Add tomato slices. Cover tomato slices with other slice of cheese, then cover with other piece of bread. In the meantime, heat griddle or pan with butter. Also spread butter on top of each side of bread. Grill until sandwich is brown on both sides and cheese is melted.",
  "name": "Grilled Cheese with Tomato",
  "ready_time": 10,
  "tags": [
    1,
    2,
    4
  ]
};


export default class RecipeSingle extends React.Component {
  getInstructions(instructions) {
    if (instructions.length) {
      return (
        <p id="instructions">{instructions}</p>
      )
    } else {
      return (
        <p disabled>Sorry, we don't have instructions.</p>
      )
    }
  }

  render() {
    const id = this.props.params.id;
    const name = recipe.name;
    const blurb = recipe.blurb;
    const image = recipe.image;
    const ready_time = recipe.ready_time;
    const instructions = recipe.instructions;
    const ingredients = recipe.ingredient_ams.map(function(ingredient){
      return(
        <div key={ingredient.ingredient_id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient.ingredient_id}>{ingredient.original_string}</Link></p>
        </div>);
    });
    const tags = recipe.tags.map(function(tag){
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
              <div class="row ">
                  {tags}
              </div>
              <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
              <div class="panel-body">
              <h4 >Ready in {ready_time} minutes.</h4>
              </div>
              </div>
              </div>

              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <OptionalList
              title="Ingredients"
              list={ingredients}
              />
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h3 disabled={!instructions.length}>Instructions</h3>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {this.getInstructions(instructions)}
              </div>
            </div>


          </div>
        </div>
      </div>
    );
  }
}
