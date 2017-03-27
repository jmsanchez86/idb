import React from "react";
import { IndexLink, Link } from "react-router";

export default class TagItem extends React.Component {
  getLink(id) {
    return "tags/" + id;
  }

  render() {
    const tag = this.props.tag;
    const image = tag.image;
    const name = tag.name;
    const id = tag.id;

    return (
      <div class="col-sm-6 col-md-4">
        <div class="thumbnail">
          <img src={image} />
          <div class="caption">
              <h3 class="grid">{name}</h3>
              <p><Link class="btn btn-primary" role="button" to={this.getLink(id)}>Details</Link></p>
          </div>
        </div>
      </div>
    );
  }
}
