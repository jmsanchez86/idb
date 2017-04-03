import React from "react";
import { Link } from "react-router";

import Footer from "../components/layout/Footer";
import Nav from "../components/layout/Nav";

export default class Layout extends React.Component {
  render() {
    /* Location gives us info about which route we've gone through */
    const { location } = this.props;


    return (
      <div >
        <Nav location={location} />
        <div class="container-fluid">
              {this.props.children}
        </div>
        <Footer/>
      </div>

    );
  }
}
