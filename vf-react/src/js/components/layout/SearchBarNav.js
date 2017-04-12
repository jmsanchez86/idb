
import React from "react";
import { Link } from "react-router";


export default class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      terms: "",
    };
  }

  onClick(event) {
    console.log(this.refs.myText.value);
    console.log(this.refs.myText.placeholder);
    this.refs.myText.value="";
  }
  render() {
    return (
      <div id="NavSearch" class="form-group form-group-md pull-right col-lg-3 col-md-3 col-sm-6">
        <div  class="input-group">
          <p><input type="text" ref="myText" id="TextBox" class="search-query form-control" placeholder="Search" /></p>
          <span class="input-group-btn">
            <Link to="search">
            <button class="btn btn-md btn-default" type="button" onClick={this.onClick.bind(this)}>
              <span class=" glyphicon glyphicon-search"></span>
            </button>
            </Link>
          </span>
        </div>
      </div>
    )
  }
};
