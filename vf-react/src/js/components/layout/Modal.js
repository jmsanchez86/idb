import React from "react";
import { IndexLink, Link } from "react-router";

import SortModule from "./SortModule";
import FilterModule from "./FilterModule";
import Apply from "./Apply";

export default class Modal extends React.Component {
  onApply() {
    this.props.onApply();
  }
  onCheck(event) {
    this.props.onCheck(event);
  }
onRadio(event) {
    this.props.onRadio(event);
  }
  render() {
    return (
      <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">


            <div class="modal-body">
              <button type="button" class="close" data-dismiss="modal">&times;</button>

              <SortModule
                onRadio={this.onRadio.bind(this)}
                sorters={this.props.sorters}
              />
              <FilterModule
                onCheck={this.onCheck.bind(this)}
                filters={this.props.filters}
              />
              <Apply
                onApply={this.onApply.bind(this)}
              />

            </div>

          </div>
        </div>
      </div>
    )
  }
};
