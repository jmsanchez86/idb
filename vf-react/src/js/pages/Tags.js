import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";
import VFPagination from "../components/layout/VFPagination";

var apiRoot = '' + require('../scripts/Config.js');

export default class Ingredients extends React.Component {
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
    var params = "http://" + apiRoot + "/tags?page_size=16&sort=";

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
    params += "&page=" + 0;
    return params;
  }

  requestQuery(requestString) {
    var _this = this;
    var _data = {};
    var _links = {};

    // call api with new query params
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
          for (var id in responseData.data){
            _data[responseData.data[id].name] = responseData.data[id];
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
    return (
      {
        0:
          {
            name: "All",
            checked: true
          },
        10:
          {
             name: "Lukewarm Popularity",
             checked: false
          },
        30:
          {
             name: "Medium-heat Popularity",
             checked: false
          },
        100:
          {
            name: "On-Fire Popularity",
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
        links: {active: 0}
      });
    const request = this.query();
    this.requestQuery(request);
  }
  handleSelect(type) {
    this.requestQuery(this.state.links[type]);
  }

  render() {
    const data = this.state.data;
    console.log(data);
    const links= this.state.links;
    return (
      <div id="grid-page" class="container">
        <Greeting />
        <Controller
          sorters={this.state.sorters}
          filters={this.state.filters}
          handleApply={this.handleApply.bind(this)} />
        <GridSystem
          width={4}
          path="tags"
          data={data} />
        <VFPagination
          active={this.state.links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>

    );
  }
}
