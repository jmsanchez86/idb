import React from "react";

import UnitTestButton from "../components/layout/UnitTestButton";

var teamData = require('json!../../../../app/static/data/team-info.json');
var tech_doc = '' + require('../scripts/tech-doc.js'); // pulls in tech doc as md string

var showdown  = require('showdown'),
    converter = new showdown.Converter(),
    html      = converter.makeHtml(tech_doc); // converts markdown to html

export default class About extends React.Component {
  constructor() {
    super();
    this.state = {
      gitDataUrl: 'https://api.github.com/repos/jmsanchez86/idb/stats/contributors',
      gitIssuesUrl: 'https://api.github.com/repos/jmsanchez86/idb/issues',
      api_endpoint: 'http://api.vennfridge.appspot.com/',
      contributors: new Map(),
      totalIssues: 0,
      totalCommits: 0,
      totalUnitTests: 0,
    };
  }
  getTotals(attributeToTotal) {
    var total = 0;
    for (var[name, cont] of this.state.contributors) {
      total = total + cont[attributeToTotal];
    }
    this.state[attributeToTotal] = total;
    this.forceUpdate();
  }
  // when the component loads
  componentDidMount() {
    // update our state for each contributor
    for(var i=0; i<teamData.length; ++i) {
      this.state.contributors.set(teamData[i].username,
      {
            name: teamData[i].name,
            bio: teamData[i].bio,
            picUrl: teamData[i].imgUrl,
            responsibilities: teamData[i].responsibilities,
            totalUnitTests: teamData[i].numberOfUnitTests,
            totalIssues:0
      });
          
    }
    var _this = this;
    
    fetch(this.state.gitDataUrl)
      .then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem loading github info. Status Code: ' +
              response.status);
            return;
          }
        
          // Examine the text in the response
          response.json().then(function(data) {
            for(var i=0; i<data.length; ++i) {
              // update our github state for each contributor
              const contributor = _this.state.contributors.get(data[i].author.login);
              if(contributor){
                  var gitContr = {
                    login: data[i].author.login,
                    gitPicUrl: data[i].author.avatar_url,
                    totalCommits: data[i].total,
                    profUrl: data[i].author.html_url
                  };
                  
                  for (var attrname in gitContr)
                    { contributor[attrname] = gitContr[attrname]; }
              }
              
            }
            var cont = _this.state.contributors;
            cont.get('scottnm').totalIssues = 32;
            cont.get('CoryDunn').totalIssues = 1;
            cont.get('jmsanchez86').totalIssues = 0;
            cont.get('ndbenzinger').totalIssues = 1;
            cont.get('scott-hornberger').totalIssues = 5;
            cont.get('thomascardwell7').totalIssues = 21;
            _this.getTotals("totalIssues");
            _this.getTotals("totalCommits");
            _this.getTotals("totalUnitTests");
            
            _this.forceUpdate();
          });
        })
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
      
    // this will force an update before rendering
    this.forceUpdate();
  }

  render() {
    var r = Array.from(this.state.contributors, (contributor) => contributor);
    var contrList = r.map(function(c){
      const contributor = c[1];
      return (
        <div key={contributor.name} className='contributor' class='list-group-item container'>
          <div class="thumbnail col-sm-4">
            <img src={contributor.picUrl ? contributor.picUrl : contributor.gitPicUrl} />
            <div class="caption">
              <h4>{contributor.name + ' '}
                <small><a href={contributor.profUrl}>{contributor.login}</a></small>
              </h4>
              <p><span class="badge active">{contributor.totalCommits}</span>
                {' '}fridgetacular commit
                {contributor.totalCommits > 1 || contributor.totalIssues == 0?'s':''}.
              </p>
              <p><span class="badge active">{contributor.totalIssues}</span>
                {' '}fridgetacular issue
                {contributor.totalIssues > 1 || contributor.totalIssues == 0?'s':''}.
              </p>
              <p>
                <span class="badge active">{contributor.totalUnitTests}</span>
                {' '}contributed unit test
                {contributor.totalUnitTests > 1 || contributor.totalUnitTests == 0?'s':''}.
              </p>
            </div>
          </div>
          <div class='col-md-6'>
            <h4>{contributor.bio ? 'Bio' : ''}</h4>
            <p>{contributor.bio}</p>
            <h4>{contributor.responsibilities ? 'Responsibilities' : ''}</h4>
            <p>{contributor.responsibilities}</p>

          </div>
        </div>);});

    return (
      <div id="unique-content">

        <div class="container">
          <div class="col-sm-8 col-sm-offset-2 text-center">
            <h2>Meat the team</h2>
            <img class="venn" src="../static/images/diagram.png" />
          </div>
        </div>
        
        <div id="contributor-list" class="list-group container">
          {contrList}
        </div>
        <div class="container">
          <h4>Useful Links!</h4>
          <h6><a href="https://github.com/jmsanchez86/idb">GitHub Repo</a></h6>
          <p><span class="badge active">{this.state.totalCommits}</span>
                {' '}total commits.
          </p>
          <h6><a href="https://github.com/jmsanchez86/idb/issues">Issue Tracker</a></h6>
          <p><span class="badge active">{this.state.totalIssues}</span>
                {' '}total issues.
          </p>
          <p><span class="badge active">{this.state.totalUnitTests}</span>
                {' '}total unit tests.
          </p>
          <UnitTestButton api_endpoint={this.state.api_endpoint}/>
          <h6><a href="http://docs.vennfridge.apiary.io/#">Apiary API</a></h6>
        </div>
        <div class="container" dangerouslySetInnerHTML={{__html: html}} />
      </div>
    );
  }
}
