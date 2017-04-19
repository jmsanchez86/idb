import React from "react";
import Link from "react-router";

import Controller from "../components/layout/Controller";
import Landing from "./Landing";
import Greeting from "../components/layout/Greeting";
import * as SearchActions from "../actions/SearchActions"
import SearchStore from "../stores/SearchStore";
import SearchSystem from "../components/layout/SearchSystem";
import VFPagination from "../components/layout/VFPagination";

export default class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      links:   this.initLinks(),
      data:    {},
      value:   "",
      valid: false,
      };
  }

  componentDidMount() {
    SearchStore.on("change", () => {
      this.setState({
        value:SearchStore.getValue(),
        data: SearchStore.getData(),
        links:SearchStore.getLinks(),
        valid: true,
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
    SearchActions.urlRequest(this.state.links[type]);
  }

  baconEgg() {
    SearchActions.searchSubmit("bacon");
  }

  render() {
    const path = this.state.path;
    const data = SearchStore.getData();
    const links= SearchStore.getLinks();
    const value= SearchStore.getValue();
    const results = SearchStore.getNumResults();


    window.scrollTo(0, 0);

    if (this.state.valid) {
      return (
          <div id="search-page" class="container-fluid">
          {results ?
          <VFPagination
            active={links.active}
            onSelect={this.handleSelect.bind(this)}
            links={links} />
            :
            <div>
            </div>}

          <div id="SearchHeader">
            {results} search results for "{value}"
          </div>

          <SearchSystem
            data={data} />

          {results ?
          <VFPagination
            active={links.active}
            onSelect={this.handleSelect.bind(this)}
            links={links} />
          :
          <div id="SearchHeader">
            <center>
              Did you mean "<a href="#/search" onClick={this.baconEgg.bind(this)}>bacon</a>"?
            </center>
          </div>}
        </div>
        );
      }
      else {
        return (
          <Landing />
        );
      }
  }
}
