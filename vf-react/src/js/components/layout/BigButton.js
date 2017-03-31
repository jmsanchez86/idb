
import React from "react";
import { IndexLink, Link } from "react-router";

export default class BigButton extends React.Component {
  render() {
    return (
      <button id="BigButton" type="button" class="btn btn-default btn-md round" data-toggle="modal" data-target="#myModal">
        <h5>
          Sort and Filter
        </h5>
      </button>

    )
  }
};
