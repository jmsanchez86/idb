import { EventEmitter } from "events";
import Dispatcher from "../Dispatcher";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.state = {data: [], links:{}, value: ""};
    this.err = "";
  }

  getQuery(sanitizedValue) {
    return "http://api.vennfridge.appspot.com/search?q=" + sanitizedValue;
  }
  sanitizeString(value) {
    return value.replace(/[^\w\s-']/gi, '').trim().replace(/ +/gi, '+').toLowerCase();
  }
  searchRequest(value) {
    const query = this.getQuery(this.sanitizeString(value));
    this.urlRequest(query, value);
  }

  urlRequest(query, value) {
    var _data = {};
    var _links = {};
    value = value ? value : this.state.value;
    // call api with new query params
    fetch(query)
      .then(function(response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem loading vennfridge info. Status Code: ' +
              response.status);
        }
        response.json().then(function(responseData) {
          for (var context in responseData.data){
            _data[context] = responseData.data[context];
          }
          for (var elem in responseData.links){
            _links[elem] = responseData.links[elem];
          }
          const obj = {data: _data, links: _links, value: value};
          Dispatcher.dispatch({type:"RESPONSE", obj});
        });
      })
    .catch(function(err) {
        console.log('Fetch Error: -S', err);
        Dispatcher.dispatch({type:"SEARCH_ERROR", err});
      });
  }

  handleResponse(response) {
    this.state = response;
    this.emit("change");
  }
  getData() {
    return this.state.data;
  }
  getLinks() {
    return this.state.links;
  }
  getValue() {
    return this.state.value;
  }
  handleError(obj) {
  }

  handleAction(action) {
    switch(action.type) {
      case "SEARCH_REQUEST": {
        this.searchRequest(action.value);
        break;
      }
      case "URL_REQUEST": {
        this.urlRequest(action.query);
        break;
      }
      case "RESPONSE": {
        this.handleResponse(action.obj);
        break;
      }
      case "SEARCH_ERROR": {
        this.handleError(action.err);
        break;
      }
    }
  }
}

const searchStore = new SearchStore;
Dispatcher.register(searchStore.handleAction.bind(searchStore));
export default searchStore;
