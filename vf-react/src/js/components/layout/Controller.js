import React from "react";
import { IndexLink, Link } from "react-router";

export default class RecipeItem extends React.Component {

  render() {
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
                        <p>{this.props.sort_params[0].name}</p>
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
