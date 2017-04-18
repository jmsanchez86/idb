import React from "react";
import { Link } from "react-router";

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

  handleSubmit(e) {
    if (!this.state.value.length) {
      e.preventDefault();
    }
    else {
      SearchActions.searchSubmit(this.state.value);
      this.setState({value: ""});
    }
  }

  getLink() {
    return "search" +  sanitizeString();
  }

  render() {
    return (
      <span id="NavSearch" class="form-group form-group-md col-lg-3 col-md-3 col-sm-6 pull-right">
        <form>
          <div class="input-group">
          <input
            class="search-query form-control"
            id="TextBox"
            placeholder="Search our site..."
            value={this.state.value}
            onChange={this.handleChange.bind(this)}
            />
            <span class="input-group-btn">
            <Link onClick={this.handleSubmit.bind(this)} to="search">
              <button
                disabled={!this.state.value.length}
                class="btn btn-md btn-default"
                id="SearchButton"
                type="submit button"
                value="Submit">
                <span class="glyphicon glyphicon-search">
                </span>
              </button>
              </Link>
            </span>
          </div>
        </form>
      </span>
    )
  }
};
