import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems(data) {
    const searchItems=[];
    for (var id in data) {
      searchItems.push(<SearchItem key={id} path={"/" + data[id].pillar_name + "/" + id} item={data[id]} />);
    }
    return searchItems;
  }

  render() {
    return (
      <div class="container-fluid" id="grid-page">
        <ListGroup>
            {this.getSearchItems(this.props.data)}
        </ListGroup>
      </div>
    );
  }
}
