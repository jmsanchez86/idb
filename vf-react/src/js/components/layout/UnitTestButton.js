import React from "react";
import { Button } from 'react-bootstrap';


export default class UnitTestButton extends React.Component {
  constructor() {
      super();
      this.state = {
          isLoading: false
      };
  }

  handleClick() {
    this.setState({isLoading: true});

    // call our api to get test results
    var _this = this;
    fetch(this.props.api_endpoint + 'test')
      .then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem loading test info from the vennfridge api (' +
              _this.props.api_endpoint + '/test). Status Code: ' +
              response.status);
            return;
          }

          // Examine the text in the response
          response.json().then(function(data) {
            //console.log(data);
            _this.setState({isLoading: false, testData: data});
          });
        })
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
      this.forceUpdate();
  }

  listTestData(toList) {
    const listItems = [];
    for(var item in this.state.testData[toList]) {
      listItems.push(<li key={item} class="list-group-item">{this.state.testData[toList][item]}</li>);
    }
    return listItems;
  }

  unitTestState() {
      if(this.state.testData)
        return (
            <div class="container thumbnail">
            <h4>{this.state.testData.successes.length == this.state.testData.total_tests ? "Success!" : "Failure."}</h4>
            <p>{this.state.testData.output}</p>
            <h6>{this.state.testData.successes.length == 0 ? '' : 'Successes:'}</h6>
            <ul class="successes list-group">{this.listTestData('successes')}</ul>
            <h6>{this.state.testData.failures.length == 0 ? '' : 'Failures:'}</h6>
            <ul class="failures list-group">{this.listTestData('failures')}</ul>
            <p><span class="badge active">{this.state.testData.total_tests}</span>
                {' '}total unit tests.
            </p>
            </div>
            );
      return (<div/>);
  }

  render() {
    let isLoading = this.state.isLoading;
    console.log(this.state.testData);
    return (
      <div>
        <Button
            bsStyle="primary"
            disabled={isLoading}
            onClick={!isLoading ? this.handleClick.bind(this) : null}>
            <p>{isLoading ? 'Loading...' : 'Run Unit Tests'}</p>
        </Button>
      {this.unitTestState()}
      </div>
    );
  }



}
