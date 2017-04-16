
import React from "react";
import { Link } from "react-router";

import SearchStore from "../../stores/SearchStore";
import * as SearchActions from "../../actions/SearchActions"

export default class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "",
      terms: "",
    };
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    SearchActions.searchSubmit(this.state.value);
    event.preventDefault();
    this.setState({value: ""});
  }

  sanitizeString() {
    return this.state.raw.replace(/[^\w\s]/gi, '').trim().replace(/ +/gi, '+').toLowerCase();
  }

  render() {
    return (
      <span id="NavSearch" class="form-group form-group-md col-lg-3 col-md-3 col-sm-6 pull-right">
        <form onSubmit={this.handleSubmit.bind(this)}>
          <div class="input-group">
          <input
            class="search-query form-control"
            id="TextBox"
            placeholder="Search our site..."
            value={this.state.value}
            onChange={this.handleChange.bind(this)}
            />
            <span class="input-group-btn">
              <button
                class="btn btn-md btn-default"
                id="SearchButton"
                type="submit button"
                value="Submit">
                <span class="glyphicon glyphicon-search"></span>
              </button>
            </span>
          </div>
        </form>
      </span>
    )
  }
};
