import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";
import VFPagination from "../components/layout/VFPagination";

const data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const links = {
  activePage: 0,
  next: ".../api/ingredients?sort=aplha&page=1",
  last: ".../api/ingredients?sort=aplha&page=100" // MOCK DATA
}

export default class Ingredients extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.initFilters(),
      sorters: this.initSorters(),
      links :  this.initLinks(),
      };
  }
  query() {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = "/api/ingredients?sort=";
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
    params += "?page=" + this.state.activePage;
    console.log("Mock API Request:\n" + params);
    // Query with state.filters and state.sorters
    const response = {
      data: ingredients,
      links: this.state.links
    };
    return response; //TODO
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
  initLinks() {
    return (
      {
       activePage: 0,
       next: ".../api/ingredients?sort=aplha&page=1",
       last: ".../api/ingredients?sort=aplha&page=100" // MOCK DATA
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
        activePage: 0
      });
  }
  handleSelect(type) {
    console.log(links[type]);
  }
  render() {
    const response = this.query();
    const data = response.data;
    const links= response.links;
    return (
      <div class="contatiner">
        <Greeting />
        <Controller
          sorters={this.state.sorters}
          filters={this.state.filters}
          handleApply={this.handleApply.bind(this)} />
        <GridSystem
          path="ingredients"
          data={data} />
        <VFPagination
          activePage={links.activePage}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>

    );
  }
}
