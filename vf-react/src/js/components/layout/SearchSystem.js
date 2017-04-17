import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems(data) {
    const searchItems=[];
    console.log(data);
    for (var id in data) { 
      console.log(id);
      searchItems.push(<SearchItem key={id} path={this.props.path +  "/" + data[id].pillar_name + "/" + id} item={data[id]} />);
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
