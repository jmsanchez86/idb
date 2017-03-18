import React from "react";

export default class Settings extends React.Component {
  constructor() {
    super();
    this.state = {
      gitDataUrl: 'https://api.github.com/repos/jmsanchez86/idb/stats/contributors',
      contributors: []
    };
  }

  // when the component loads
  componentDidMount() {
    var _this = this;
    fetch(this.state.gitDataUrl)  
      .then(  
        function(response) {  
          if (response.status !== 200) {  
            console.log('Looks like there was a problem. Status Code: ' +  
              response.status);  
            return;  
          }

          // Examine the text in the response  
          response.json().then(function(data) {  
            //console.log(data);
            // update our state for each contributor
            for(var i=0; i<data.length; ++i) {
              _this.setState(_this.state.contributors[i] = {
                  login: data[i].author.login,
                  picUrl: data[i].author.avatar_url,
                  totalCommits: data[i].total 
                });
            }  
          });  
        }  
      )  
      .catch(function(err) {  
        console.log('Fetch Error :-S', err);  
      });
  }

  render() {
    console.log("settings");
    return (
      <div id="main-text" class="container">
        <div class="col-sm-8 col-sm-offset-2 text-center">
          <h2>Meat the team</h2>
          <img class="venn" src="../static/images/diagram.png" />
        </div>
        <div id="grid-results" class="row">      
        {this.state.contributors.map(function(contributor) {
            return (
              <div key={contributor.login} className="contributor" class='col-sm-8 col-md-6'>
                <div class="thumbnail">
                  <img src={contributor.picUrl} />
                  <div class="caption">
                      <h3 href='contributor.profUrl'>{contributor.login}</h3>
                      <p>{contributor.totalCommits + ' '}
                        fridgetacular commit
                        {contributor.totalCommits > 1?'s':''}.</p>
                  </div>
                </div>
              </div>
            );
          })}
          </div>
      </div>
    );
  }
}
