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
      links:   this.initLinks(),
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
          data={data} />
        <VFPagination
          active={this.state.links.active}
          onSelect={this.handleSelect.bind(this)}
          links={links} />
      </div>
    );
  }
}
