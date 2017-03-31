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
      var cls = "btn btn-default";
      if (id == this.state.selectedValue)
        cls = "btn btn-default active";
      buttons.push(
        <label class={cls}>
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
        <div class="btn-group btn-group-justified">
          {this.getRadioButtons()}
          </div>
        </RadioGroup>



    )
  }
};
