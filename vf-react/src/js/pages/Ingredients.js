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
      filters: this.initFilters(),
      sorters: this.initSorters()
      };
  }
  query() {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = ".../api/ingredients?sort=";
    for (var id in sorters) {
      if (sorters[id].checked)
        params += id;
    }
    console.log(filters);

    var firstTag = true;
    for (var id in filters ) {
      if (filters[id].checked) {
        if (firstTag) {
          firstTag = false;
          params += "&tags="
        }
        params += id + ",";
      }
    }
    params = firstTag ? params : params.substring(0, params.length-1);
    console.log(params);
    // Query with state.filters and state.sorters
    return ingredients; //TODO
  }
  initFilters() {
    const tags = {};

    for (var id in data.tags) {
      tags[id] = {
          name: data.tags[id].name,
          checked: false,
        }
    }
    return tags; // {id, name, checked}
  }
  initSorters() {
    return (
      {
        alpha:
          {
            name: "A - Z",
            checked: true
          },
        alpha_reversed:
          {
             name: "Z - A",
             checked: false
          }
      }
    )
  }
  handleApply(_filters,_sorters) {
    this.setState({
        sorters: _sorters,
        filters: _filters,
      });
  }
  render() {
    return (
      <div class="contatiner">
        <Greeting />
        <Controller
          sorters={this.state.sorters}
          filters={this.state.filters}
          handleApply={this.handleApply.bind(this)} />
        <GridSystem
          path="ingredients"
          data={this.query()} />
      </div>

    );
  }
}
