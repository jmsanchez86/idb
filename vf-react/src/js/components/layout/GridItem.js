  import React from "react";
import { IndexLink, Link } from "react-router";

export default class RecipeItem extends React.Component {
  getLink(id) {
    return this.props.path + "/" + id;
  }
  render() {
    const item  = this.props.item;
    const image = item.image;
    const name  = item.name;
    const blurb = item.blurb;
    var id = item.id;
    if (this.props.path == 'tags'){
      id = name;
    }

    return (

      <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3">
        <Link to={this.getLink(id)}>
        <div class="thumbnail">
          <div class="image">

              <img class="img img-responsive full-width thumb" src={image} />

          </div>

          <div class="caption">

              <h5 class="grid">
                {name.length > 50 ? name.substr(0,50) + "..." : name}
              </h5>
              <p>
                {blurb.length > 100 ? blurb.substr(0,100) + "..." : blurb}
              </p>

          </div>
        </div>
        </Link>
      </div>
    );
  }
}
