import React from "react";
import { IndexLink, Link } from "react-router";
import { ListGroup, ListGroupItem } from "react-bootstrap";

export default class SearchItem extends React.Component {
  getLink(id) {
    return this.props.path;
  }

  render() {
    const item    = this.props.item;
    const image   = item.image;
    const name    = item.name;
    const context = item.contexts;

    var id = item.id;

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

            <h4 id="search_item_name" class="search">
            {name && name.length > 50 ? name.substr(0,100) + "..." : name}
            </h4>

              <p dangerouslySetInnerHTML={{__html: context}} />


        </div>

      </ListGroupItem>
      </div>
    );
  }
}
