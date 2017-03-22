import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');
const recipes = data.recipes;


export default class Recipes extends React.Component {
  render() {
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
                <div class="image">
                  <img class="img img-responsive full-width" src={recipes[1].image} />
                </div>
                <div class="caption">
                    <h3>{recipes[1].name}</h3>
                    <p>{recipes[1].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="recipes/1">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <div class="image">
                  <img class="img img-responsive full-width" src={recipes[2].image} />
                </div>
                <div class="caption">
                    <h3>{recipes[2].name}</h3>
                    <p>{recipes[2].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="recipes/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <div class="image">
                  <img class="img img-responsive full-width" src={recipes[3].image} />
                </div>
                <div class="caption">
                    <h3>{recipes[3].name}</h3>
                    <p>{recipes[3].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="recipes/3">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
