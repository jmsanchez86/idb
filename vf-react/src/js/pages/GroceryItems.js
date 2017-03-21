import React from "react";
import { IndexLink, Link } from "react-router";

var data = require('json!../../data/food.json');


export default class GroceryItems extends React.Component {
  render() {
    const groceryitems = data.grocery_items;


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
                <img src={groceryitems[1].image} />
                <div class="caption">
                    <h3>{groceryitems[1].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="grocery-items/1">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={groceryitems[2].image} />
                <div class="caption">
                    <h3>{groceryitems[2].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="grocery-items/2">Details</Link></p>
                </div>
              </div>
            </div>

            <div class="col-sm-6 col-md-4">
              <div class="thumbnail">
                <img src={groceryitems[3].image} />
                <div class="caption">
                    <h3>{groceryitems[3].name}</h3>
                    <p><Link class="btn btn-primary" role="button" to="grocery-items/2">Details</Link></p>
                </div>
              </div>
            </div>

          </div>
      </div>

    );
  }
}
