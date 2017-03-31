import React from "react";
import { IndexLink, Link } from "react-router";

export default class RecipeItem extends React.Component {
  render() {
    const heading = this.props.heading ? this.props.heading : "Nom nom nom...";
    const msg = this.props.msg ? this.props.msg : "Let us help you help yourself to some tasty food.";

    return (
        <div class="container text-center">
          <h4>{heading}</h4>
          <img class="venn" src="../static/images/diagram.png" />
          <p>{msg}</p>
        </div>
    );
  }
}
