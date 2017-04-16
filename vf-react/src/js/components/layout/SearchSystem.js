import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems(data, path) {
    const searchItems=[];
    var i = 0;
    const w = this.props.width;
    for (var id in data) {
      if (!(i++ % w)) {
        searchItems.push(<div key={"clear-"+i} class="clearfix"></div>);
      }
      searchItems.push(<SearchItem key={id} path={path} item={data[id]} />);
    }
    return searchItems;
  }

  render() {
    return (
      <div class="container-fluid" id="grid-page">
        <ListGroup>
            {this.getSearchItems(this.props.data, this.props.path)}
        </ListGroup>
      </div>
    );
  }
}
