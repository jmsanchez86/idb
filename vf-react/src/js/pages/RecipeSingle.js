import React from "react";
import { IndexLink, Link } from "react-router";

import OptionalList from "../components/layout/OptionalList";

var apiRoot = '' + require('../scripts/Config.js');

export default class RecipeSingle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ingredient_list : [],
      tags : [],


      instructions : '',
      ready_time : '',
      source : '',
      blurb : '',
      image : '',
      name : '',
      id : this.props.params.id,

    };
    this.requestData();
  }

  requestData() {

    var _this = this;

    const requestString = 'http://' + apiRoot + '/recipes/' + _this.state.id;

    // Fetch singleton's required data.
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {

            _this.setState({
                ingredient_list : responseData.ingredient_list,
                tags : responseData.tags,

                instructions : responseData.instructions,
                ready_time : responseData.ready_time,
                source : responseData.source_url,
                blurb : responseData.blurb,
                image : responseData.image,
                name : responseData.name,
            });

        });
      })
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  getInstructions(instructions, source) {
    if (instructions && instructions.length) {
      return (
        <p id="instructions">{instructions}</p>
      )
    } else {
      return (
        <div>
        <p disabled>Sorry, we don't have instructions. Click the following to visit the recipe source. </p>
        <p><a href={source}> Recipe Source. </a></p>
        </div>
      )
    }
  }

  render() {
    const name = this.state.name;
    const blurb = this.state.blurb;
    const image = this.state.image;
    const source = this.state.source;
    const ready_time = this.state.ready_time;
    const instructions = this.state.instructions;

    const ingredients = this.state.ingredient_list.map(function(ingredient){
      return(
        <div key={ingredient.id} class="list-group-item">
          <p><Link to={"ingredients/" + ingredient.id}>{ingredient.original_string}</Link></p>
        </div>);
    });
    console.log(ingredients);
    const tags = this.state.tags.map(function(tag){
      return (
        <div key={tag.name} class="center-block col-lg-2 col-md-2 col-sm-3 col-xs-3">
          <Link to={"tags/" + tag.name}><img class="img-responsive" src={tag.image} /></Link>
        </div>);
    });

    return (
      <div class="single container-fluid">
        <div class="row">
          <div class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
            <h3>
              {name}
            </h3>
          </div>
        </div>
        <div class="row">
          <div id="blurb" class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
            <p>
            {blurb}
            </p>
          </div>
        </div>
        <div class="row gutter-20">
          <div class="col-lg-offset-1 col-lg-4 col-md-6 col-sm-6 col-xs-12">
            <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
              <div class="row">
                <p>
                  <img class="img-rounded img-responsive" src={image} />
                </p>
              </div>
              <div class="row ">
                  {tags}
              </div>
              <div class="row">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
              <div class="panel-body">
              <h4 >Ready in {ready_time} minutes.</h4>
              </div>
              </div>
              </div>

              </div>
            </div>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <OptionalList
              title="Ingredients"
              list={ingredients}
              />
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                <h3 disabled={!instructions || !instructions.length}>Instructions</h3>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                {this.getInstructions(instructions, source)}
              </div>
            </div>


          </div>
        </div>
      </div>
    );
  }
}
