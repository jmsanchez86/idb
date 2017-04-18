import { EventEmitter } from "events";
import Dispatcher from "../Dispatcher";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.values = "";
    this.response = {data: [], links:{}};
    this.err = "";
    
    }


  handleRequest(obj) {
    console.log(obj);
  }
  handleResponse(response) {
    this.response = response;
    console.log(this.response);
    this.emit("change");
  }
  getData() {
    return this.response.data;
  }
  getLinks() {
    return this.response.links;
  }

  handleError(obj) {
    console.log(obj);
  }

  handleAction(action) {
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
