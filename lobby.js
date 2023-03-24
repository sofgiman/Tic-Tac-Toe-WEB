let players;
/**
 * A method that set the lobby enviroment
 * @param {array of players} playersList - current player list
 */
function lobbyInit(playersList) {
  const name = sessionStorage.getItem("name");
  playerName = name; // defining the player name
  players = playersList; // defining the players list
  if (Array.isArray(players)) {
    players.forEach((plyr) => addplayerToList(plyr)); // adding the players to the html file
  }

  document.getElementById("welcomeEntry").style.display = "none"; // the will not see the welcomeEntry
  document.getElementById("lobby").style.display = "block"; // the user will see the lobby
  updateplayerlist = setInterval(updatePlayerList, 1500); // setting an interval that will update the players list
  clientIsOnline = setInterval(clientOnline, 1500); // setting an interval that will send signal the user is active
}

/**
 * A function that re-setting the lobby enviroment when a player return from a game
 */
function reDrawPlayerList() {
  document.getElementById("game").style.display = "none"; // hide the game visual
  document.getElementById("lobby").style.display = "block"; // show the lobby visual
  updateplayerlist = setInterval(updatePlayerList, 1500); // re-creating the interval that update the player list
  document.getElementById("gameProcess").innerText = ""; // resetting the gameProcess element(that shows if the user is waiting for a game)
  document.getElementById("playButton").disabled = false;
}

/**
 * A function that finds a game for the user
 */
function findGame() {
  document.getElementById("playButton").disabled = true;
  const http = new XMLHttpRequest(); // creating an ajax request
  http.open("GET", "/findgame?" + sessionStorage.getItem("name")); // openning a 'findgame' request with the player name
  http.send();
  http.onload = () => {
    /**
     * Getting response from the server that contaings a json object, that includes the player status, and if there is a game id,
     * that way creating the game
     */
    const response = http.responseText;
    const playrsObj = JSON.parse(response);
    const showGameProcessElement = document.getElementById("gameProcess");
    if (playrsObj === "Eror") {
      showGameProcessElement.innerText = "Eror";
    } else {
      if (playrsObj.Status === "Playing") {
        // if status is "Playing" then a game needs to start
        showGameProcessElement.innerText = "Joining the game";
        const gameID = playrsObj.gameID;
        setGameEnivroment(gameID); // creating the game
      } else if (playrsObj.Status === "Waiting") {
        // if status is "Waiting" then a game will start after an opponent willcome
        showGameProcessElement.innerText = "waiting for opponent";
        waitforopponet = setInterval(findOpponet, 1000); // creating an interval that check if there is a matched opponent
      }
    }
  };
}

/**
 * A function that add a player to the players list in the lobby
 */
function addplayerToList(player) {
  const playersListElement = document.getElementById("players"); // the ul at html that contains the list
  const li = document.createElement("li"); // the new li(list)
  let you = "";
  if (player.Name === playerName) {
    you = "(You)";
  }
  li.innerText = `${player.Name}${you} - ${player.Status}`; // setting the new list text
  li.id = player.Name; // setting it's id

  playersListElement.appendChild(li); // appending it to the html file
}

/**
 * A method that send requst to server to get a response of an updated players list
 */
function updatePlayerList() {
  const http = new XMLHttpRequest();
  http.open("GET", "/sendPlayerList"); // openning the request
  http.send(); // sending the request
  http.onload = () => {
    /**
     * Getting a response from the server, which is an json object that contains the updated players list
     */
    const old_players = players; // defining an old players list to know what needs to be updated
    players = JSON.parse(http.responseText);
    if (players.length >= old_players.length) {
      // if there are new players
      for (i = 0; i < old_players.length; i++) {
        // updating the names and statuses of the current players
        let you = "";
        if (players[i].Name === playerName) {
          you = "(You)";
        }
        document.getElementById(
          old_players[i].Name
        ).innerText = `${players[i].Name}${you} - ${players[i].Status}`;
      }
      for (i = 0; i < players.length - old_players.length; i++) {
        addplayerToList(players[old_players.length + i]); // creating the new players
      }
    } else if (players.length < old_players.length) {
      // that meand a player left
      for (i = 0; i < old_players.length; i++) {
        if (checkPlayerOnList(old_players[i].Name, players) === false) {
          // check if the old player is not in the updated playres list
          document
            .getElementById("players")
            .removeChild(document.getElementById(old_players[i].Name)); // remove the player from the html players list
        }
      }
    }
  };
}

/**
 * A function that checks if there is a player on the list given that contains tha name given
 * @param {string} name
 * @param {array of players} list
 * return - true if there is player with the name given on the list, else false
 */
function checkPlayerOnList(name, list) {
  for (index = 0; index < list.length; index++) {
    if (list[index].Name === name) {
      return true;
    }
  }
  return false;
}

/**
 * A function that finds an opponent to the user
 */
function findOpponet() {
  const http = new XMLHttpRequest();
  http.open("GET", "/opponentAvailable?" + sessionStorage.getItem("name")); // sending a request to checks if there are opponent
  http.send();

  http.onload = () => {
    /**
     * The response is a json type that contains the current player status and if there is, a game id; that way checks if the player found a game
     */
    const player = JSON.parse(http.responseText);
    if (player.Status === "Playing") {
      // if player is playing he need to be in a a game
      const showGameProcessElement = document.getElementById("gameProcess");
      showGameProcessElement.innerText = "joining the game";
      clearInterval(waitforopponet); // clear the interval
      gameID = player.gameID; // defining the game id
      setGameEnivroment(gameID);
    }
  };
}

/**
 * A funcion that create the game
 * @param {int} gameID
 */
function setGameEnivroment(gameID) {
  sessionStorage.setItem("ID", gameID); // setting the game id in the session storage, that way it's possible to knew what game user was in he refresh the page
  document.getElementById("lobby").style.display = "none";
  document.getElementById("game").style.display = "block";
  clearInterval(updateplayerlist); // stop updating the players list
  game();
}

/**
 * A fucntion that send signals to the servers that the player is online
 */
function clientOnline() {
  const data = {
    name: sessionStorage.getItem("name"),
  };
  const http = new XMLHttpRequest();
  http.open("GET", "/playerOnApp?" + JSON.stringify(data));
  http.send();
  console.log("sent");

  
}

/**
 * A function whose purpose is to handle a refresh page when player is on lobby or on a game; if he is on lobby putting him on lobby,
 * if he is on a game, putting him into that game
 */
function onloadInit() {
  if (sessionStorage.getItem("name") !== null) {
    // player is on lobby or in game
    playerName = sessionStorage.getItem("name");
    clientIsOnline = setInterval(clientOnline, 1500); // re-creating the interval
    const http = new XMLHttpRequest();
    http.open("GET", "/sendPlayerList"); // sending a request to have the playrs list
    http.send();
    http.onload = () => {
      /**
       * getting a json object from the response, the object is the current players list
       */
      players = JSON.parse(http.responseText);
      if (Array.isArray(players)) {
        players.forEach((plyr) => {
          addplayerToList(plyr); // adding the playrs to the html file
          if (plyr.Name === playerName) {
            if (plyr.Status === "Waiting") {
              // if user is waiting for an opponent
              document.getElementById("playButton").disabled = true;
              waitforopponet = setInterval(findOpponet, 1000); // set interval that checks for an opponent
              const showGameProcessElement = document.getElementById(
                "gameProcess"
              );
              showGameProcessElement.innerText = "waiting for opponent";
            }
          }
        });
      }
      if (sessionStorage.getItem("ID") === null) {
        // if the player is not on a game
        document.getElementById("welcomeEntry").style.display = "none";
        document.getElementById("lobby").style.display = "block"; // the player is on lobby
        updateplayerlist = setInterval(updatePlayerList, 1500);
      }
    };
    if (sessionStorage.getItem("ID") !== null) {
      // if player is on a game
      document.getElementById("welcomeEntry").style.display = "none";
      document.getElementById("game").style.display = "block";
      refreshGame(); // refreshing the game
    }
  }
}
