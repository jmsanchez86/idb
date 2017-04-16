import { EventEmitter } from "events";
import Dispatcher from "../Dispatcher";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.state = {
      value: "",
    }
  }

  handleAction(action) {
    switch(action.type) {
      case "SEARCH": {
        this.searchValue(action.value);
      }
    }
  }

  searchValue(value) {
    console.log(value);
    var _this = this;
    var _data = {};
    var _links = {};

    // call api with new query params
    fetch("http://api.vennfridge.appspot.com/search?q=test")
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
          console.log(_data);
          console.log(_links);
          // _this.state.data = _data;
          // _this.state.links = _links;
          // _this.forceUpdate();

        });
      })
    .catch(function(err) {
        console.log('Fetch Error: -S', err);
      });
  }



}

const searchStore = new SearchStore;
Dispatcher.register(searchStore.handleAction.bind(searchStore));
window.Dispatcher = Dispatcher;
export default searchStore;
