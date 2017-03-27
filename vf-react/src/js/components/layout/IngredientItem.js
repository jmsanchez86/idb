import React from "react";
import { IndexLink, Link } from "react-router";

export default class IngredientItem extends React.Component {
  getLink(id) {
    return "ingredients/" + id;
  }
  render() {
    const ingredient = this.props.ingredient;
    const image = ingredient.image;
    const name = ingredient.name;
    const id = ingredient.id;

    return (
      <div class="col-lg-4 col-sm-6 col-xs-12 col-md-4">
        <div class="thumbnail">
          <div class="image">
            <img class="img img-responsive full-width" src={image} />
          </div>
          <div class="caption">
              <h3 class="grid">{name}</h3>
              <p><Link class="btn btn-primary" role="button" to={this.getLink(id)}>Details</Link></p>
          </div>
        </div>
      </div>
    );
  }
}
