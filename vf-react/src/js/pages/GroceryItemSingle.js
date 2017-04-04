import React from "react";
import { IndexLink, Link } from "react-router";


export default class GroceryItemSingle extends React.Component {
   constructor(props) {
    super(props);
    this.state = {
      ingredient : {},
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

    var _ingredient = '';
    var _tags = [];
  
    var _image = '';
    var _name = '';
    var _upc = '';

    const requestString = 'http://api.vennfridge.appspot.com/grocery_items/' + _this.state.id;
    console.log(requestString);
    // call api with new query params
    fetch(requestString)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
            const temp_ingredient = responseData.ingredient;
            const temp_tags = responseData.tags;

            for (var id in temp_tags) {
              _tags.push(temp_tags[id]);
            }

            _ingredient = responseData.ingredient;
            _image = responseData.image;
            _name = responseData.name;
            _upc = responseData.upc;

            _this.setState({
                ingredient : _ingredient,
                tags : _tags,

                image : _image,
                name : _name,
                upc : _upc,
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
    const ing_id = this.state.ingredient.id;
    const ingredient = this.state.ingredient;
    const upc = this.state.upc;
    
    const tags = this.state.tags.map(function(tag){
      const tagItem = tag;
      return (
        <div key={tag} class="center-block col-lg-3 col-md-3 col-sm-3 col-xs-3">
        <Link to={"tags/" + tag.id}><img class="img-responsive" src={tagItem.image} /></Link>
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
                      <h3 disabled={!ingredient}>Related Ingredient</h3>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-11 col-md-12 col-sm-12 col-xs-12">
                      <div key={ing_id} class="list-group-item">
                        <p><Link to={"ingredients/" + ing_id}>{ingredient.name}</Link></p>
                      </div>
                    </div>
                  </div>
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
              </div>

            </div>
    );
  }
}
