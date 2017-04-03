import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";
import VFPagination from "../components/layout/VFPagination";

const data = require('json!../../data/food.json');
const ingredients = data.ingredients;
const links = {
  activePage: 0,
  next: "http://api.vennfridge.appspot.com/ingredients?sort=alpha&page=1",
  last: "http://api.vennfridge.appspot.com/ingredients?sort=alpha&page=100" // MOCK DATA
}

export default class Ingredients extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.initFilters(),
      sorters: this.initSorters(),
      links :  this.initLinks(),
      response : {
                    data: ingredients,
                    links: links
                 },
      };
    this.requestQuery(this.query());
  }

  query() {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = "http://api.vennfridge.appspot.com/ingredients?sort=";
    for (var id in sorters) {
      if (sorters[id].checked)
        params += id;
    }

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
    params += "&page=" + this.state.links.activePage;
    console.log("Mock API Request:\n" + params);
    // Query with state.filters and state.sorters
    return params; //TODO
  }

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
        alpha_reverse:
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
       next: "http://api/ingredients?sort=alpha&page=1",
       last: "http://api/ingredients?sort=alpha&page=100" // MOCK DATA
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
    const request = this.query();
    this.requestQuery(request);
  }
  handleSelect(type) {
    console.log(links[type]);
  }
  render() {
    const data = this.state.response.data;
    const links= this.state.response.links;
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
