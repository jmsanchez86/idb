import React from "react";
import { IndexLink, Link } from "react-router";
import { ListGroup, ListGroupItem } from "react-bootstrap";

export default class SearchItem extends React.Component {
  getContexts(contexts) {
    const context_html_list = [];
    for (var c of contexts) {
      context_html_list.push((<p key={c} class="search-c">... <span dangerouslySetInnerHTML={{__html: c}} /> ...</p>))
    }
    return context_html_list;
  }
  render() {
    const item = this.props.item;
    const path = this.props.path;
    const image = item.image;
    const name  = item.name;
    
    var id = item.id;

    return (
      <div>
      <Link to={path}>
      <ListGroupItem class="row search-result">
        
        <div class="col-md-3 col-sm-6 col-xs-12">
          <div class="image">
              <img class="img img-rounded img-responsive thumb" src={image} />
          </div>
        </div>
        <div class="caption col-md-9 col-sm-6 col-xs-12">

            <h4 id="search_item_name" class="search">
            {name && name.length > 50 ? name.substr(0,100) + "..." : name}
            </h4>
             
            {this.getContexts(item.contexts)}

        </div>
        
      </ListGroupItem>
      </Link>
      </div>
    );
  }
}
