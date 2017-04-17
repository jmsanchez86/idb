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
      filters: this.initFilters(),
      sorters: this.initSorters(),
      links:   this.initLinks(),
      path: "http://" + apiRoot,
      data:    {},
      };
    this.requestQuery(this.query());
  }

  query() {
    const sorters = this.state.sorters;
    const filters = this.state.filters;
    var params = "http://" + apiRoot + "/search?q=cheese";

    // for (var id in sorters) {
    //   if (sorters[id].checked)
    //     params += id;
    // }

    // var firstTag = true;
    // for (var id in filters ) {
    //   if (filters[id].checked) {
    //     if (firstTag) {
    //       firstTag = false;
    //       params += "&tags="
    //     }
    //     params += filters[id].name + ",";
    //   }
    // }
    // params = firstTag ? params : params.substring(0, params.length-1);
    // params += "&page=" + 0;
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
          //console.log(_data);
          _this.state.links = responseData.links; //_links;
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
             name : 'Ingredients',
             checked : false
          },
      2 : {
             name : 'Recipes',
             checked : false
          },
      3 : {
             name : 'Grocery Items',
             checked : false
          },
      4 : {
             name : 'Tags',
             checked : false
          }
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
        links: {
          active: 0
        }
      });
    const request = this.query();
    this.requestQuery(request);
  }
  handleSelect(type) {
    this.requestQuery(this.state.links[type]);
  }

  render() {
    const data = this.state.data;
    //console.log(data);
    const path = this.state.path;
    const links= this.state.links;
    return (
      <div id="search-page" class="container-fluid">
        <Greeting />
        <SearchSystem
          data={data} 
          path={path}/>
        <VFPagination
          active={this.state.links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>

    );
  }
}
