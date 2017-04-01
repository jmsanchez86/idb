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
            console.log(data);
            _this.setState({isLoading: false, testData: data});
          });
        })
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  unitTestState() {
      if(this.state.testData)
        return (
            <div>
            <h4>{this.state.testData.errors.size == 0 ? "Success!\n" : "Failure.\n"}</h4>
            <p>{this.state.testData.output}</p>
            </div>
            );
      return (<div/>);
  }

  render() {
    let isLoading = this.state.isLoading;
    return (
      <div class="container">
        <Button
            bsStyle="primary"
            disabled={isLoading}
            onClick={!isLoading ? this.handleClick.bind(this) : null}>
            <p>{isLoading ? 'Loading...' : 'Run Unit Tests'}</p>
        </Button>
      {this.unitTestState.bind(this)} 
      </div>
    );
  }

  

}