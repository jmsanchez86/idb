import React from "react";

import Controller from "../components/layout/Controller";
import Greeting from "../components/layout/Greeting";
import * as SearchActions from "../actions/SearchActions"
import SearchStore from "../stores/SearchStore";
import SearchSystem from "../components/layout/SearchSystem";
import VFPagination from "../components/layout/VFPagination";

var apiRoot = '' + require('../scripts/Config.js');


export default class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      links:   this.initLinks(),
      data:    {},
      value:   ""
      };
  }

  componentWillMount() {
    SearchStore.on("change", () => {
      this.setState({
        value:SearchStore.getValue(),
        data: SearchStore.getData(),
        links:SearchStore.getLinks(),
      })
    })
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
    SearchActions.urlRequest(this.state.links[type]);
  }

  render() {
    const path = this.state.path;
    const data = SearchStore.getData();
    const links= SearchStore.getLinks();
    const value= SearchStore.getValue();
    return (
      <div id="search-page" class="container-fluid">
        <div id="SearchHeader">
          Search results for "{value}"
        </div>
        <SearchSystem
          data={data} />
        <VFPagination
          active={links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>
    );
  }
}
