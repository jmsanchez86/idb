import React from "react";
import { IndexLink, Link } from "react-router";

export default class RecipeItem extends React.Component {
  getLink(id) {
    return "recipes/" + id;
  }
  render() {
    console.log(this.props.recipes);
    const recipe = this.props.recipe;
    const image = recipe.image;
    const name = recipe.name;
    const blurb = recipe.blurb;
    const id = recipe.id;

    return (

      <div class="col-sm-6 col-md-4">
        <div class="thumbnail">
          <div class="image">
            <img class="img img-responsive full-width" src={recipe.image} />
          </div>
          <div class="caption">
              <h3 class="grid">{recipe.name}</h3>
              <p>{recipe.blurb}</p>
              <p><Link class="btn btn-primary" role="button" to={this.getLink(id)}>Details</Link></p>
          </div>
        </div>
      </div>
    );
  }
}
