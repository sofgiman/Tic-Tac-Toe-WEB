/**
 * A file who represent the game
 */

let typeOfPlayer;  // the client type (player1 or player2)
let turn;  // true or false if it's players turn
let type;  // 'X' or 'O'
//let playerNum;  // playerX; x = 1||2
let board;  // two deminsion array that contain the table data
let gameID;  // the game id 
let playerName;  // the name of the player

/**
 *
 */
function game() {
  const welcome1 = document.getElementById("welcome1");
  const welcome2 = document.getElementById("welcome2");
  playerName = "user";
  if (sessionStorage.getItem("name") !== null) {
    playerName = sessionStorage.getItem("name");
  }
  gameID = sessionStorage.getItem("ID");

  type = null;
  board = [
    [null, null, null],
    [null, null, null],
    [null, null, null],
  ];
  enableButtons();
  myVar = setInterval(checkMyTurn, 1000); // intreval that cheks if it's the playr  turn
  informPlayerTurn = setInterval(writeWaitingForOpponetRespone, 400);  // if it's not player turn there will be animation telling him 
  const http = new XMLHttpRequest();  // creating an ajax reqest
  const data = {  // preparing to send the game id and player's name 
    name: playerName,  
    ID: gameID,
  };

  http.open("GET", "/init?" + JSON.stringify(data));  // sending an init + the data to know enough about the game to create it
  http.send();
  http.onload = handleHttpLoad;

  /**
   * The function that handle the response; the response will be a json objet that contains the type of playr,
   * the type of 'X''O',  the opponent name
   * @param {string} eventLoad 
   */
  function handleHttpLoad(eventLoad) {
    player_data = JSON.parse(eventLoad.currentTarget.responseText);
    typeOfPlayer = player_data.clientType;
    const opponentName = player_data.opponentName;
    type = player_data.playerType;
    let opponentType;
    if (type === "X") {  // 'X' is always starting
      opponentType = "O";
      turn = true;
    } else {
      opponentType = "X";
      turn = false;
    }
    if (type !== null) {
      console.log("You: " + playerName + "(" + type + ")");
      welcome1.innerText =
        "You: " +
        playerName +
        "(" +
        type +
        ")";
        welcome2.innerText = 
        "vs " +
        opponentName +
        "(" +
        opponentType +
        ")";
    } else welcome.innerText = "You Are: " + typeOfPlayer;
  }
}
/**
 * A function that asks the server if it's the playrs turn
 */
function checkMyTurn() {
  if (turn !== true) {  // if it's not its than the server will be asked
    disapleAllButton();  // making that the player won't be able to press a button
    const data = {
      id: gameID,
      player: typeOfPlayer,
    };
    const http = new XMLHttpRequest();
    http.open("GET", "/isTurn?" + JSON.stringify(data));  // sendin a request to ask if it's the turn now for that player in the game id game
    http.send();
    /**
     * A method that handle the respone; the response will have two things: if it's the playrs turn and 
     * if so, the updated board, and also if there's a winner 
     */
    http.onload = () => {
      gameData = JSON.parse(http.responseText);  // parsing the response
      if (gameData.is_turn === true) {  
        turn = true;
        document.getElementById("turnCheckButton").innerText = "Your turn!";
        const updatedBoard = gameData.board;  // getting board data
        fixArray(updatedBoard);  // updating the board array
        enableButtons(); 
        const won = gameData.won;
        checkWin(won);  // always check if there is a winner
      } else {
        const won = gameData.won;  // always check if there is a winner
        checkWin(won);
      }
    };
  } else {
    document.getElementById("turnCheckButton").innerText = "Your turn!";
  }
}

let dotStr = "";
/**
 * A function that show the opponent that he is wating for opponent turn to be played
 */
function writeWaitingForOpponetRespone() {
  if (turn !== true) {
    document.getElementById("turnCheckButton").innerText =
      "Waiting for opponent response" + dotStr;
    if (dotStr == "") dotStr = ".";
    else if (dotStr == ".") dotStr = "..";
    else if (dotStr == "..") dotStr = "...";
    else if (dotStr == "...") dotStr = "";
  }
}

/**
 * A function that handle a button click
 * @param {button} btn  - the pressed button
 */
function handleButtonNumberClick(btn) {
  const disabledAtt = btn.getAttribute("disabled");
  if (turn === true && disabledAtt === "false") {   // if it's the player turn the button hasn't been pressed yet then the click is ok
    handleButtonClick(btn); //
  }
}

/**
 * A method the handle the button pressed
 * @param {button} buttonNumber 
 */
function handleButtonClick(buttonNumber) {
  const http = new XMLHttpRequest();
  const data = {  // need to send the game id and the button number so the server could handle that
    id: gameID,
    buttonNumber: buttonNumber.id,
  };

  http.open("GET", "/buttonClick?" + JSON.stringify(data));  
  http.send();
  disapleAllButton();  // disabling al button cause turn has been played
  console.log("boars");
  /**
   * Handling the response; that contains the updated board, if there's a winner an the button who been pressed 
   */
  http.onload = () => {
    const response = JSON.parse(http.responseText);
    const updatedBoard = response.board;
    board = updatedBoard;
    const buttonClicked = response.buttonClick;
    const won = response.won;

    document.getElementById(buttonClicked).innerText = type;
    checkWin(won);  // checking if there's a winner
    turn = false;
  };
}

/**
 * A function that get an updated board and update what the user sees
 * @param {two dimensions array} updatedBoard 
 */
function fixArray(updatedBoard) {
  let index = 1;
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++, index++) {
      board[i][j] = updatedBoard[i][j];
      if (board[i][j] == "O" || board[i][j] == "X") {
        document.getElementById(index).innerText = board[i][j];
      }
    }
  }
}

/**
 * A method that prevent from the user to click on the buttons
 */
function disapleAllButton() {
  for (i = 1; i < 10; i++) {
    document.getElementById(i).setAttribute("disabled", "true");  // that way he can't press the div
  }
}

/**
 * A method that enable buttons who hasn't been pressed yet to be pressed 
 */
function enableButtons() {
  for (i = 0; i < 9; i++) {
    const loc = caculateLoc(i);
    if (board[loc[0]][loc[1]] !== "X" && board[loc[0]][loc[1]] !== "O") {
      document.getElementById(i + 1).setAttribute("disabled", "false");
    }
  }
}

/**
 * A method that convert one deminsion index to two deminsions index
 * @param {index} loc 
 * return - two demindion index
 */
function caculateLoc(loc) {
  const loc_cells = [
    [0, 0],
    [0, 1],
    [0, 2],
    [1, 0],
    [1, 1],
    [1, 2],
    [2, 0],
    [2, 1],
    [2, 2],
  ];
  return loc_cells[loc];
}

/**
 * A function that checks if there a winner, or a tie
 * @param {string} won 
 */
function checkWin(won) {
  if (won !== null) {  // that means there is a tie or a winner
    if (won === "Tie") {  // if tie
      document.getElementById("win_state").innerText = won;
    } else {
      if (won === type) // there's a winner
        document.getElementById("win_state").innerText =  // if it's the player 'X' or 'O' type than he is the winner
          "You are the winner!!!";
      else document.getElementById("win_state").innerText = "You are the loser"; // else he los't
    }
    document.getElementById("Texts").style.display = "block";  // let the player be back to the lobby 
    disapleAllButton();  // disabling the button for secure
    clearInterval(myVar);  // clearing the active intervals
    clearInterval(informPlayerTurn);  
  }
}

/**
 * A function the ending the game; it's purpose is to delete the game from the server
 */
function endGame() {
  const data = {  
    id: gameID,
    player: typeOfPlayer,
    name: playerName,
  };
  const http = new XMLHttpRequest();
  http.open("GET", "/endGame?" + JSON.stringify(data));  // sending the game id and who left
  http.send();
  http.onload = () => {
    console.log("game finished");
  };
}

/**
 * A function that handle when the player want to go back to lobby
 */
function toLobby() {
  endGame();  // ending game
  for (i = 1; i < 10; i++) {
    document.getElementById(i).innerText = null;  // making all buttons text null(back to original)
  }
  document.getElementById("Texts").style.display = "none";  
  sessionStorage.removeItem("ID");  // removing the game id from session, because he isn't active
  reDrawPlayerList(); // back to lobby
}

/**
 * A function that handle when the user refresh the page when he is on a game
 */
function refreshGame() {
  gameID = sessionStorage.getItem("ID");
  const game_data = {
    name: playerName,
    ID: gameID,
  };
  const http = new XMLHttpRequest();
  http.open("GET", "/refreshGameData?" + JSON.stringify(game_data));  // sending the server the data 
  http.send();
  /**
   * A function that handle the respone to be able to be back in the game; the response contain the type of player, the turn,
   * the type('X' or 'O'), an updated board, if ther's a winner and the opponent name
   */
  http.onload = () => {
    const data = JSON.parse(http.responseText);
    typeOfPlayer = data.typeOfPlayer;
    turn = data.turn;
    type = data.type;
    board = data.board;
    const won = data.won;
    const opponentName = data.opponentName;
    fixArray(board);  // fixing what user sees
    if (turn === true) {  
      disapleAllButton();
      enableButtons();
    }

    myVar = setInterval(checkMyTurn, 1000);  // re-creating intrevals
    informPlayerTurn = setInterval(writeWaitingForOpponetRespone, 400);

    let opponentType;
    if (type === "X") {
      opponentType = "O";
    } else {
      opponentType = "X";
    }
    if (type !== null) {
      welcome1.innerText =
        "You: " +
        playerName +
        "(" +
        type +
        ")" ;
        welcome2.innerText = "vs " +
        opponentName +
        "(" +
        opponentType +
        ")";
    } else welcome1.innerText = "You Are: " + typeOfPlayer;
    checkWin(won);  // checks if there's a winner
  };
}
