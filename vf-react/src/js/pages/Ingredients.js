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

          <div class="container">
            <div class="col-lg-1 dropdown">
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

            <div class="offset-2 col-lg-1 dropdown">
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
            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
                <div class="image">
                  <img class="img img-responsive full-width" src={ingredients[1].image} />
                </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[1].name}</h3>
                    <p>{ingredients[1].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/1">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[2].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[2].name}</h3>
                    <p>{ingredients[2].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[3].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[3].name}</h3>
                    <p>{ingredients[3].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/3">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[4].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[4].name}</h3>
                    <p>{ingredients[4].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/4">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[5].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[5].name}</h3>
                    <p>{ingredients[5].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/5">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[6].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[6].name}</h3>
                    <p>{ingredients[6].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/6">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[7].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[7].name}</h3>
                    <p>{ingredients[7].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/7">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[8].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[8].name}</h3>
                    <p>{ingredients[8].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/8">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
              <div class="thumbnail">
              <div class="image">
                <img class="img img-responsive full-width" src={ingredients[9].image} />
              </div>
                <div class="caption">
                    <h3 class="grid">{ingredients[9].name}</h3>
                    <p>{ingredients[9].blurb}</p>
                    <p><Link class="btn btn-primary" role="button" to="ingredients/9">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
