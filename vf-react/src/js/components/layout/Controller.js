import React from "react";
import { IndexLink, Link } from "react-router";

export default class RecipeItem extends React.Component {
  sort_param_display(sort_params) {
    var display_list = [];
    for(var sort of sort_params) {
      display_list.push(<button key={sort.name} type="button" class="btn btn-default">{sort.name}</button>);
    }
    return display_list;
  }

  render() {
    //console.log(this.sort_param_display(this.props.sort_params));
    return (
      <div class="container-fluid">
        <div class="row panel">
          <div class="col-lg-3 col-md-3 pull-right">
            <div class="btn-group btn-group-justified" role="group" aria-label="...">

              <div class="btn-group" role="group">
                <button type="button" class="btn btn-default btn-md" data-toggle="modal" data-target="#myModal"><h5>Sort and Filter</h5></button>

                <div class="modal fade" id="myModal" role="dialog">
                  <div class="modal-dialog modal-md">
                    <div class="modal-content">

                      <div class="modal-body">
                        <h4>Sort by: <small>(select one)</small></h4>
                        <div class="btn-group btn-group-justified" role="group" aria-label="...">
                          {this.sort_param_display(this.props.sort_params)}
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
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
