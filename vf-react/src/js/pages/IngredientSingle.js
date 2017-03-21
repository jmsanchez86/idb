import React from "react";

var data = require('json!../../data/food.json');
const ingredients = data.ingredients;


export default class IngredientSingle extends React.Component {
  render() {
    const id = this.props.params.id;
    return (
      <div id="unique-content">

          <div class="container">
            <div class="col-sm-8 col-sm-offset-2 text-center">
              <h2>Ingredient: {id}</h2>
              <h4>Nom nom nom...</h4>
              <img class="venn" src="../static/images/diagram.png" />
              <p>Let us help you help yourself to some tasty food.</p>
            </div>
          </div>


      </div>

    );
  }
}
