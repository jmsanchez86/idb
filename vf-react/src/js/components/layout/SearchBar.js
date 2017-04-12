
import React from "react";


export default class SearchBar extends React.Component {
  render() {
    return (
    <div class="form-group  form-group-lg col-lg-5 col-md-5 col-sm-6">
      <div  class="input-group">
        <p><input type="text" class="  search-query form-control" placeholder="Search" /></p>
        <span class="input-group-btn">
          <button class="btn btn-lg btn-default" type="button">
            <span class=" glyphicon glyphicon-search"></span>
          </button>
        </span>
      </div>
    </div>

    )
  }
};
