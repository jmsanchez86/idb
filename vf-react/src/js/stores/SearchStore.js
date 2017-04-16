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
        console.log(action.value);
      }
    }
  }


}

const searchStore = new SearchStore;
Dispatcher.register(searchStore.handleAction.bind(searchStore));
window.Dispatcher = Dispatcher;
export default searchStore;
