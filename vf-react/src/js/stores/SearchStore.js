import { EventEmitter } from "events";

class SearchStore extends EventEmitter {
  constructor() {
    super();
    this.state = {
      value: "",
    }
  }
  test() {
    alert("SearchStore");
  }


}

const searchStore = new SearchStore;
export default searchStore;
