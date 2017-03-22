import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');

export default class Tags extends React.Component {
  getName(name) {
    return "http://placehold.it/500?text=" + name;
  }
  render() {
    const tags = data["tags"];


    return (
      <div id="unique-content">
          <div class="container">
            <div class="col-sm-8 col-sm-offset-2 text-center">
              <h4>Nom nom nom...</h4>
              <img class="venn" src="../static/images/diagram.png" />
              <p>Let us help you help yourself to some tasty food.</p>
            </div>
          </div>

          <div id="grid-results" class="row">

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={tags[1].image} />
                <div class="caption">
                    <h3>{tags[1].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="tags/1">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={tags[2].image} />
                <div class="caption">
                    <h3>{tags[2].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="tags/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={tags[3].image} />
                <div class="caption">
                    <h3>{tags[3].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="tags/3">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
