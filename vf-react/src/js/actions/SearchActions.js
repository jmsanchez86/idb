import Dispatcher from "../Dispatcher";

export function searchSubmit(value) {
  Dispatcher.dispatch({type: "SEARCH_REQUEST", value});
}
