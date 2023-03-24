/**
 * A file that represent the entry, what player sees at the start
 */

/**
 * A method that send the name to server
 */
function sendYourName() {
  document.getElementById("entryNameButton").disabled = true; // diabling that the user won't be able to spam the sendYourName button
  document.getElementById("nameTakenLabel").innerText = "";

  const nameElement = document.getElementById("name");
  const name = nameElement.value;
  const http = new XMLHttpRequest(); // creating an ajax request that will be send to the server
  http.open("GET", "/insertname?" + name); // open a request that will insert a name to the game
  http.send(); // sending the request
  http.onload = () => {
    /**
     * handling the response; the response will come from the server as an json object and will include two things:
     * that if the name is already taken and the current playres list
     */
    const entryData = JSON.parse(http.responseText); // parsing the json object
    if (entryData.nameIsTaken !== true) {
      // if name isn't taken
      sessionStorage.setItem("name", name); // setting the name is session storage
      lobbyInit(entryData.playersList);
    } else {
      // if name is taken showing to the user that it is taken and he need to choose a new one
      document.getElementById("nameTakenLabel").innerText =
        'the name "' + name + '" is already taken';
      document.getElementById("entryNameButton").disabled = false;
    }
  };
}
