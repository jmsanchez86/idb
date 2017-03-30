import React from "react";
import { IndexLink, Link } from "react-router";


import BigButton from "./BigButton";
import Modal from "./Modal";

export default class Controller extends React.Component {

  handleClick() {
    this.props.updateList(this.props.filters);
  }

  handleSubmit() {
    console.log("SUBMIT");
  }

  render() {
    return (
      <div class="container-fluid">
        <BigButton />
        <Modal sort_params={this.props.sort_params} filters={this.props.filters} onClick={this.handleSubmit.bind(this)} />
      </div>
    )
  }
}
