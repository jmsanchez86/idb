import React from "react";
import { IndexLink, Link } from "react-router";

export default class FilterModule extends React.Component {
  getFilters() {
    const res = [];
    const filters = this.props.filters;
    for (var id in filters) {
      res.push(
        <div key={filters[id].id} class="checkbox">
          <label>
            <h5>
              <input
                id={id}
                onChange={this.onCheck.bind(this)}
                type="checkbox"
                value="" />
                {filters[id].name}
              </h5>
            </label>
        </div>
      );
    }
    return res;
  }
  onCheck(event) {
      this.props.onCheck(event);
  }
  render() {
    return (
      <div class="panel">
        <h5>Filter</h5>
        <div class="btn-group btn-group-justified" role="group" aria-label="...">
          {this.getFilters()}
        </div>
      </div>
    )
  }
};
