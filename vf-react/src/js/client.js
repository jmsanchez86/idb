import React from "react";
import ReactDOM from "react-dom";
import { Router, Route, IndexRoute, hashHistory } from "react-router";

import About from "./pages/About";
import Badges from "./pages/Badges";
import GroceryItems from "./pages/GroceryItems";
import Ingredients from "./pages/Ingredients";
import Landing from "./pages/Landing";
import Recipes from "./pages/Recipes";

import Layout from "./pages/Layout";

const app = document.getElementById('app');

ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={Layout}>
      <IndexRoute component={Landing}></IndexRoute>

      <Route path="recipes(/:optional-params)" name="recipes" component={Recipes}></Route>
      <Route path="ingredients" name="ingredients" component={Ingredients}></Route>
      <Route path="grocery-items" name="grocery-items" component={GroceryItems}></Route>
      <Route path="badges" name="badges" component={Badges}></Route>

      <Route path="about" name="about" component={About}></Route>
    </Route>
  </Router>,
app);
