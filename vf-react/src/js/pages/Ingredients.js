import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');

export default class Ingredients extends React.Component {

  render() {
    const ingredients = data.ingredients;

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
                <img src={ingredients[0].image} />
                <div class="caption">
                    <h3>{ingredients[0].name}</h3>
                    <p>{ingredients[0].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/0">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[1].image} />
                <div class="caption">
                    <h3>{ingredients[1].name}</h3>
                    <p>{ingredients[1].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/1">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[2].image} />
                <div class="caption">
                    <h3>{ingredients[2].name}</h3>
                    <p>{ingredients[2].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[3].image} />
                <div class="caption">
                    <h3>{ingredients[3].name}</h3>
                    <p>{ingredients[3].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[4].image} />
                <div class="caption">
                    <h3>{ingredients[4].name}</h3>
                    <p>{ingredients[4].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[5].image} />
                <div class="caption">
                    <h3>{ingredients[5].name}</h3>
                    <p>{ingredients[5].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[6].image} />
                <div class="caption">
                    <h3>{ingredients[6].name}</h3>
                    <p>{ingredients[6].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[7].image} />
                <div class="caption">
                    <h3>{ingredients[7].name}</h3>
                    <p>{ingredients[7].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={ingredients[8].image} />
                <div class="caption">
                    <h3>{ingredients[8].name}</h3>
                    <p>{ingredients[8].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
