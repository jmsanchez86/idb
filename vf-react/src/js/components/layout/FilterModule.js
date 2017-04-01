import React from "react";
import { IndexLink, Link } from "react-router";

export default class FilterModule extends React.Component {
  bar() {
    const bar = [];
    const filters = this.props.filters;
    for (var id in filters) {
      bar.push(
        <div key={filters[id].id} class="checkbox">
          <label><h5><input type="checkbox" value="" />{filters[id].name}</h5></label>
        </div>
      );
    }
    return bar;
  }
  render() {
    return (
      <div>
        <h5>Filter</h5>
        <div class="btn-group btn-group-justified" role="group" aria-label="...">
          {this.bar()}
        </div>
      </div>
    )
  }
};
