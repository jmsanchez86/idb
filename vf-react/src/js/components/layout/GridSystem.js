import React from "react";
import GridItem from "./GridItem";


export default class GridSystem extends React.Component {

  getGridItems(data, path) {
    const gridItems=[];
    var i = 0;
    const w = this.props.width;
    for (var id in data) {
      if (!(i++ % w)) {
        gridItems.push(<div key={"clear-"+i} class="clearfix"></div>);
      }
      gridItems.push(<GridItem key={id} path={path} item={data[id]} />);
    }
    return gridItems;
  }

  render() {
    return (
      <div class="container-fluid">
        <div class="row">
            {this.getGridItems(this.props.data, this.props.path)}
        </div>
      </div>
    );
  }
}
