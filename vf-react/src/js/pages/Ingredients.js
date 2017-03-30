import React from "react";
import { IndexLink, Link } from "react-router";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";

const data = require('json!../../data/food.json');
const ingredients = data.ingredients;


export default class Ingredients extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ingredients: this.initialQuery(), // query database with no params
      tags: this.getTags(),
      sort_params:
        [
          {
            name: "A - Z",
            query: "alpha"
          },
          {
            name: "Z - A",
            query: "zeta"
          }
        ],
      };

  }
  initialQuery() {
    return ingredients;
  }
  getTags() {
    const filters = [];
    const tags = data.tags;
    for (var id in tags) {
      filters.push(
        {
          id: id,
          name: tags[id].name,
          active: false,
        }
      );
    }
    return filters; // {id, name, active}
  }
  updateIngredients(params) {
    console.log("Hi Scott. Which one?");
    console.log(params);
    // call api with new params
    // update ingredient
    this.setState({ingredients}); // re-renders
  }
  render() {
    const ingredients = this.state.ingredients;
    return (

      <div class="contatiner">
        <Greeting />
        <Controller sort_params={this.state.sort_params} filters={this.state.tags} updateList={this.updateIngredients.bind(this)} />
        <GridSystem path="ingredients" data={this.state.ingredients} />
      </div>

    );
  }
}
