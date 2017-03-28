import React from "react";
import { IndexLink, Link } from "react-router";

import Greeting from "../components/layout/Greeting";
import GridItem from "../components/layout/GridItem";

var data = require('json!../../data/food.json');
const ingredients = data.ingredients;


export default class Ingredients extends React.Component {
  getGridItems() {
    const gridItems=[];
    for (var id in ingredients) {
      gridItems.push(<GridItem key={id} path="ingredients" item={ingredients[id]} />);
    }
    return gridItems;
  }

  render() {
    return (
      <div>
      <Greeting />
      <div>
        {this.getGridItems()}
      </div>
      </div>

    );
  }
}
