import React from "react";
import { IndexLink, Link } from "react-router";


import BigButton from "./BigButton";
import Modal from "./Modal";

export default class Controller extends React.Component {
  constructor() {
    super();
    this.state = {
      filters: {},
      sorters: {},
    };
  }
  handleApply(event) {
    this.props.handleApply(this.state.filters);

  }
  handleRadio(event) {
    console.log("Radio");
  }
  handleCheck(event) {
    const id = event.target.id;
    const checked = event.target.checked;

    this.state.filters[id] = checked;
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
