import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";


export default class SearchSystem extends React.Component {

  getSearchItems() {
    const data = this.props.data;
    const path = this.props.path;
    const searchItems=[];
    console.log(data);
    for (var id in data) {
      const item = data[id];
      searchItems.push(<SearchItem
                          key={item.id + id}
                          path={path}
                          item={item} />);
    }
    return searchItems;
  }

  render() {
    return (
      <div class="container-fluid" id="grid-page">
        <ListGroup>
            {this.getSearchItems()}
        </ListGroup>
      </div>
    );
  }
}
