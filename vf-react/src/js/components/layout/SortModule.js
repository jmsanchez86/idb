import React from "react";
import { IndexLink, Link } from "react-router";

export default class SortModule extends React.Component {
  getSortButtons() {
    const bar = [];
    const sorters = this.props.sorters;
    var i = 0;
    for (var p of sorters) {
      if (i++ == 0) {
        bar.push(
          <label key={p.query} class="btn btn-sm btn-default active">
            <input type="radio"  name={p.query} autocomplete="off"  />
              <h5>{p.name}</h5>
          </label>
        );
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
