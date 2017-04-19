define([], function () {

var tech_doc = `## Venn Fridge

## Endless Stomach

###### Noel Benzinger, Thomas Cardwell, Cory Dunn, Scott Hornberger, Scott Munro, Jose Sanchez

## Introduction

#### What is the problem?

Cooking meals at home is a useful skill that leads to eating healthier, saving money, and spending valuable time with loved ones. Unfortunately, cooking the simplest of meals requires more time and thought than most people can afford in their busy lives. Would-be home-cooks must remember a wide array of tasty recipes alongside their current stock of ingredients and somehow merge that data together into a game plan for a delicious home-cooked meal. It’s a daunting task that drives people back into the greasy arms of their favorite take-out restaurants and TV dinners. Venn Fridge aims to solve this problem by providing users with an easy method to find delicious recipes that best utilize their ingredients. In addition, Venn Fridge will provide all kinds of auxiliary knowledge about recipes you’re interested in and ingredients that you cook with; ingredient substitutions, dietary categories, and related recipes will all be right at your fingertips through Venn Fridge.

#### What are the use cases?

1. Find Recipe From Ingredients - A user has a set of ingredients that they’d like to cook with. Using Venn Fridge, they are able to find a set of recipes that uses most of those ingredients and then look at grocery products to fill ones they are missing.

2. Browse Recipes - Users can search through our database of recipes, sorting and filtering the results, until they find something delicious. Then, they can read all about that particular recipe or browse through involved ingredients and related recipes.

3. Browse Ingredients - Just like recipes, users can sort and filter through ingredients in our database to find something to their liking. They can then click on the ingredient to find out more about the ingredient such as other recipes that use it.

4. Find substitute ingredients - Users can see what ingredients or combinations of ingredients act as substitutes for an ingredient they do not have or wish to avoid using.

5. Find grocery store items for ingredients - With a specific ingredient in mind, users can browse through products sold at grocery stores.

6. Search for food by cuisines - Users can find ingredients, recipes, and grocery products of a cuisine to satisfy their culinary curiosity.

7. Discover food that adheres to a dietary restriction - Users with dietary restrictions can find ingredients, recipes, and grocery products that adhere to their restrictions.

#### User Stories
Developing user stories is an agile technique that involves thinking about use cases in terms of the various sorts of users that will use the product and the ways they will want to use it. We used planning poker to discuss user stories, estimate their difficulty, and come to a consensus about the challenges and priorities of the project. The user stories for the project’s final stage are listed below.

A user should be able to search our website for grocery items, recipes, tags, ingredients, and all of their attributes.
Estimate: 40
Actual: 15 hours

Developer Janet should see a technical report of at least 5000 words.
Estimate: 8
Actual: 5 hours

Designer Jeane should be able to see a visualization of the Star Wars API.
Estimate: 20
Actual: 30 hours

Glenn wants to see a presentation about our website.
Estimate: 13
Actual: 3 hours

User Janet will be able to find the search bar on every single page.
Estimate: 3
Actual: 3 hours

Christie, a developer, will want to get appropriate data when they use our API.
Estimate: 3
Actual: 5 hours

User Bobby wants to have a good user experience on a mobile device.
Estimate: 5
Actual: 2 hours

Bill wants to be directed to a dense search results page when searching our site.
Estimate: 13
Actual: 25 hours

Quentin wants to see his search query contextualized.
Estimate: 20
Actual: 5 hours

Greg would like to see a link to our presentation on the about page.
Estimate: ½
Actual: Less than an hour

Bryan wants to see a good looking search results page.
Estimate: 5
Actual: 2 hours

## Design

#### Single Page Application

We opted for a Single Page Application model for our website instead of the more traditional model with a hierarchy of HTML pages. This pattern has become more common because of its frequency of use in mobile applications. In addition to its modernity, we chose this model because it was a simple way of displaying and communicating data between the front and back end. We are able to serve one HTML file and simply replace its contents with different components that we need as we navigate the site. This is largely due to React’s separation of rendering for different components, meaning a header on our site will not be re-rendered when we switch from the ingredients page to the recipes page.

#### Data Models

<div class="container">![image alt text](/static/images/image_0.png)</div>

The four pillars of our model are ingredients, recipes, grocery items, and tags. Ingredients are the individual items that go into making a recipe. Recipes are the completed dishes that users can cook. Grocery items are cooking items purchasable in grocery stores. And tags are descriptive categories containing subsets of ingredients, recipes, and grocery items. In addition to viewing all the elements of one of our pillars and viewing details about an individual element, we provide a few more useful relationships such as finding which ingredients can be substituted for other ingredients and searching for recipes that are similar to each other.

#### RESTful API

**List** all members of a group:

\`\`\`
[GET] /ingredients{?page_size}{?page}{?tags}{?sort} all the Ingredients, sorted and filtered
[GET] /recipes{?page_size}{?page}{?tags}{?sort} all the Recipes, sorted and filtered
[GET] /grocery_items{?page_size}{?page}{?tags}{?sort} all the Grocery Items, sorted and filtered
[GET] /tags{?page_size}{?page}{?min}{?sort} all the Tags, sorted and filtered
\`\`\`

**Details** of a member of a group:

\`\`\`
[GET] /recipes/{id} info for a specific recipe
[GET] /ingredients/{id} info for a specific ingredient
[GET] /grocery_items/{id} info for a specific grocery item
[GET] /tags/{id} info for a specific tag
\`\`\`

#### Search Capability

To enhance the browsability of our site, we added search functionality through a text field on our navigation bar. By typing search terms into the field, users can quickly get a list of matches to our data over any attribute. Names, servings on recipes, tag descriptions, and UPC codes are all a simple search away. We included pagination to enable users to browse through large sets of results and find what they are looking for. We also added contextualization to the results so users can see where their search terms are matched for each result.

In the API contract between frontend and backend, frontend sends a full search query string, page number, and page size. Then back-end responds with a list of matches each containing the pillar the result is from, the id, name, and image of the item, a list of context strings containing search terms, and pagination links.

To get a better feel for how we can implement searching in the backend, we decided to do spikes. There were three search architectures that we considered: Whoosh, PostgreSQL, and writing one from scratch. We spent a few days trying to construct a mock search using each tool to see which one would best suit our needs and discover potential pitfalls before we got too invested. We opted not to use Whoosh (or any of its many variants; see Whooshee, WhooshAlchemy, etc) because we ran into issues during our spike where we couldn't find a simple way to merge search results from multiple models. The PostgreSQL option looked similarly promising, but it would have meant restructuring our tests to run using a local PostgreSQL database instead of a SQLite database which was a hefty task. In the end, we settled on writing a search engine from scratch because it was the easiest to implement given the requirements of our search capabilities and a great learning experience as developers.

The first step to constructing our search engine is to create a search index out of our models. We have one index for each pillar saved to disk as a pickle file where each index is a mapping of lower case words to lists of items in the database. For each item, we generate a lowercased description string containing all the attributes of the item. Then we add a mapping in our index from each word in the description to the item. Having done this, a single access to our search index gives us a list of all the items in our database containing a word. And because the indexes are python dictionaries, indexing is very fast.

The second step in building our search engine is breaking down queries and building up search results using the indexes. First, words are extracted from the query using a regex that matches alphanumerical characters in addition to apostrophes and hyphens. Then we instantiate a dictionary that will map items to a set of terms the item contains. For each term in the query and each pillar’s index, we get a list of items from the index that contain the term and add the term to the item’s list in the map. At this point we’ve constructed a dictionary that tells us what set of search terms an item contains.

To finish up, we reverse the dictionary, giving us a mapping of search term sets to disjoint sets of items, and then turn the dictionary into a list by traversing its keys in descending order of set lengths. This gives us a list of items where items matching more terms come first. The final piece of the puzzle is selecting a portion of the search results using the page parameters, querying the database to get the items’ attributes, and for each result generating a context by rebuilding the description string and isolating portions where search terms show up.

## Data

[Spoonacular Food API](https://spoonacular.com/food-api)
[Pixabay Images API](https://pixabay.com/api/docs/)

#### Data Scraping

Our chosen source API for all our data is Spoonacular. With a student API key, we are allowed to make 5000 requests a day. Any requests past 5000 will begin to charge the credit card bound to the API key, so we are cautious to stay reasonably below the limit. By monitoring the headers of each request we make and keeping track of our request limit, we are able to set a soft and hard limit in our code. When the soft limit is reached, the scraper will finish the current recipe it is processing and then stop. If the hard limit is reached, an exception is thrown and no more requests are made. The hard limit is set to 50 so in the event that it’s hit we still have a few emergency requests at our disposal. The soft limit was set to 250 based on an estimate of the average requests we make per recipe so that we allow the scraper to finish the current recipe before it quits.

As implied above, our scraper’s largest unit of work is a recipe. Our decision to begin our scraping with recipes is two-fold. The first reason is a result of Spoonacular’s API. Unlike recipes, Spoonacular provides no endpoints for random ingredients or grocery items. Therefore we had no way to reasonably find ingredients or grocery products without a recipe to start with. The second reason was completeness. If we had simply chosen random recipes, ingredients, and grocery products, there would have been little overlap between our pillars. In the end, we decided to start with recipes which came with an ingredient list and use ingredients to get relevant grocery items.

However, we later realized that this method of scraping can easily blow through our request limit. We made this realization when we noticed that many recipes have 20 or more ingredients and that most ingredients have over 10 grocery products. This means that a recipe could require 200 or more requests alone in order to completely scrape. To cut down our demand we decided to limit the number of grocery products to 5 per ingredient. Additionally, we relied on the fact that many recipes share common ingredients such that over a long running time the average amount of new ingredients per recipe was much lower. Alone this was sufficient to allow us to scrape 375 unique recipes with all their ingredients and the first five grocery products to each ingredient.

Another concern of ours was how we could build similarities within our pillars. At the beginning of the project, our goal was to have each item display related items from the same pillar. Later we found out that the only pillar for which we could easily find similarities was recipes by using Spoonacular’s “find similar recipes” endpoint. Ingredients, grocery items, and tags would have to depend on other methods. Because of time constraints, we decided to describe similarities between grocery items as those that share the same ingredient and drop our plans for related ingredients and tags.

Finally, our data scraping is separated into two parts. The first part is the actual scraping of data in which we make requests to Spoonacular and save the results to JSON files. We chose this approach as a way to conserve our requests and retain all the data returned by Spoonacular in the event that we decide to make use of the extra data. After the data is scraped to JSON files we can read from them quickly without constraints or worries about request limits. In addition, having the data at hand through JSON files helped us visualize the data that was being returned in order to parse it with our code.

The second part is to process the JSON data and insert relevant information into the database. Unfortunately, due to unforeseen inconsistencies in Spoonacular’s data, this is an unexpectedly difficult task. We discovered while parsing the data that many of the basic expectations we had about Spoonacular’s data were wrong. Important fields are sometimes null, various ingredients have missing IDs and their images are too small, many recipe and ingredient names are garbage, field names are inconsistent, and more. We found ourselves running into issues one after another, forcing us to make lots of unattractive choices in order to sanitize the data. As a result, our data fell short of what we had set out to accomplish.

While our scraping strategy was able to work around many of Spoonacular’s limitations, we still needed to find suitable replacements for some of the tiny images they provided. We utilized the image API Pixabay to fill this gap, which was able to provide us with images of appropriate sizes. However, since Pixabay’s images are tagged by their users, we still needed to manually verify the results and make replacements where the images were unsuitable for our purposes.

## Tools

#### Front-end

###### Bootstrap

Bootstrap is a CSS, JavaScript and HTML front-end framework created by Twitter that helps web developers create applications ready for both web and mobile. It has gained enormous popularity in recent years, being used by websites like Lyft and Vogue. Its popularity can make the stock settings look rather commonplace in today’s design setting, but it offers many potential customizations to build off of the base Bootstrap components. Bootstrap is engineered to be mobile first, which means implementing Bootstrap styling across a plethora of devices, from phones to tablets to desktops, while maintaining a consistent but aesthetically pleasing experience is very easy. We were able to leverage Bootstrap to further the positives of React, that is, modular code and code reuse. Bootstrap furthers this by attaching their simple and modern components to HTML div attributes via class names. From there, we edit any CSS by connecting those containers to a style sheet and overriding properties as we see fit, including different configurations for various screen sizes.

###### [React](https://facebook.github.io/react/)

React is a front-end library for JavaScript initially developed for internal use by Facebook. It has since been open-sourced and has gained a large following. Two of the main reasons for React’s large following are its efficient way of updating the browser’s DOM and its ability to play nice with JSX syntax.

A web page in a browser is logically defined by its Document Object Model (DOM). Updating the browser’s DOM is a costly procedure. Even deciding when to update the DOM is a non-trivial task, normally accomplished by recursively traversing the DOM tree looking for changes. React solves this problem with an elegant solution. Obviously, the DOM should update when data is updated. However, it is costly to traverse the entire DOM regularly checking for dirty data. With React, each component maintains and monitors its own state. A component re-renders itself only when its internal state changes. But the component does not render itself onto the browser’s DOM, it renders onto **React’s virtual DOM.** React keeps a virtual copy of the browser’s DOM that is much more efficiently updated. Think of updating the browser’s DOM like changing a line in a book, and updating the virtual DOM like changing your mind about the line you might have written. The changes to the virtual DOM do not get drawn to the screen unless they visually alter the browser’s DOM, and only the components that have changed are updated. React has an efficient diff algorithm to check for dissimilarities between the DOMs. 

**React with JSX** solves a major problem with the classic trio: HTML, CSS, and JavaScript. Developers using these tools in their vanilla form are forced to write code in three separate places to create, style, and add functionality to an element on a web page. Using JSX with React allows a developer to write XML syntax within components. This means that developers can create the HTML object and define its functionality in the same object. This solution, coupled with Bootstrap’s simple syntax and pre-defined components, greatly speeds up the programming process. HTML elements are styled with Bootstrap according to their class attribute within the HTML code itself. The trio we chose to work with, React, JSX, and Bootstrap, gave us the power to create, style, and define functionality for each component on the page, while also making our code easy to read and understand.

In addition to React’s functionality, the Venn Fridge team also chose React over alternatives due to the large community supporting its development. There is significant documentation and many examples to draw from available. Many of the problems we ran into had been solved or clarified by others previously. Our team found the [tutorials](https://www.youtube.com/playlist?list=PLoYCgNOIyGABj2GQSlDRjgvXtqfDxKm5b) by LearnCode.academy to be incredibly helpful in understanding React’s design and structure. React and the surrounding community have also introduced us to other useful front-end features and practices, such as JSX and ES6. 

React allowed us to programmatically adjust elements on the page and to populate element attributes with REST responses. The team info section of this page is dynamically generated with calls to GitHub’s API in addition to a team info JSON file. In React, these things are easily merged and added to the page as one templated container used for all 6 team members. And thanks to JSX, simple logic such as whether to put an ‘s’ on the attribute name depending on the value of that attribute is just inlined directly into the HTML.

**React Router** is a community-created package available for React that allows developers to easily create single page applications. By injecting React components into a single HTML file, React Router saves a web application from having to load a completely new HTML file any time the user navigates to a new page. React Router complements React’s modularity by allowing developers to connect routes directly to modules. In our site, we nest every page’s route component within a parent route named Layout so that all unique content displays between a persistent navigation and footer bar. We find this nesting feature of React Router appealing because the logical structure of the router reflects the structure of our site.

React Router works by taking the current URL path, verifying that it is one of its declared routes, and loading the related React component into a specified location on the page. React Router also has a helpful feature called hash-history that stores a unique hash representing the current page state into the URL. This is necessary in order for single-page applications to preserve navigation history in browsers. Overall, React Router was an easy addition to our application that gave us important functionality.

**React-Bootstrap** is a library of React components that implement Twitter’s popular front-end framework, Bootstrap. As mentioned above, React with JSX and Bootstrap gives developers the power to create, style, and add functionality to page elements in one component. The major flaw in this trio is the awkward means by declaring an HTML element’s class for Bootstrap styling. For example, to create a small button with default coloring, one must declare:

\`<button class=”btn btn-sml btn-default”>Click Here</button>\`

The word “button” (and “btn”) must be repeated quite a few times. It would be better if one could declare a Bootstrap component and specify its size, coloring, and style in the same way we pass other information to other Bootstrap components. React-Bootstrap allows for cleaner code, and coupled with React and JSX, it unifies the syntax for creating, styling, and adding functionality to HTML elements:

\`<Button bsStyle="success" bsSize="small" onClick={someFunction}>Click Here</Button>\`

###### Webpack

Webpack is a module bundler for JavaScript designed to bundle images, scripts and other files into one entry point location for an application. Webpack transforms each file, whether it be a .js or a .jpg, into a module in the application and adds it to a dependency graph for what will be our *bundle*. It also allows plugins and actions to be taken on large parts of the code (e.g. uglifyjs to compress and minify JavaScript for production). We also utilized a webpack component that listened to changes in code and updated a server, which was very efficient for front-end development.

#### Back-end

###### Flask

Flask is a lightweight Python web framework that allows us to write the business logic of a simple backend web server in a readable, expressive style. One of Flask’s standout features is its use of Python route decorators. These allow us to write functions that respond to HTTP messages sent to our server with any valid HTTP response. Our team used these route functions to structure our website as a Single Page Application. Essentially, any request to our website can be routed through the one callback that will give the client (in this case a web browser) the homepage of our site. As well, we can use the route decorators to set up a RESTful API that can be accessed via HTTP messages, which allows any client (including the front end of our Single Page Web Application) to query for any useful information it needs.

Flask’s second great strength is the extensive list of tools that we can seamlessly integrate into our project. Instead of having to roll our own OAuth solution we can use one of the popular Flask-focused solutions like Flask-Dance or Flask-OAuth.

###### SQLAlchemy

Because database systems are built on relational algebra, declarative programming patterns, and distributed storage, it can often be challenging to write software that effectively uses them. SQLAlchemy provides us an Object Relational Mapping (ORM) which aligns the interface of the database with the style of imperative programming languages like Python. As well, in combination with Flask, SQLAlchemy can remove the burden of having to implement certain common database patterns like association tables.

SQLAlchemy ORM works by abstracting away database languages through python classes. Each class represents a relation or table in the database and each column of the table is an instance of the SQLAlchemy Column class. The Column class and SQLAlchemy value type abstractions simplify column definitions and make it easy for any developer to decipher the column to at a glance. Then, to alter rows in the database or query for data, it’s as simple as accessing or assigning to a model class’s members. Underneath the hood, SQLAlchemy will use the model classes and their columns to compile queries in the database’s language. As a result, database code is programmatic so it is easy to read and work with.

Another benefit of SQLAlchemy’s database abstraction is testing. SQLAlchemy supports many back-end databases, and a useful choice for testing is SQLite which can easily be deployed on almost any development environment. Additionally, SQLAlchemy even has an in-memory SQLite option which circumvents having to setup a database. This choice is great for continuous integration where database setup and takedown can be difficult and expensive. However, it is worth noting that database testing with a different back-end is not recommended as there are differences between databases that may hide failures.

###### MyPy

MyPy is a tool that allows us to annotate our python source code with a simple type system, and then statically analyze that source code for type errors. Using MyPy, our team can avoid many common runtime type errors and more easily reason about the execution of our python backend. An important part of MyPy is that it allows mixing of dynamic and statically typed code so that projects can continue to work with untyped code. Consequently, large projects can slowly transition towards a fully typed project over time instead of all in one go.

#### Productivity

###### Slack

Slack is a team communication tool that provides a number of services useful to our group. Multiple linked conversation channels enable us to separate discussions by topic while keeping them in a centralized location. Integration of the Slack chat with our GitHub repo allows everyone to stay up to date on the state of each feature as it was worked on. Slack’s Google Hangouts tool also facilitates easy planning and hosting of remote meetings. Slack also provided a convenient place to list examples or tutorials easily found by all members, especially while learning the tools.

###### ZenHub

ZenHub is a project management app that adds significant features to GitHub’s issue tracker. These features include the ability to assign tasks to specific group members, classify issues as sub-problems of larger ‘epic’ tasks, and track their progress. Group members can move issues between several columns in a board, designated by their completion level. For example, a contributor may move an issue from the project backlog into the current sprint or close an issue by moving it into the closed column. We used ZenHub to organize the needs of our project, internally communicate our progress on issues, and request reviews of our changes.

###### [PlanITpoker](http://www.planitpoker.com/)

Planning Poker is an agile development activity used to estimate the relative difficulties of tasks in a project. Members of the development team each vote anonymously on how hard they believe a task will be, and then all votes are revealed simultaneously. If there is disagreement then the task is discussed, with people defending their estimates and refining their opinions. After the discussion there is another round of voting, and if there is still disagreement another round of discussion. The process repeats until a consensus is achieved, and then the next task is voted on. Anonymous voting forces everyone to think about the tasks without just deferring to one group member, and the discussion phase helps each team member gain a fuller understanding of the task. In the end, all teammates should have a better understanding of the project goals and a set of well-reasoned estimates for their difficulty.

PlanITpoker is an online tool that allows teams to play planning poker digitally and save the results. We used PlanITpoker to analyze our user stories for the final phase of the project and develop informed estimates about the tasks ahead of us.

## Hosting

#### Using Google Cloud Platform

Google Cloud App Engine allows developers to write web applications without having to worry about managing the host servers that your application runs on. App Engine also uses a developer-friendly minute-by-minute payment plan.

We used Google Cloud Platform and the Google Cloud App Engine to host our web application. App Engine gives us the ability to write our applications without having to manage the host server infrastructure. Common challenges such as building servers, maintaining server environments, spinning up servers to meet increases in website traffic, and partitioning our web application into smaller, more manageable microservices are all challenges we avoid by using App Engine. App Engine makes it easy and economical to serve our website to whoever may be trying to access it without slowing down our development cycle. 

Our first step to setting up our app on Google App Engine was creating a Google Cloud Platform account with billing information. Once this account was verified, we could create projects that our app could be deployed to.

The next step was setting up our Google App Engine database to store all of our site’s data, which we chose to build using Google’s CloudSQL platform. CloudSQL was the right choice for our team because it is efficient, cloud-accessible, and its relational scheme mirrored the data we were trying to model. CloudSQL also integrates well with the object-relational mapping tools like MySQL and SQLAlchemy that make interacting with databases much simpler.

When it was finally time to deploy an iteration of our app we used Google’s Cloud SDK. After ensuring that the SDK is set up to target the correct Google App Engine project, we used the "gcloud app deploy" command which magically packages up our code for us, spins up any necessary server instances, and makes our app available on the web.

#### Namecheap Setup

Once our web app was deployed to Google’s App Engine servers, it was initially only reachable through a very ugly URL, *<project-id>.appspot.com*. To make our website more attractive to potential users, we purchased a more attractive domain name from Namecheap. Next, we verified that we owned the new domain through Google’s custom domain name options in our App Engine project preferences. Google App Engine’s custom domain name service then generated domain name records that we appended to our Namecheap domain configuration. After deleting any conflicting domain records and waiting 24 hours for the DNS changes to propagate, our web app was available at our new domain."
`;
            
    return tech_doc;
});