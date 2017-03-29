import React from "react";
import { IndexLink, Link } from "react-router";

export default class Controller extends React.Component {
  getSortButtons() {
    const bar = [];
    const sort_params = this.props.sort_params;
    var i = 0;
    for (var p of sort_params) {
      if (i++ == 0) {
        bar.push(
          <label key={p.query} class="btn  btn-sm btn-default active">
            <input type="radio" name="options" id="option2" autocomplete="off"  />
            <div class="row">
              <h5>{p.name}</h5>
            </div>
          </label>
        );
      }
      else {
        bar.push(
          <label key={p.query} class="btn  btn-sm btn-default">
            <input type="radio" name="options" id="option2" autocomplete="off"  />
            <div class="row">
              <h5>{p.name}</h5>
            </div>
          </label>
        );
      }
    }
    return bar;
  }
  bar() {
    const bar = [];
    const filters = this.props.filters;
    for (var id in filters) {
      bar.push(
        <div key={filters[id].id} class="checkbox">
          <label><h5><input type="checkbox" value="" />{filters[id].name}</h5></label>
        </div>
      );
    }
    return bar;
  }

  handleClick() {
    this.props.updateList(this.props.filters);
  }

  render() {
    return (
      <div class="container-fluid">
        <div class="row panel">
          <div class="col-lg-3 col-md-3 pull-right">
            <div class="btn-group btn-group-justified" role="group" aria-label="...">

              <div class="btn-group" role="group">
                <button type="button" class="btn btn-default btn-md round" data-toggle="modal" data-target="#myModal"><h5>Sort and Filter</h5></button>
              </div>
            </div>

                <div class="modal fade" id="myModal" role="dialog">
                  <div class="modal-dialog modal-sm">
                    <div class="modal-content">

                      <div class="modal-body">

                        <button type="button" class="close" data-dismiss="modal">&times;</button>

                        <h5>Sort</h5>
                        <div class="btn-group btn-group-justified" data-toggle="buttons" role="group" aria-label="...">
                          {this.getSortButtons()}



                        </div>

                        <h5>Filter</h5>
                        <div class="btn-group btn-group-justified" role="group" aria-label="...">
                          {this.bar()}
                        </div>



                      <div class="modal-footer">
                        <div class="btn-group btn-group-justified" role="group" aria-label="...">
                          <div class="btn-group" role="group">
                            <button type="button"  onClick={this.handleClick.bind(this)} data-dismiss="modal" class="btn btn-lg btn-success"><h5>Apply</h5></button>
                          </div>

                        </div>
                      </div>



                    </div>
                  </div>
                </div>

          </div>
        </div>


      </div>
      </div>
    )
  }
}
