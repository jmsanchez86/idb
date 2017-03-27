import React from "react";
import { IndexLink, Link } from "react-router";

export default class GroceryItemItem extends React.Component {
  getLink(id) {
    return "grocery-items/" + id;
  }
  render() {
    const groceryItem = this.props.groceryItem;
    const image = groceryItem.image;
    const name = groceryItem.name;
    const id = groceryItem.id;

    return (
      <div class="col-sm-6 col-md-4">
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
