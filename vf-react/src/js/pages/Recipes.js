import React from "react";
import { IndexLink, Link } from "react-router";

import Greeting from "../components/layout/Greeting";
import GridItem from "../components/layout/GridItem";
import GridSystem from "../components/layout/GridSystem";

var data = require('json!../../data/food.json');
const recipes = data.recipes;


export default class Recipes extends React.Component {
  getGridItems() {
    const gridItems=[];
    for (var id in recipes) {
      gridItems.push(<GridItem key={id} cat="recipes" item={recipes[id]} />);
    }
    return gridItems;
  }

  render() {

    return (
      <div>
          <Greeting />
          <GridSystem path="recipes" data={recipes} />
      </div>

    );
  }
}
