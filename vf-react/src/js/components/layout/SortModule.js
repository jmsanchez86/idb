import React from "react";
import { IndexLink, Link } from "react-router";
import { RadioGroup, Radio } from 'react-radio-group'

export default class SortModule extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedValue: "alpha"
    }
  }
  getRadioButtons() {
    const sorters = this.props.sorters;
    const buttons = [];
    for (var id in sorters) {
      var cls = "btn btn-default btn-block";
      if (id == this.state.selectedValue)
        cls = "btn btn-default btn-block active";
      buttons.push(
        <label key={id} class={cls}>
          <h5>{sorters[id].name}</h5>
          <Radio value={id} />
        </label>
      );
    }
    return buttons;
  }
  onRadio(event) {
    this.setState({selectedValue: event})
    this.props.onRadio(event);

  }
  render() {
    return (
        <RadioGroup name="fruit" selectedValue={this.state.selectedValue} onChange={this.onRadio.bind(this)}>
        <h5>Sort</h5>
        <div class="btn-list">
          {this.getRadioButtons()}
          </div>
        </RadioGroup>



    )
  }
};
