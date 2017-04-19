import React from "react";

import * as d3 from "d3";

var film_total = 0;
var planet_total = 0;
var char_total = 0;
var global_total = 0;

var link_total = 0;
var links_ = [];
export default class Visual extends React.Component {
	constructor() {
		super();
		this.state = {
		    width : 1536,
			height : 759,

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

		var radius;
		var svg = d3.select("svg");
		

		var color = d3.scaleOrdinal(d3.schemeCategory20);

		var simulation = d3.forceSimulation()
		    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(150))
		    .force("charge", d3.forceManyBody().strength(-15))
		    .force("center", d3.forceCenter(this.state.width / 2, this.state.height / 3))
		    .force("collide", d3.forceCollide().radius(1).iterations(2));
		

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
					  		  .on("end", dragended));

		node.append("circle")
			.attr("r", function(d) { d.film ? radius=50 : radius=20; return radius;})
			.attr("fill", function(d) { return color(d.group); })
		    .append("title")
		    .text(function(d) { return d.id; });;

		
		node.append("text")
		   	.attr("dx", 10)
      		.attr("dy", ".35em")
		    .text(function(d) { return d.id; })
		    .style("stroke", "black");


		simulation
		    .nodes(graph.nodes)
		    .on("tick", ticked);

		simulation.force("link")
		    .links(graph.links);

	
		function ticked() {
		  link
		      .attr("x1", function(d) { return d.source.x; })
		      .attr("y1", function(d) { return d.source.y; })
		      .attr("x2", function(d) { return d.target.x; })
		      .attr("y2", function(d) { return d.target.y; });

		  d3.selectAll("circle")
		  	.attr("cx", function(d) { return d.x; })
		  	.attr("cy", function(d) { return d.y; });

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
		    	 
		    	if (link_total === 121) {
		    		var graph = {
		    						nodes : _this.state.nodes,
		    						links : links_,
		    					};
		    		_this.visualize(graph);
		    	}
		    	});
		     })
		   .catch(function(err) {
		      console.log('Fetch Error: -S', err);
		    });
	}

	componentDidMount() {
		this.buildGraph();
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
		    			nodes.push({id : film.title, group : film.episode_no, film : true});
		    			for (var pid in film.planet_list){
		    				const planet = film.planet_list[pid];
		    				_this.requestData(planet, film.title, "film");
		    			}
		    		}	

		    		_this.setState({ film_nodes : nodes });
		    		film_total++;
		    		global_total++;
		    	
		    		if (global_total === 28){
		    			console.log("Done.");
		    			var final = nodes.concat(_this.state.char_nodes);
		    			final = final.concat(_this.state.plan_nodes);
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
		    			nodes.push({id : planet.name, group : 10, film : false});
		    			for (var cid in planet.character_list) {
		    				const charr = planet.character_list[cid];
		    				_this.requestData(charr, planet.name, "planet");
		    			}
		    		}	

		    		_this.setState({ plan_nodes : nodes });
		    		planet_total++;
		    		global_total++;
		    	
		    		if (global_total === 28){
		    			console.log("Done.");
		    			var final = nodes.concat(_this.state.char_nodes);
		    			final = final.concat(_this.state.film_nodes);
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
		    			nodes.push({id : char.name, group : 15, film : false});
		    		}	

		    		_this.setState({ char_nodes : nodes });
		    		char_total++;
		    		global_total++;
		    		
		    		if (global_total === 28){
		    			console.log("Done.");
		    			var final = nodes.concat(_this.state.plan_nodes);
		    			final = final.concat(_this.state.film_nodes);
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
			<svg width={this.state.width} height={this.state.height}></svg>
		);
	}
}