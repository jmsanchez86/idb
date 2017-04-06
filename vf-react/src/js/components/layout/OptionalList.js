
import React from "react";


export default class OptionalList extends React.Component {
  getResponse(empty) {
    if (empty) {
      return (
        <p>{this.props.msg ? this.props.msg : "Sorry, we found nothing."}</p>
      );
    }
    else {
      return this.props.list;
    }

  }
  render() {
    const title = this.props.title;
    const empty = !this.props.list.length;
    console.log(this.props.list);

    return (
      <div>
        <div class="row">
          <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
            <h3 disabled={empty}>{title}</h3>
          </div>
        </div>
        <div class="row">
          <div  disabled={empty} class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
            {this.getResponse(empty)}
          </div>
        </div>
      </div>
    );
  }
}
