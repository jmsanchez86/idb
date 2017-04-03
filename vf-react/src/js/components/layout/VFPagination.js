import React from "react";
import { Pager } from 'react-bootstrap';

import GridItem from "./GridItem";


export default class VFPagination extends React.Component {
  onFirst() {
    this.props.onSelect("first");
  }
  onPrev() {
    this.props.onSelect("prev");
  }
  onLast() {
    this.props.onSelect("last");
  }
  onNext() {
    this.props.onSelect("next");
  }
  render() {
    return (

          <Pager id="pagination" >
            <Pager.Item disabled={!this.props.links['first']} previous onSelect={this.onFirst.bind(this)}>&lt;&lt;</Pager.Item>
            <Pager.Item disabled={!this.props.links['prev']} previous onSelect={this.onPrev.bind(this)}>&lt;</Pager.Item>
            <Pager.Item disabled={!this.props.links['last']} next onSelect={this.onLast.bind(this)}>&gt;&gt;</Pager.Item>
            <Pager.Item disabled={!this.props.links['next']} next onSelect={this.onNext.bind(this)}>&gt;</Pager.Item>
            <Pager.Item disabled>{this.props.active}</Pager.Item>
          </Pager>

    );
  }
}
