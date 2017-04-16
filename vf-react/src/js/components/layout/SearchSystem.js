import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";


export default class SearchSystem extends React.Component {

  getSearchItems() {
    const data = this.props.data;
    const path = this.props.path;
    const searchItems=[];
    var i = 0;
    const w = this.props.width;
    console.log(data);
    for (var id in data) {
      console.log(id);
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
            {this.getSearchItems()}
        </ListGroup>
      </div>
    );
  }
}
