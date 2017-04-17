import React from "react";

import * as d3 from "d3";

export default class Visual extends React.Component {
	constructor() {
		super();
		this.state = {
			width : 500,
			height : 500,
			graph : { 	
						nodes : [], 
						links : []
					},
		}
	}

	visualize() {
		var svg = d3.select("svg");
		

		var color = d3.scaleOrdinal(d3.schemeCategory20);

		var simulation = d3.forceSimulation()
		    .force("link", d3.forceLink().id(function(d) { return d.id; }))
		    .force("charge", d3.forceManyBody())
		    .force("center", d3.forceCenter(this.state.width / 2, this.state.height / 2));
		

		var link = svg.append("g")
		    .attr("class", "links")
		  .selectAll("line")
		  .data(this.state.graph.links)
		  .enter().append("line")
		    .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

		var node = svg.append("g")
		    .attr("class", "nodes")
		  .selectAll("circle")
		  .data(this.state.graph.nodes)
		  .enter().append("circle")
		    .attr("r", 5)
		    .attr("fill", function(d) { return color(d.group); })
		    .call(d3.drag()
		        .on("start", dragstarted)
		        .on("drag", dragged)
		        .on("end", dragended));

		node.append("title")
		    .text(function(d) { return d.id; });

		simulation
		    .nodes(this.state.graph.nodes)
		    .on("tick", ticked);

		simulation.force("link")
		    .links(this.state.graph.links);

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

	componentDidMount() {
		var _this = this;
		var graph = {
			nodes : [],
			links : []
		};

		/*var myHeaders = new Headers();

		var myInit = { method: 'GET',
		               headers: myHeaders,
		               mode: 'cors',
		               cache: 'default' };*/

		fetch("http://www.thesweawakens.me/api/films")
	      .then(function(response) {
	        if (response.status !== 200) {
	            console.log('Looks like there was a problem loading sweawakens info. Status Code: ' +
	              response.status);
	        }
	        response.json().then(function(responseData) {
	        	console.log(responseData);
	    		for (var film in responseData) {
	    			graph.nodes.push({id : responseData[film].title, group : responseData[film].episode_no});
	    		}	

	    		_this.setState({
	    		
	    			graph : graph
	    		
	    		});
	    		
	    		_this.visualize();

	        });
	      })
	    .catch(function(err) {
	        console.log('Fetch Error: -S', err);
	      });
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