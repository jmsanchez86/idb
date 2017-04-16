  import React from "react";
import { IndexLink, Link } from "react-router";
import { ListGroup, ListGroupItem } from "react-bootstrap";

export default class SearchItem extends React.Component {
  getLink(item) {
    return item.pillar_name + "/" + item.id;
  }

  render() {
    const item  = this.props.item;
    const image = item.image;
    const name  = item.name;
    const id = item.id;


    return (
      <div>
      <ListGroupItem class="row">
        <Link to={this.getLink(item)}>
        <div class="thumbnail col-md-3 col-sm-6 col-xs-12">
          <div class="image">
              <img class="img img-rounded img-responsive thumb" src={image} />
          </div>
        </div>
        </Link>
        <div class="caption col-md-9 col-sm-6 col-xs-12">
          <Link to={this.getLink(id)}>
            <h5 id="search_item_name" class="search">
            {name && name.length > 50 ? name.substr(0,100) + "..." : name}
            </h5>
          </Link>
        </div>

      </ListGroupItem>
      </div>
    );
  }
}
