import React from "react";

export default class Recipes extends React.Component {
  render() {
    console.log("settings");
    return (
      <div id="unique-content">
          <div class="container">
            <div class="col-sm-8 col-sm-offset-2 text-center">
              <h4>Nom nom nom...</h4>
              <img class="venn" src="../static/images/diagram.png" />
              <p>Let us help you help yourself to some tasty food.</p>
            </div>
          </div>

          <div id="grid-results" class="row">
              <div class="col-sm-6 col-md-4">
                <div class="thumbnail">
                  <img src="../static/images/diagram.png" />
                  <div class="caption">
                      <h3>MegaCool Recipe</h3>
                      <p>This is totally the first part of the best MegaCool you have ever eaten...</p>
                      <p><a href="#" class="btn btn-primary" role="button">Get Recipe</a> <a href="#" class="btn btn-default" role="button">Find More Like This</a></p>
                  </div>
                </div>
              </div>

              <div class="col-sm-6 col-md-4">
                  <div class="thumbnail">
                  <img src="../static/images/eggs.jpg" />
                  <div class="caption">
                      <h3>MegaCool 2 Recipe</h3>
                      <p>This is totally the egg part of the best MegaCool you have ever eaten...</p>
                      <p><a href="#" class="btn btn-primary" role="button">Get Recipe</a> <a href="#" class="btn btn-default" role="button">Find More Like This</a></p>
                  </div>
                  </div>
              </div>

              <div class="col-sm-6 col-md-4">
                  <div class="thumbnail">
                  <img src="../static/images/greens.jpg" />
                  <div class="caption">
                      <h3>MegaLeek Recipe</h3>
                      <p>Chefs around the universe agree, when you put leeks with onions, you win...</p>
                      <p><a href="#" class="btn btn-primary" role="button">Get Recipe</a> <a href="#" class="btn btn-default" role="button">Find More Like This</a></p>
                  </div>
                  </div>
              </div>

              <div class="col-sm-6 col-md-4">
                  <div class="thumbnail">
                  <img src="../static/images/strawberries.jpg" />
                  <div class="caption">
                      <h3>MegaStrawberry Recipe</h3>
                      <p>Snozberries? What's a Snozberry?</p>
                      <p><a href="#" class="btn btn-primary" role="button">Get Recipe</a> <a href="#" class="btn btn-default" role="button">Find More Like This</a></p>
                  </div>
                  </div>
              </div>

          </div>
      </div>

    );
  }
}
