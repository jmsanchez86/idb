import React from "react";

import * as d3 from "d3";

var global_total = 0;
var link_total = 0;
var links_ = [];
var nodes_ = [];
var progress = 0;
var collecting = true;
export default class Visual extends React.Component {

    constructor() {
        super();
        this.state = {
            width : window.innerWidth-200,
            height : window.innerHeight- 100,
            film_nodes : [],
            char_nodes : [],
            plan_nodes : [],
            nodes : [],

            film_links : [],
            char_links : [],
            plan_links : [],
        }
    }

    visualize(graph) {

        const width = this.state.width;
        const height = this.state.height;

        //Toggle stores whether the highlighting is on
        var toggle = 0;
        var svg = d3.select("#mysvg");

        var color = d3.scaleOrdinal(d3.schemeCategory20);

        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(150))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(width / 2, height / 3))
            .force("collide", d3.forceCollide().radius(function(d) { return d.size * 1.5;}).iterations(2).strength(0.95));

        var link = svg.selectAll(".link")
                      .data(graph.links)
                      .enter().append("line")
                      .attr("class", "links")
                      .style("stroke-width", function(d){return Math.sqrt(d.value);});

        var node = svg.selectAll(".node")
                      .data(graph.nodes)
                      .enter().append("g")
                      .attr("class", "nodes")
                      .call(d3.drag()
                              .on("start", dragstarted)
                              .on("drag", dragged)
                              .on("end", dragended)
                              .on("start.highlight", connectedNodes));
        node.append("circle")
            .attr("id", "mynode")
            .attr("r", function(d) {return d.size;})
            .attr("fill", function(d) { return color(d.group); })
            .append("title")
            .text(function(d) { return d.id; });;

        node.append("text")
            .attr("dx", 10)
            .attr("dy", ".35em")
            .text(function(d) { return d.id; })
            .style("stroke", "white")
            .style("text-shadow", "black 1px 2px")
            .style("font-family", "Raleway, sans-serif");

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        //Create an array logging what is connected to what
        var linkedByIndex = {};
        for (var i = 0; i < graph.nodes.length; i++) {
            linkedByIndex[i + "," + i] = 1;
        };
        graph.links.forEach(function (d) {
            linkedByIndex[d.source.index + "," + d.target.index] = 1;
        });

        function ticked() {
          link
              .attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          d3.selectAll("#mynode")
            .attr("cx", function(d) { return d.x = Math.max(d.size, Math.min(width - d.size, d.x)); })
            .attr("cy", function(d) { return d.y = Math.max(d.size, Math.min(height - d.size, d.y)); });

          d3.selectAll("text")
            .attr("x", function(d) { return d.x; })
            .attr("y", function(d) { return d.y; });
         }

        function dragstarted(d) {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }

        function dragged(d) {
          d.fx = d3.event.x;
          d.fy = d3.event.y;
        }

        function dragended(d) {
          if (!d3.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }

        //This function looks up whether a pair are neighbours
        function neighboring(a, b) {
            return linkedByIndex[a.index + "," + b.index];
        }
        function connectedNodes() {
            if (toggle == 0) {
                reduceNodes(this);
                toggle = 1;

            } else {
                restoreNodes();
                toggle = 0;
            }
        }

        function reduceNodes(item) {
            var d = d3.select(item).node().__data__;
            node.style("opacity", function (o) {
                return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
            });
            link.style("opacity", function (o) {
                return d.index==o.source.index | d.index==o.target.index ? 1 : 0.1;
            });
        }

        function restoreNodes() {
            node.style("opacity", 1);
            link.style("opacity", 1);
        }
    }

    requestData(requestString, target, type) {
        var _this = this;
        var links = [];

        fetch(requestString)
          .then(function(response) {
             if (response.status !== 200) {
                 console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
                   response.status);
             }
             response.json().then(function(responseData) {

                links_.push({source: responseData[0].name, target: target, value: 5});
                link_total++;
                progress += 10;
                _this.setState({p : 5});
                if (link_total === 121) {
                    var graph = {
                                    nodes : _this.state.nodes,
                                    links : links_,
                                };

                    collecting = false;
                    _this.visualize(graph);
                    _this.setState({collecting : false});
                }
                });
             })
           .catch(function(err) {
              console.log('Fetch Error: -S', err);
            });
    }

    componentDidMount() {
    	if (progress === 0){
    		this.buildGraph();
    	}
    	else
    	{
    		var graph = {
    						nodes : nodes_,
    						links : links_,
    					};
    		this.visualize(graph);
    	}
    }


    buildFilmNodes () {
        var _this = this;
        var nodes = [];

        var request;
        // Acquire films
        for (var i = 1; i < 3; i++){
            request = "http://www.thesweawakens.me/api/films/?page=";
            request += i;
            fetch(request)
              .then(function(response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
                      response.status);
                }
                response.json().then(function(responseData) {
                    for (var id in responseData) {
                        const film = responseData[id];
                        nodes.push({id : film.title, group : 7, size: 45});
                        for (var pid in film.planet_list){
                            const planet = film.planet_list[pid];
                            _this.requestData(planet, film.title, "film");
                        }
                    }

                    progress += 15;
                    _this.setState({ film_nodes : nodes });

                    global_total++;

                    if (global_total === 28){
                        console.log("Done.");
                        var final = nodes.concat(_this.state.char_nodes);
                        final = final.concat(_this.state.plan_nodes);
                        nodes_ = final;
                        _this.setState({nodes : final});
                    }

                });
              })
            .catch(function(err) {
                console.log('Fetch Error: -S', err);
              });
        }
    }
    buildPlanetNodes() {
        var _this = this;
        var nodes = [];

        var request;
        // Acquire planets
        for (var i = 1; i < 12; i++){
            request = "http://www.thesweawakens.me/api/planets/?page=";
            request += i;
            fetch(request)
              .then(function(response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
                      response.status);
                }
                response.json().then(function(responseData) {
                    for (var id in responseData) {
                        const planet = responseData[id];
                        nodes.push({id : planet.name, group : 10, size : 20});
                        for (var cid in planet.character_list) {
                            const charr = planet.character_list[cid];
                            _this.requestData(charr, planet.name, "planet");
                        }
                    }

                    progress += 15;
                    _this.setState({ plan_nodes : nodes });
                    global_total++;

                    if (global_total === 28){
                        console.log("Done.");
                        var final = nodes.concat(_this.state.char_nodes);
                        final = final.concat(_this.state.film_nodes);
                        nodes_ = final;
                        _this.setState({nodes : final});
                    }

                });
              })
            .catch(function(err) {
                console.log('Fetch Error: -S', err);
              });
        }
    }
    buildCharNodes() {
        var _this = this;
        var nodes = [];

        var request;
        // Acquire planets
        for (var i = 1; i < 16; i++){
            request = "http://www.thesweawakens.me/api/characters/?page=";
            request += i;
            fetch(request)
              .then(function(response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
                      response.status);
                }
                response.json().then(function(responseData) {
                    for (var id in responseData) {
                        const char = responseData[id];
                        nodes.push({id : char.name, group : 15, size : 10});
                    }

                    progress += 15;
                    _this.setState({ char_nodes : nodes });
                    global_total++;

                    if (global_total === 28){
                        console.log("Done.");
                        var final = nodes.concat(_this.state.plan_nodes);
                        final = final.concat(_this.state.film_nodes);
                        nodes_ = final;
                        _this.setState({nodes : final});
                    }

                });
              })
            .catch(function(err) {
                console.log('Fetch Error: -S', err);
              });
        }

    }
    buildGraph() {
        this.buildFilmNodes();
        this.buildPlanetNodes();
        this.buildCharNodes();
    }

    render() {
        return (
            <div id="stars" class="row">
                <div class="col-lg-1 col-md-1 col-sm-1 col-xs-12">
                  <table id="mytable" class="table table-bordered table-striped">
                    <thead>
                      <tr>
                        <th><h4><center>Legend</center></h4></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>

                        <td>
                        <center>
                        <h5>Movie</h5>
                        <svg height="70" width="70">
                        <circle r="30" fill="#ff7f0e" cx="37" cy="30"><title>Movie</title></circle>
                        </svg>
                        </center>
                        </td>
                      </tr>
                      <tr>
                        <td>
                        <center>
                        <h5>Planet</h5>
                        <svg height="50" width="60">
                        <circle r="20" fill="#aec7e8" cx="30" cy="25"><title>Planet</title></circle>
                        </svg>
                        </center>
                        </td>
                      </tr>
                      <tr>
                        <td>
                        <center>
                        <h5>Character</h5>
                        <svg height="50" width="60">
                        <circle r="10" fill="#1f77b4" cx="30" cy="25"><title>Character</title></circle>
                        </svg>
                        </center>
                        </td>
                      </tr>
                      <tr>
                      <td>
                        <button
                          type="button"
                          class="btn btn-group-justified btn-primary"
                          data-toggle="modal"
                          data-target="#myModal">
                          <p>About</p><div class="glyphicon glyphicon-question-sign"></div>
                        </button>

                        <div id="myModal" class="modal fade" role="dialog">
                          <div class="modal-dialog">
                            <div class="modal-content">
                              <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal">&times;</button>
                                <h4 class="modal-title">About this visualization</h4>
                              </div>
                              <div class="modal-body">
                                <p>This visualization shows the relationships between the movies, planets, and characters of the Star Wars universe.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="col-lg-11 col-md-11 col-sm-11 col-xs-12">
                 	{collecting &&
                 		(<div class="progress">
				  			<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0"
				  				aria-valuemin="0" aria-valuemax="100" style={{width : progress}}>
				  			</div>
				  		</div>)}
                	<svg id="mysvg" width={this.state.width} height={this.state.height}></svg>
                </div>
            </div>
        );
    }
}
