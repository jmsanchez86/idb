import React from "react";

export default class Settings extends React.Component {
  render() {
    console.log("settings");
    return (
      <div id="main-text" class="container">
        <div class="col-sm-8 col-sm-offset-2 text-center">
          <h2>Badges</h2>
          <img class="venn" src="../static/images/diagram.png" />
        </div>
      </div>
    );
  }
}
