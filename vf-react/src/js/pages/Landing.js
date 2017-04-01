import React from "react";

export default class Landing extends React.Component {
  render() {
    return (
        <div>

          <div id="myCarousel" class="carousel slide" data-ride="carousel">
            <ol class="carousel-indicators">
                <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
                <li data-target="#myCarousel" data-slide-to="1"></li>
                <li data-target="#myCarousel" data-slide-to="2"></li>
            </ol>
            <div class="carousel-inner">
                <div class="item active">
                    <div class="slide1"></div>
                </div>
                <div class="item">
                  <div class="slide2"></div>
                </div>
                <div class="item">
                  <div class="slide3"></div>
                </div>
            </div>
          </div>
          <div id="main-text" >
            <div class="text-center">
              <h2>We Love Your Fridge</h2>
              <img class="venn" src="../static/images/diagram.png" />
              <h4 id="landing-h4">We love food. We eat almost every day.</h4>
              <p id="landing-p">Let us help you help yourself to some tasty food.</p>
            </div>
          </div>



          </div>
    );
  }
}
