import React from "react";
import { IndexLink, Link } from "react-router";

import BigButton from "./BigButton";
import Modal from "./Modal";

export default class Controller extends React.Component {
  constructor() {
    super();
  }
  handleApply(event) {
    this.props.handleApply(this.props.filters,this.props.sorters);
  }
  handleRadio(event) {
    const id = event;
    const sorters = this.props.sorters;
    for (var i in sorters) {
      if (id == i) {
        sorters[i].checked = true;
      }
      else {
        sorters[i].checked = false;
      }
    }

  }
  handleCheck(event) {
    const id = event.target.id;
    const checked = event.target.checked;

    this.props.filters[id].checked = checked;
  }

  render() {
    return (
      <div class="container-fluid">
        <BigButton />
        <Modal
          sorters ={this.props.sorters}
          filters ={this.props.filters}
          onCheck ={this.handleCheck.bind(this)}
          onRadio ={this.handleRadio.bind(this)}
          onApply ={this.handleApply.bind(this)}
        />
      </div>
    )
  }
}
