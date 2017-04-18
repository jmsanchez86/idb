import { EventEmitter } from "events";
import Dispatcher from "../Dispatcher";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.response = {data: [], links:{}};
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
    console.log(query);
    this.urlRequest(query, value);
  }

  urlRequest(query, value) {
    var _data = {};
    var _links = {};
    value = value ? value : this.value;
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
    this.response = response;
    this.emit("change");
  }
  getData() {
    return this.response.data;
  }
  getLinks() {
    return this.response.links;
  }
  getValue() {
    return this.response.value;
  }
  handleError(obj) {
    console.log(obj);
  }

  handleAction(action) {
    console.log(action);
    switch(action.type) {
      case "SEARCH_REQUEST": {
        this.searchRequest(action.value);
        break;
      }
      case "URL_REQUEST": {
        console.log(action.query);
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
