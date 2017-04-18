import React from "react";

import * as d3 from "d3";

var total = 0;
export default class Visual extends React.Component {
	constructor() {
		super();
		this.state = {
			count : 0,
			width : 1920,
			height : 1080,
			end : 0,
			graph : { 	
						nodes : [{id : "Hello", group : 10, film : true},
								 {id : "World", group : 10, film : false}], 
						links : [{source : "World", target : "Hello", value : 5}]
					},
			final_graph : {
							 nodes : [],
							 links : []
						  },
		}
	}

	visualize(graph) {

		var radius;
		var svg = d3.select("svg");
		

		var color = d3.scaleOrdinal(d3.schemeCategory20);

		var simulation = d3.forceSimulation()
		    .force("link", d3.forceLink().id(function(d) { return d.id; }))
		    .force("charge", d3.forceManyBody())
		    .force("center", d3.forceCenter(this.state.width / 2, this.state.height / 2));
		

		var link = svg.append("g")
		    .attr("class", "links")
		  .selectAll("line")
		  .data(graph.links)
		  .enter().append("line")
		    .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

		var node = svg.append("g")
		    .attr("class", "nodes")
		  .selectAll("circle")
		  .data(graph.nodes)
		  .enter().append("circle")
		    .attr("r", function(d) { d.film ? radius=15 : radius=9; return radius;})
		    .attr("fill", function(d) { return color(d.group); })
		    .call(d3.drag()
		        .on("start", dragstarted)
		        .on("drag", dragged)
		        .on("end", dragended));

		node.append("title")
		    .text(function(d) { return d.id; });

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

		  node
		      .attr("cx", function(d) { return d.x; })
		      .attr("cy", function(d) { return d.y; });
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

	requestData(requestString, graph, film, group) {
		var _this = this;
		var count = _this.state.count++;
		fetch(requestString)
		  .then(function(response) {
		     if (response.status !== 200) {
		         console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
		           response.status);
		     }
		     response.json().then(function(responseData) {
		      //console.log(responseData);
		    	for (var id in responseData) {
		    		const item = responseData[id];
		    		
		    		console.log({id : item.name, group : group, film : false});
		    		graph.nodes.push({id : item.name, group : group, film : false});

		    		console.log({source : item.name, target : film, value : 5 });
		    		graph.links.push({source : item.name, target : film, value : 5 });
		    	}	

		    	    _this.setState({ final_graph : graph, count: count });
		    	    console.log(_this.state.final_graph);
		    	    console.log("Count");
		    	    console.log(_this.state.count);
		    	    total++;
		    	    console.log("Total");
		    	    console.log(total);
		    	    if (total === 34) {
		    	    	var setme = new Set(_this.state.final_graph.nodes);
		    	    	console.log(setme);
		    	    	_this.buildGraph(_this.state.final_graph);
		    	    }
		    	});
		     })
		   .catch(function(err) {
		      console.log('Fetch Error: -S', err);
		    });
	}

	componentDidMount() {
		var _this = this;
		var graph = {
			nodes : [],
			links : []
		};
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
		        console.log(request);
		        response.json().then(function(responseData) {
		    		for (var id in responseData) {
		    			const film = responseData[id];
		    			graph.nodes.push({id : film.title, group : film.episode_no, film : true});
		    			for (var pid in film.planet_list) {
		    				const planet = film.planet_list[pid];
		    				_this.requestData(planet, graph, film.title, film.episode_no);
		    			}
		    		}	

		    		_this.setState({ final_graph : graph});

		        });
		      })
		    .catch(function(err) {
		        console.log('Fetch Error: -S', err);
		      });
		}
	}

	buildGraph(graph) {
		this.visualize(graph);
	}

	render() {
		return (
			<div class="container">
			<svg width={this.state.width} height={this.state.height}>
			</svg>
			</div>
		);
	}
}