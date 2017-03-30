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
      filters: this.getAllTags(),
      sorters:
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
  getAllTags() {
    const tags = {};

    for (var id in data.tags) {
      tags[id] = {
          name: data.tags[id].name,
          checked: false,
        }
    }
    return tags; // {id, name, checked}
  }
  handleApply(updatedList) {
    for (var id in updatedList) {
      this.state.filters[id].checked = updatedList[id];
    }

    // call api with new params
    // update ingredient
    this.setState({ingredients}); // re-renders
  }
  render() {
    console.log(this.state.filters);
    const ingredients = this.state.ingredients;
    return (

      <div class="contatiner">
        <Greeting />
        <Controller
          sorters={this.state.sorters}
          filters={this.state.filters}
          handleApply={this.handleApply.bind(this)} />
        <GridSystem
          path="ingredients"
          data={this.state.ingredients} />
      </div>

    );
  }
}
