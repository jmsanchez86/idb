import React from "react";
import SearchItem from "./SearchItem";
import { ListGroup } from "react-bootstrap";

export default class SearchSystem extends React.Component {

  getSearchItems() {
    const searchItems=[];

    const and = this.props.data.and;
    if (and) {
      searchItems.push(
        <h5><center> AND Results </center> </h5>
      )
      for (var id in and) {
        const item = and[id];
        searchItems.push(<SearchItem key={id}
          path={"/" + item.pillar_name + "/" + item.id}
          item={item} />);
      }
    }
    const or = this.props.data.or;
    if (or) {
      searchItems.push(
        <h5><center>OR Results</center></h5>
      )
      for (var id in or) {
        const item = or[id];
        searchItems.push(<SearchItem key={id}
          path={"/" + item.pillar_name + "/" + item.id}
          item={item} />);
      }
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
