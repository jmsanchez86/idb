import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import SearchSystem from "../components/layout/SearchSystem";
import VFPagination from "../components/layout/VFPagination";

var apiRoot = '' + require('../scripts/Config.js');

export default class Recipes extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      links:   this.initLinks(),
      data:    {},
      };
    this.requestQuery(this.query());
  }

  query(search_string) {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = "http://" + apiRoot + "/search?q="+search_string;

    params += "&page=" + 0;
    return params;
  }

  requestQuery(requestString) {
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
          for (var result of responseData.data){
            _data[result.id] = result;
          }
          

          _this.state.data = _data;
          _this.state.links = responseData.links; //_links;
          _this.forceUpdate();

        });
      })
    .catch(function(err) {
        console.log('Fetch Error: -S', err);
      });
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
        links: {
          active: 0
        }
      });
    const request = this.query("cheese");
    this.requestQuery(request);
  }
  handleSelect(type) {
    this.requestQuery(this.state.links[type]);
  }

  render() {
    const data = this.state.data;
    const links= this.state.links;
    return (
      <div id="search-page" class="container-fluid">
        <Greeting />
        <SearchSystem
          data={data} />
        <VFPagination
          active={this.state.links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>

    );
  }
}
