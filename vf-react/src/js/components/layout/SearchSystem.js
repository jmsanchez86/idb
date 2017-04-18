import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems() {
    const data = this.props.data.and;

    const searchItems=[];

    for (var id in data) {
      const item = data[id];
      searchItems.push(<SearchItem key={id}
        path={"/" + item.pillar_name + "/" + item.id}
        item={item} />);
    }
    return searchItems;
  }

  render() {
    return (
      <div class="container-fluid" id="SearchSystem">
        <ListGroup>
            {this.getSearchItems()}
        </ListGroup>
      </div>
    );
  }
}
