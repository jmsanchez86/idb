import React from "react";
import { IndexLink, Link } from "react-router";

var apiRoot = '' + require('../scripts/Config.js');

export default class GroceryItemSingle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      related_grocery_items : [],
      tags : [],

      image : '',
      name : '',
      upc : '',
      id : this.props.params.id,

    };
    this.requestData(); 
  }

  requestData() {

    var _this = this;

    const requestString = 'http://' + apiRoot + '/grocery_items/' + _this.state.id;
    console.log(requestString);

    // Fetch singleton's required data.
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {

            _this.setState({
                related_grocery_items : responseData.related_grocery_items,
                tags : responseData.tags,

                image : responseData.image,
                name : responseData.name,
                upc : responseData.upc,
            });

        });
      })
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  render() {
    const name = this.state.name;
    const image = this.state.image;
    const upc = this.state.upc;
    
    const tags = this.state.tags.map(function(tag){
      return (
        <div key={tag.name} class="center-block col-lg-3 col-md-3 col-sm-3 col-xs-3">
        <Link to={"tags/" + tag.name}><img class="img-responsive" src={tag.image} /></Link>
        </div>);
      });
    const grocery_items = this.state.related_grocery_items.map(function(item){
      return (
        <div key={item.id} class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <Link to={"grocery_items/" + item.id}><p> {item.name} </p></Link>
        </div>);
      });
    return (

            <div class="grocery-item-single single container-fluid">
              <div class="row">
                <div class="col-lg-offset-1 col-lg-11 col-md-12 col-sm-12 col-xs-12">
                  <h3>
                    {name}
                  </h3>
                </div>
              </div>
              <div class="row top-buffer gutter-20">
                <div class="col-lg-offset-1 col-lg-4 col-md-6 col-sm-6 col-xs-12">
                  <div class="row">
                    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                      <div class="row">
                        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                          <p>
                            <img class="img-rounded img-responsive" src={image} />
                          </p>
                        </div>
                      </div>
                      <div id="upc" class="row">
                        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
                          <p>
                            UPC: {upc}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <h3 disabled={!tags.length}>Tags</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="panel-body">
                      {tags}
                    </div>
                  </div>
                </div>
                <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <h3 disabled={!grocery_items.length}>Related Grocery Items</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="panel-body">
                      {grocery_items}
                    </div>
                  </div>
                </div>
              </div>

            </div>
    );
  }
}
