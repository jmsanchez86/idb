import React from "react";
import { IndexLink, Link } from "react-router";

export default class BigButton extends React.Component {
  render() {
    return (
      <div class="row panel">
        <div class="col-lg-3 col-md-3 pull-right">

          <div class="btn-group btn-group-justified" role="group" aria-label="...">
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-default btn-md round" data-toggle="modal" data-target="#myModal">
                <h5>
                  Sort and Filter
                </h5>
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
};
