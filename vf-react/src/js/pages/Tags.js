import React from "react";
import { IndexLink, Link } from "react-router";

import Greeting from "../components/layout/Greeting";
import GridSystem from "../components/layout/GridSystem";

const data = require('json!../../data/food.json');
const tags = data.tags;

export default class Tags extends React.Component {
  getGridItems() {
    const gridItems=[];
    for (var id in tags) {
      gridItems.push(<GridItem key={id} path="tags" item={tags[id]} />);
    }
    return gridItems;
  }
  render() {
    return (
      <div>
        <Greeting />
        <GridSystem path="tags" data={tags} />
      </div>

    );
  }
}
