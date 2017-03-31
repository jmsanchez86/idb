import React from "react";
import { Link } from "react-router";

import Footer from "../components/layout/Footer";
import Nav from "../components/layout/Nav";

export default class Layout extends React.Component {
  render() {
    /* Location gives us info about which route we've gone through */
    const { location } = this.props;
    const containerStyle = {
      /* push content down so it won't be covered by navbar */
      marginTop: "40px"
    };

    return (
      <div >
        <Nav location={location} />

        <div class="container-fluid" style={containerStyle}>
          <div class="row">

              {this.props.children}

          </div>
          <Footer/>
        </div>
      </div>

    );
  }
}
