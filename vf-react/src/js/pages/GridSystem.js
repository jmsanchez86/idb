import React from "react";
import { IndexLink, Link } from "react-router";

import GridItem from "./GridItem";


export default class GridSystem extends React.Component {

  getGridItems(data, path) {
    const gridItems=[];
    for (var id in data) {
      gridItems.push(<GridItem key={id} path={path} item={data[id]} />);
    }
    return gridItems;
  }

  render() {
    return (
        <div id="grid" class="contatiner">
          {this.getGridItems(this.props.data, this.props.path)}
        </div>

    );
  }
}
