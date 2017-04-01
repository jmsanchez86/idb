import React from "react";
import { IndexLink, Link } from "react-router";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";

const data = require('json!../../data/food.json');
const tags = data.tags;


export default class Tags extends React.Component {
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
    var params = ".../api/tags?sort=";
    for (var id in sorters) {
      if (sorters[id].checked)
        params += id;
    }

    var firstTag = true;
    for (var id in filters ) {
      if (filters[id].checked) {
        if (firstTag) {
          firstTag = false;
          params += "&min="
        }
        params += id + ",";
      }
    }
    params = firstTag ? params : params.substring(0, params.length-1);
    console.log("Mock API Request:\n" + params);
    // Query with state.filters and state.sorters
    return tags; //TODO
  }
  initFilters() {
    return (
      {
        0:
          {
            name: "All",
            checked: true
          },
        10:
          {
             name: "> 10",
             checked: false
          },
        20:
          {
             name: "> 20",
             checked: false
          }
      }
    )
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
  updateFilters(updatedList) {
    const filters = this.state.filters;
    for (var id in updatedList) {
      filters[id].checked = updatedList[id].checked;
    }
    return filters;
  }
  updateSorters(updatedList) {
    const sorters = this.state.sorters;
    for (var id in updatedList) {
      sorters[id].checked = updatedList[id].checked;
    }
  }
  handleApply(_filters,_sorters) {
    this.setState({
        sorters: _sorters,
        filters: _filters,
      });
  }
  render() {

    return (
      <div>
          <Greeting />
          <Controller
            sorters={this.state.sorters}
            filters={this.state.filters}
            handleApply={this.handleApply.bind(this)} />
          <GridSystem
            path="tags"
            data={this.query()} />
      </div>

    );
  }
}
