import React from "react";
import { IndexLink, Link } from "react-router";

export default class Nav extends React.Component {
  constructor() {
    super()
    this.state = {
      collapsed: true,
    };
  }

  toggleCollapse() {
    const collapsed = !this.state.collapsed;
    this.setState({collapsed});
  }

  render() {
    const { location } = this.props;
    const { collapsed } = this.state;

    const navClass = collapsed ? "collapse" : "";

    return (
 /* NEW */

      <nav class="navbar navbar-default">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" onClick={this.toggleCollapse.bind(this)}>
              <span class="sr-only">Toggle navigation</span>
              <span class="glyphicon glyphicon-cutlery"></span>
            </button>
            <IndexLink id="logohome" class="navbar-brand" to="/" onClick={this.toggleCollapse.bind(this)}>venn fridge</IndexLink>
          </div>
          <div class={"navbar-collapse " + navClass} id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
              <li activeClassName="active">
                <Link to="ingredients" onClick={this.toggleCollapse.bind(this)}>Ingredients</Link>
              </li>
              <li activeClassName="active">
                <Link to="recipes" onClick={this.toggleCollapse.bind(this)}>Recipes</Link>
              </li>
              <li activeClassName="active">
                <Link to="grocery-items" onClick={this.toggleCollapse.bind(this)}>Grocery Items</Link>
              </li>
              <li activeClassName="active">
                <Link to="badges" onClick={this.toggleCollapse.bind(this)}>Badges</Link>
              </li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
            <li activeClassName="active">
              <Link to="about" onClick={this.toggleCollapse.bind(this)}>About Us</Link>
            </li>
            </ul>
          </div>
        </div>
      </nav>
    );
  }
}
