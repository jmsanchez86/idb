import React from "react";

import apiRoot from "./scripts/Config";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";
import VFPagination from "../components/layout/VFPagination";


export default class Recipes extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.initFilters(),
      sorters: this.initSorters(),
      links:   this.initLinks(),
      data:    {},
      };
    this.requestQuery(this.query());
  }

  query() {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = "http://" + apiRoot + "/recipes?page_size=16&sort=";

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
        params += filters[id].name + ",";
      }
    }
    params = firstTag ? params : params.substring(0, params.length-1);
    params += "&page=" + this.state.links.active;
    return params;
  }

  requestQuery(requestString) {
    console.log(requestString);
    var _this = this;
    var _data = {};
    var _links = {};

    //call api with new query params
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
          for (var id in responseData.data){
            _data[id] = responseData.data[id];
          }
          for (var id in responseData.links){
            _links[id] = responseData.links[id];
          }

          _this.state.data = _data;
          _this.state.links = _links;
          _this.forceUpdate();

        });
      })
    .catch(function(err) {
        console.log('Fetch Error: -S', err);
      });
  }

  initFilters() {
    const _filters = {
      1 : {
             name : 'Starter',
             checked : false
          },
      2 : {
             name : 'Morning Meal',
             checked : false
          },
      3 : {
             name : 'Dessert',
             checked : false
          },
      4 : {
             name : 'Snack',
             checked : false
          },
      5 : {
             name : 'Salad',
             checked : false
          },
      6 : {
             name : 'Sauce',
             checked : false
          },
      7 : {
             name : 'Dip',
             checked : false
          },
      8 : {
             name : 'Soup',
             checked : false
          },
      9 : {
             name : 'Vegan',
             checked : false
          },
      10 : {
             name : 'Gluten-free',
             checked : false
          },
    };
    return _filters;
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
       active: 0,
      }
    )
  }

  handleApply(_filters,_sorters) {
    this.setState({
        sorters: _sorters,
        filters: _filters,
        active: 0
      });
    const request = this.query();
    this.requestQuery(request);
  }
  handleSelect(type) {
    this.requestQuery(this.state.links[type]);
  }

  render() {
    const data = this.state.data;
    const links= this.state.links;
    return (
      <div id="grid-page" class="contatiner">
        <Greeting />
        <Controller
          sorters={this.state.sorters}
          filters={this.state.filters}
          handleApply={this.handleApply.bind(this)} />
        <GridSystem
          width={4}
          path="recipes"
          data={data} />
        <VFPagination
          active={this.state.links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>

    );
  }
}
