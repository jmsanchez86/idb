import Dispatcher from "../Dispatcher";

export function searchSubmit(value) {
  Dispatcher.dispatch({type: "SEARCH_REQUEST", value});
}

export function urlRequest(query) {
  Dispatcher.dispatch({type: "URL_REQUEST", query});
}
