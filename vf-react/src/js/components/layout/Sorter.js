import React from "react";
import { IndexLink, Link } from "react-router";

export default class Sorter extends React.Component {
  getSortButtons() {
    const buttons = [];
    const sort_params = this.props.sort_params;
    var i = 0;
    for (var p of sort_params) {
      if (i++ == 0) {
        buttons.push(
          <label key={p.query} class="btn btn-sm btn-default active">
            <input type="radio"  name={p.query} autocomplete="off"  />
              <h5>{p.name}</h5>
          </label>
        );
      }
      else {
        buttons.push(
          <label key={p.query} class="btn btn-sm btn-default">
            <input type="radio" name={p.query} autocomplete="off"  />
              <h5>{p.name}</h5>
          </label>
        );
      }
    }
    return buttons;
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
