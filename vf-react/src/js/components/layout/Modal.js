import React from "react";
import { IndexLink, Link } from "react-router";

import SortModule from "./SortModule";
import FilterModule from "./FilterModule";
import Apply from "./Apply";

export default class Modal extends React.Component {
  render() {
    return (
      <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">


            <div class="modal-body">
              <button type="button" class="close" data-dismiss="modal">&times;</button>

              <SortModule sort_params={this.props.sort_params} />
              <FilterModule filters={this.props.filters} />

            </div>

            <Apply onClick={this.props.onClick} />




          </div>
        </div>
      </div>
    )
  }
};
