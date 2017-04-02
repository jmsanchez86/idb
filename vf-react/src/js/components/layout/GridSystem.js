import React from "react";
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
      <div class="contatiner-fluid">
        <div class="row">
            {this.getGridItems(this.props.data, this.props.path)}
        </div>
      </div>

    );
  }
}
