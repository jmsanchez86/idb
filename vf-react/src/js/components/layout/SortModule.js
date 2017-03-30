import React from "react";
import { IndexLink, Link } from "react-router";

export default class SortModule extends React.Component {
  getSortButtons() {
    const bar = [];
    const sort_params = this.props.sort_params;
    var i = 0;
    for (var p of sort_params) {
      if (i++ == 0) {
        bar.push(
          <label key={p.query} class="btn btn-sm btn-default active">
            <input type="radio"  name={p.query} autocomplete="off"  />
              <h5>{p.name}</h5>
          </label>
        );
        console.log(bar);
      }
      else {
        bar.push(
          <label key={p.query} class="btn btn-sm btn-default">
            <input type="radio" name={p.query} autocomplete="off"  />
              <h5>{p.name}</h5>
          </label>
        );
      }
    }
    return bar;
  }
  render() {
    return (
      <div>
        <h5>Sort</h5>
        <div class="btn-group btn-group-justified" data-toggle="buttons" role="group" aria-label="...">
          {this.getSortButtons()}
        </div>
      </div>
    )
  }
};
