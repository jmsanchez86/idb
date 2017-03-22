import React from "react";

var teamData = require('json!../../../../app/static/data/team-info.json');

export default class About extends React.Component {
  constructor() {
    super();
    this.state = {
      gitDataUrl: 'https://api.github.com/repos/jmsanchez86/idb/stats/contributors',
      contributors: new Map(),
    };
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
            numberOfUnitTests: teamData[i].numberOfUnitTests
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
              // update our state for each contributor
              const contributor = _this.state.contributors.get(data[i].author.login);
              if(contributor){
                  var gitContr = {
                    login: data[i].author.login,
                    gitPicUrl: data[i].author.avatar_url,
                    totalCommits: data[i].total,
                    profUrl: data[i].author.html_url
                  };
              }
              for (var attrname in gitContr)
                { contributor[attrname] = gitContr[attrname]; }
            }
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
              <h3>{contributor.name + ' '}
                <small><a href={contributor.profUrl}>{contributor.login}</a></small>
              </h3>
              <p><span class="badge active">{contributor.totalCommits}</span>
                {' '}fridgetacular commit
                {contributor.totalCommits > 1?'s':''}.
              </p>
              <p>
                <span class="badge active">{contributor.numberOfUnitTests}</span>
                {contributor.numberOfUnitTests ? ' contributed unit tests.' : ''}
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

      </div>
    );
  }
}
