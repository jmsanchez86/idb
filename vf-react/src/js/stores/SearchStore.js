import { EventEmitter } from "events";
import Dispatcher from "../Dispatcher";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.response = {data: [], links:{}};
    this.err = "";
  }

  sanitizeString(value) {
    return value.replace(/[^\w\s-']/gi, '').trim().replace(/ +/gi, '+').toLowerCase();
  }
  handleRequest(value) {
    this.value = value;
    const query = this.sanitizeString(value);
    var _data = {};
    var _links = {};
    // call api with new query params
    fetch("http://api.vennfridge.appspot.com/search?q="+query)
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
          Dispatcher.dispatch({type:"SEARCH_RESPONSE", obj});
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
        this.handleRequest(action.value);
        break;
      }
      case "SEARCH_RESPONSE": {
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
