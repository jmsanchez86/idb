import React from "react";
import { IndexLink, Link } from "react-router";

export default class Apply extends React.Component {

  render() {
    return (
      <div class="modal-footer">
        <div class="btn-group btn-group-justified" role="group" aria-label="...">
          <div class="btn-group" role="group">
            <button onClick={this.props.onClick} data-dismiss="modal" class="btn btn-lg btn-success">
              Apply
            </button>
          </div>
        </div>
      </div>
    )
  }
};
