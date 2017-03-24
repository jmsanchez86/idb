import React from "react";

var teamData = require('json!../../../../app/static/data/team-info.json');
var tech_doc = `## Venn Fridge

#### Endless Stomach

###### Noel Benzinger, Thomas Cardwell, Cory Dunn, Scott Hornberger, Scott Munro, Jose Sanchez

## Introduction

#### What is the problem?

Cooking meals at home is a useful skill that leads to eating healthier, saving money, and spending valuable time with loved ones. Unfortunately, cooking the simplest of meals requires more time and thought than most people can afford in their busy lives. Would-be home-cooks must remember a wide array of tasty recipes alongside their current stock of ingredients and somehow merge that data together into a game plan for a delicious home-cooked meal. It’s a daunting task that drives people back into the greasy arms of their favorite take-out restaurants and TV dinners. Venn Fridge aims to solve this problem by providing users with an easy method to find delicious recipes that best utilize their ingredients. In addition, Venn Fridge will provide all kinds of auxiliary knowledge about recipes you’re interested in and ingredients that you cook with; ingredient substitutions, dietary categories, and related recipes will all be right at your fingertips through Venn Fridge.

#### What are the use cases?

1. Find Recipe From Ingredients - A user has a set of ingredients that they’d like to cook with. Using Venn Fridge, they are able to find a set of recipes that uses those ingredients and lets them know which ingredients they are missing.

2. Browse Recipes - Users can search through our database of recipes, sorting and filtering the results until they find something delicious. From here, they can read all about that particular recipe or browse through related recipes.

3. Browse Ingredients - Just like recipes, users can sort and filter through ingredients in our database to find something to their linking and can also read more about the ingredient or look at related ingredients.

4. Find substitution ingredients - Users can find ingredients that can act as substitutes in their favorite recipes.

5. Find grocery store items for ingredients - With a specific ingredient in mind, users can browse through products sold at grocery stores containing the ingredient.

6. Search for food by cuisines - Users can find ingredients, recipes, and grocery products of a cuisine to satisfy their culinary curiosity.

7. Discover food that adheres to a dietary restriction - Users with dietary restrictions can find ingredients, recipes, and grocery products that adhere to their restrictions.

## Design

#### Data Models

![image alt text](/static/images/image_0.png)

The four pillars of our model are ingredients, recipes, grocery items, and tags. Ingredients are the individual items that go into making a recipe. Recipes are the completed dishes that our users want to cook. Grocery items are cooking items purchasable in a grocery stores. Tags are descriptive categories containing subsets of ingredients, recipes, and grocery items. Nutrition information is also included to provide useful health information about ingredients and recipes. In addition to viewing all the elements of one of our pillars and viewing details about an individual element, we provide a few more useful relationships such as finding which ingredients can be substituted for other ingredients and searching for recipes that are similar to each other.

#### RESTful API

**List** all members of a group:

* **[GET] /api/ingredients** all the Ingredients

* **[GET] /api/recipes** all the Recipes

* **[GET] /api/grocery_items** all the Grocery Items

* **[GET] /api/tags** all the Tags

 

**Details** of a member of a group:

* **[GET] /api/recipes/<id>** info for a specific recipe

* **[GET] /api/ingredients/<id>** info for a specific ingredient

* **[GET] /api/grocery_items/<id>** info for a specific grocery item

* **[GET] /api/tags/<id>** info for a specific grocery item

## Data

[Spoonacular Food Api](https://spoonacular.com/food-api) 

## Tools

#### Front-end

###### [React](https://facebook.github.io/react/)

React is a front-end library for JavaScript initially developed for internal use by Facebook. It has since been open-sourced and has gained a large following. React is able to produce fast results by maintaining a virtual Document Object Model (DOM), a structuring of HTML elements as a tree, for each component. As a result, instead of reconstructing the entire DOM or reloading a webpage, applications need only update the html elements that change. This pattern is known as single-page application architecture. This enables you to pass data between pages and create a hierarchical system of state and properties between your pages. React’s approach to single-page application architecture allows developers to produce robust applications with ease. 

In addition to React’s functionality, the Venn Fridge team also chose React over alternatives due to the large base of documentation and examples to draw from. Its large user-base meant that many problems we ran into have been solved or clarified by others in recent years. Our team found [tutorials](https://www.youtube.com/playlist?list=PLoYCgNOIyGABj2GQSlDRjgvXtqfDxKm5b) by LearnCode.academy to be incredibly helpful in understanding React’s design and structure. React and the surrounding community have also introduced us to other useful front-end features and practices, such as .jsx for writing html inside JavaScript, and EcmaScript for new standards in web design. We are able to programmatically adjust pages when need, or even utilize other external APIs to fill data attributes. The team info section of this page is dynamically generated with calls to GitHub’s API in addition to a team-info JSON file. In React, these things are easily merged and added to the page as one templated container used for all 6 team members. And thanks to .jsx, simple logic such as whether to put an ‘s’ on the attribute name depending on the value of that attribute is just inlined directly into the HTML.

###### React Router

React Router allows developers to easily create a single page application so that all content can be served up quickly through JavaScript. This saves the application from having to load a completely new HTML file any time the user navigates to a new page. React Router complements React’s modularity by allowing developers to connect routes directly to components. Routes and their components can also be nested to prevent parent content from changing when child content is changed.

In our site, we nest every page’s route component within a parent route named Layout so that all unique content displays between a persistent navigation and footer bar. We find this nesting feature of React Router appealing because it reflects the visual appearance and structure of our site.

React Router works by taking the current URL path, verifying that it is one of the declared routes, and loading the related React component into a specified location on the page. This enables our single-page application to simulate the association of urls to the pages so that each page can be bookmarked and shared. React Router also has a helpful feature called hash-history that stores a hash of the current page state into the url. This is necessary in order for single-page applications to preserve navigation history in browsers. Overall, React Router was an easy addition to our application that gave us important functionality.

###### Bootstrap

Bootstrap is a CSS, JavaScript and HTML framework that helps design pages for both web and mobile. It has also gained enormous popularity in recent years (websites like Lyft and Vogue use it). It’s popularity can make the stock settings look rather commonplace in today’s design setting, but it also offers a large amount of potential customizations to build off of the base Bootstrap components. It is also engineered to be relatively easy to implement Bootstrap styling across a plethora of devices, from phones to tablets to desktops, while maintaining a consistent but aesthetically pleasing experience. We were able to leverage Bootstrap to further the positives of React, that is, modular code and code reuse. Bootstrap furthers this by attaching their simple and modern components to HTML div attributes via class names. From there, we edit any css by connecting those containers to a style sheet and overriding properties as we see fit, including different configurations for various screen sizes.

###### Webpack

Webpack is a module bundler for JavaScript designed to bundle images, scripts and other files into one entry point location for an application. Webpack transforms each file, whether it be a .js or a .jpg, into a module in the application and adds it to a dependency graph for what will be our *bundle*. It also allows plugins and actions to be taken on large parts of code (e.g. uglifyjs to compress and minify JavaScript for production).

#### Back-end

###### Flask

Flask is a lightweight Python web framework that allows us to write the business logic of a simple backend web server in a readable, expressive style. One of Flask’s standout features is its use of Python route decorators. These allow us to write functions that respond to HTTP messages sent to our server with any valid HTTP response. Our team used these route functions to structure our website as a Single Page Application. Essentially, any request to our website can be routed through the one callback that will give the client (in this case a web browser) the homepage of our site. As well, we can use the route decorators to set up a RESTful API that can be accessed via HTTP messages which allows any client (including the frontend of our Single Page Web Application) to query for any useful information it needs.

Flask’s second great strength is the extensive list of tools that we can seamlessly integrate into our project. Instead of having to roll our own OAuth solution we can use one of the popular Flask-focused solutions like, Flask-Dance or Flask-OAuth.

###### SQLAlchemy

Because database systems are built on relational algebra, declarative programming patterns, and distributed storage, it can often be challenging to write software that effectively uses them. SQLAlchemy provides us an Object Relational Mapping (ORM) which aligns the interface of the database with the style of imperative programming languages like Python. As well, in combination with Flask, SQLAlchemy can remove the burden of having to implement certain common database patterns like association tables.

SQLAlchemy ORM works by abstracting away database languages through python classes. Each class represents a relation or table in the database and each column of the table is an instance of the SQLAlchemy Column class. The Column class and SQLAlchemy value type abstractions simplify column definitions and make it easy for any developer to decipher the column to at a glance. Then, to alter rows in the database or query for data, it’s as simple as accessing or assigning to a model class’s members. Underneath the hood SQLAlchemy will use the model classes and their columns to compile queries in the database’s language. As a result, database code is programmatic so it is easy to read and work with.

Another benefit of SQLAlchemy’s database abstraction is testing. SQLAlchemy supports many back-end databases, and a useful choice for testing is SQLite which can easily be deployed on almost any development environment. Additionally, SQLAlchemy even has an in-memory SQLite option which circumvents having to setup a database. This choice is great for continuous integration where database setup and takedown can be difficult and expensive. However, it is worth noting that database testing with a different back-end is not recommended as there are differences between databases that may hide failures.

###### MyPy

MyPy is a tool that allows us to annotate our python source code with a simple type system, and then statically analyze that source code for type errors. Using MyPy, our team can avoid many common runtime type errors and more easily reason about the execution of our python backend. An important part of MyPy is that it allows mixing of dynamic and statically typed code so that projects can continue to work with untyped code. Consequently, large projects can slowly transition towards a fully typed project over time instead of all in one go.

#### Productivity

###### Slack

Slack is a team communication tool that provides a number of services useful to our group. Multiple linked conversation channels enable us to separate discussions by topic while keeping them in a centralized location. Integration of the Slack chat with our GitHub repo allows everyone to stay up to date on the state of each feature as it was worked on. Slack’s Google Hangouts tool also facilitates easy planning and hosting of remote meetings.

###### Zenhub

Zenhub is a project management app that adds significant features to GitHub’s issue tracker. These features include the ability to assign tasks to specific group members, classify issues as sub-problems of larger ‘epic’ tasks, and track their progress. Group members can move issues between several columns in a board, designated by their completion level. For example, a contributor may move an issue from the project backlog into the current sprint or close an issue by moving it into the closed column. We used Zenhub to organize the needs of our project, internally communicate our progress on issues, and request reviews of our changes.

## Hosting

#### Using Google Cloud Platform

Google Cloud App Engine allows developers to write web applications without having to worry about managing the host servers that your application runs on. App Engine also uses a developer-friendly minute-by-minute payment plan.

We used Google Cloud Platform and the Google Cloud App Engine to host our web application. App Engine gives us the ability to write our applications without having to manage the host server infrastructure. Common challenges such as building servers, maintaining server environments, spinning up servers to meet increases in website traffic, and partitioning our web application into smaller, more manageable microservices are all challenges we avoid by using App Engine. App Engine makes it easy and economical to serve our website to whoever may be trying to access it without slowing down our development cycle. 

Our first step to setting up our app on Google App Engine was creating a Google Cloud Platform account with billing information. Once this account was verified, we could create projects that our app could be deployed to.

The next step was setting up our Google App Engine database to store all of our site’s data, which we chose to build using Google’s CloudSQL platform. CloudSQL was the right choice for our team because it is efficient, cloud-accessible, and its relational scheme mirrored the data we were trying to model. CloudSQL also integrates well with the object relational mapping tools like MySQL and SQLAlchemy that make interacting with databases much simpler.

When it was finally time to deploy an iteration of our app we used Google’s Cloud SDK. After ensuring that the SDK is setup to target the correct Google App Engine project, we used the "gcloud app deploy" command which magically packages up our code for us, spins up any necessary server instances, and makes our app available on the web.

#### Namecheap setup

Once our web app was deployed to Google’s App Engine servers, it was initially only reachable through a very ugly URL, *<project-id>.appspot.com*. To make our website more attractive to potential users, we purchased a more attractive domain name from Namecheap. Next we verified that we owned the new domain through Google’s custom domain name options in our App Engine project preferences. Google App Engine’s custom domain name service then generated domain name records that we appended to our Namecheap domain configuration. After deleting any conflicting domain records and waiting 24 hours for the DNS changes to propagate, our webapp was available at our new domain."
`;

var showdown  = require('showdown'),
    converter = new showdown.Converter(),
    html      = converter.makeHtml(tech_doc);

export default class About extends React.Component {
  constructor() {
    super();
    this.state = {
      gitDataUrl: 'https://api.github.com/repos/jmsanchez86/idb/stats/contributors',
      gitIssuesUrl: 'https://api.github.com/repos/jmsanchez86/idb/issues',
      contributors: new Map(),
      totalIssues: 0,
      totalCommits: 0
    };
  }
  totalCommits() {
    var total = 0;
    for (cont in this.contributors) {
      total = total + this.cont.totalCommits;
    }
    this.setState({totalCommits : total});
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
            numberOfUnitTests: teamData[i].numberOfUnitTests,
            numIssues:0
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
                   _this.totalCommits();
              }
              for (var attrname in gitContr)
                { contributor[attrname] = gitContr[attrname]; }
            }
             var cont = _this.state.contributors;
            cont.get('scottnm').numIssues = 32;
            cont.get('CoryDunn').numIssues = 1;
            cont.get('jmsanchez86').numIssues = 0;
            cont.get('ndbenzinger').numIssues = 1;
            cont.get('scott-hornberger').numIssues = 5;
            cont.get('thomascardwell7').numIssues = 21;
            _this.totalIssues = 60;
            
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
                {contributor.totalCommits > 1?'s':''}.
              </p>
              <p><span class="badge active">{contributor.numIssues}</span>
                {' '}fridgetacular issue
                {contributor.numIssues > 1?'s':''}.
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
        <div class="container">
          <h4>Useful Links!</h4>
          <h6><a href="https://github.com/jsanchez86/idb">GitHub Repo</a></h6>
          <p><span class="badge active">{181}</span>
                {' '}total commits.
          </p>
          <h6><a href="https://github.com/jsanchez86/idb/issues">Issue Tracker</a></h6>
          <p><span class="badge active">{60}</span>
                {' '}total issues.
          </p>
          <h6><a href="https://docs.vennfridge.apiary.io/#">Apiary API</a></h6>
        </div>
        <div class="container" dangerouslySetInnerHTML={{__html: html}} />
      </div>
    );
  }
}
