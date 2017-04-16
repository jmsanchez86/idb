import Dispatcher from "../Dispatcher";

export function searchSubmit(value) {
  Dispatcher.dispatch({type: "SEARCH_REQUEST", value});
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
        // console.log(_data);
        // console.log(_links);
        const obj = {data: _data, links: _links};
        console.log(obj);
        Dispatcher.dispatch({type:"SEARCH_RESPONSE", obj});

      });
    })
  .catch(function(err) {
      console.log('Fetch Error: -S', err);
      Dispatcher.dispatch({type:"SEARCH_ERROR", err});
    });

}

export function responseReturned(response) {
  Dispatcher.dispatch(
    {
      type:"SEARCH_RESPONSE",
      response
    }
  )
}
