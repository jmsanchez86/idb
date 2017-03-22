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

          <div class="container">
            <div class="offset-1 col-lg-1 dropdown">
            <button class="btn btn-sm btn-primary dropdown-toggle" type="button" data-toggle="dropdown">
              Sort Results
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
              <li><a href="#">A-Z</a></li>
              <li><a href="#">Z-A</a></li>
              <li><a href="#">Most Popular</a></li>
            </ul>
            </div>

            <div class="offset-1 col-lg-1 dropdown">
            <button class="btn btn-sm btn-primary dropdown-toggle" type="button" data-toggle="dropdown">
              Filter
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
              <li><a href="#">Crowd Pleaser</a></li>
              <li><a href="#">Vegetarian</a></li>
              <li><a href="#">Great For Sandwiches</a></li>
              <li><a href="#">Quick!</a></li>
            </ul>
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
            
            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={tags[4].image} />
                <div class="caption">
                    <h3>{tags[4].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="tags/4">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
