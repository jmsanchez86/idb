import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems() {
    const data = this.props.data;

    const searchItems=[];
    console.log(data);
    for (var id in data) {
      const item = data[id];
      searchItems.push(<SearchItem
                          key={item.id + "_" + id}
                          path={item.pillar_name+"/"+item.id}
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
