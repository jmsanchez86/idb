import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import SearchStore from "../stores/SearchStore";
import SearchSystem from "../components/layout/SearchSystem";
import VFPagination from "../components/layout/VFPagination";


var apiRoot = '' + require('../scripts/Config.js');


export default class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.initFilters(),
      sorters: this.initSorters(),
      links:   this.initLinks(),
      path: "http://" + apiRoot,
      data:    {},
      };
  }

  componentWillMount() {
    SearchStore.on("change", () => {
      this.setState({
        data: SearchStore.getData(),
        links:SearchStore.getLinks(),
      })
    })
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

  handleSelect(type) {
    //TODO move this actions
    //this.requestQuery(this.state.links[type]);
    console.log(this.state.links[type]);
  }

  render() {
    const path = this.state.path;
    const data = SearchStore.getData();
    const links= SearchStore.getLinks();
    return (
      <div id="search-page" class="container-fluid">

        <SearchSystem
          width={2}
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
