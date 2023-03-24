import http.server
import socketserver
import json
from http import HTTPStatus
from classes.Player import Player
from classes.Board import Board
from classes.Game import Game
from urllib import parse
from datetime import datetime

"""
The server file
"""

# game: Game = None
# players_modes = {"player 1": 'X',
#                 "player 2": 'O'}

players = []  # the players list
# the players names list( this list exists to check if a name that user inputted is already taken)
players_names = []
games = []  # the games list
# board = Board()
waitingForGame = []  # the player that waiting for a game is on that list, and his opponent will be there until their match created


# playerturn = 1


def convert_players_list_to_json(players):
    """
    get the players list in return an json object that contains the list
    :param players: the players list
    :return: a json list object that contains the players
    """
    names_statuses = []  # both names and statuses list
    names, statuses = [], []
    for player in players:
        names.append(player.name)  # appending each player name
        statuses.append(player.status)  # appending each player status
        print(players[0].name)
        names_statuses = [{"Name": n, "Status": s} for n, s in
                          zip(names, statuses)]  # converting all the list into a readable json object
    return names_statuses


def getIndexPlayersNamesByName(name):
    """
    A function that return a index of the names list, that the names[index] equal to that name
    :param name: the player
    :return: the index of the names list; if name not found return -1
    """
    i = 0
    for player_name in players_names:
        if player_name == name:
            return i
        i += 1
    return -1


def getIndexGameByID(game_id):
    """
    A function that return a index of the games list by game id, that the games[index].id equal to that id
    :param game_id:
    :return: the index of the games list; if id not found return -1
    """
    game_id = int(game_id)
    i = 0
    for game in games:
        if game.id == game_id:
            return i
        i += 1
    return -1


def getIndexGameByName(name):
    """
    A function that return a index of the games list by a player name, that the one of the
    players name at games[index] equal to that name
    :param name: a player name
    :return: the index of the games list; if id not found return -1
    """
    i = 0
    for game in games:
        if (game.player1.name == name or game.player2.name == name) and game.game_live == True:
            return i
        i += 1
    return -1


def is_name_taken(name):
    """
    A function that checks if a name is already taken in the names list
    :param name: a player name user want to have
    :return: True if name is taken, else return False
    """
    for player_name in players_names:
        if player_name == name:
            return True
    return False


def getIndexPlayerByName(name):
    """
    A function that return a index of the players that the player's name in that index equal to the name given
    :param name: player name
    :return: the index at the players list, if not found return -1
    """
    i = 0
    for player in players:
        if player.name == name:
            return i
        i += 1
    return -1


def check_need_to_remove_players():
    """
    A function that checks if a player didn't send a signal that he is online, if so removing him
    """
    indexes_to_remove = []  # the indexes at the players list that needed to be removed
    index = 0
    for player in players:
        # if a signal wasn't sent for more than 60 second, the players will be removed
        if (datetime.now() - player.disconnect_period).total_seconds() > 60:
            indexes_to_remove.append(index)
        index += 1
    remove_player_by_indexes(indexes_to_remove)  # removes that players


def remove_player_by_indexes(indexes_to_remove):
    """
    A function that removes players from the players list by indexes given
    :param indexes_to_remove: a list that contains indexed of players needed to be removed from the list
    """
    global waitingForGame
    num_player_removes = 0  # num of the players that had been removed
    for player_index in indexes_to_remove:
        name = players[player_index - num_player_removes].name
        game_index = getIndexGameByName(name)
        if game_index != -1:  # checking if there is game that needed to be removes
            games[game_index].player_leave_by_name(
                name)  # throw the player from the game
            # if the two players left the game
            if games[game_index].on_game["player1"] == False and games[game_index].on_game["player2"] == False:
                del games[game_index]  # remove the game
            else:
                # make the opponent the winner
                if games[game_index].get_player_by_name(name).type == 'X':
                    games[game_index].won = 'O'
                else:
                    games[game_index].won = 'X'
        name_index = getIndexPlayersNamesByName(name)
        # remove the player name from the names list
        del players_names[name_index]
        # remove the player from the players list
        del players[player_index - num_player_removes]
        if len(waitingForGame) != 0:
            if waitingForGame[0].name == name:
                waitingForGame = []


class Handler(http.server.SimpleHTTPRequestHandler):
    # http request handler
    # handle all request from client

    def do_GET(self):
        """
        A function that handles all of the get request from the client
        """
        global players
        global players_names
        # global won
        global waitingForGame
        global games
        client_type = "VIEWER"
        if self.path[:6] == '/init?':  # if it's init the the client want data to create the game
            data = self.path[6:]  # slicing string in order to get the json object data
            data = parse.unquote(data)  # unquote the data body
            data = json.loads(data)  # parse the json data to an python data
            name = data["name"]  # player's name
            gameID = data["ID"]  # game id
            player_type = None
            opponent_name = None
            game_index = getIndexGameByID(gameID)  # getting the game index
            if games[game_index].player1.name == name:
                client_type = "PLAYER1"  # setting player client type
                player_type = games[game_index].player1.type  # setting player 'X' 'O' type
                opponent_name = games[game_index].player2.name  # setting opponent name
            elif games[game_index].player2.name == name:
                client_type = "PLAYER2"
                player_type = games[game_index].player2.type
                opponent_name = games[game_index].player1.name
            player_data = {"clientType": client_type,
                           "playerType": player_type, "opponentName": opponent_name}  # converting data to json
            self.send_response(HTTPStatus.OK)  # send that all ok
            self.end_headers()  # end headers
            self.wfile.write(bytes(json.dumps(player_data), "utf-8"))  # send the data to client
        elif self.path[:12] == '/insertname?':  # handle if a new name has been inserted
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            name = self.path[12:]
            name_is_taken = False
            players_list = None
            if is_name_taken(name):
                name_is_taken = True  # name is taken
            else:
                players_names.append(name)  # adding the player name to names
                players.append(Player(None, name))  # creating the player
                players_list = convert_players_list_to_json(players)  # getting current players list
            entryData = {"nameIsTaken": name_is_taken,
                         "playersList": players_list}  # convert to json
            self.wfile.write(bytes(json.dumps(entryData), "utf-8"))  # send data
        elif self.path == '/sendPlayerList':  # if client ask for the current playrs list
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            check_need_to_remove_players()  # each ask check if a player need to be deleted
            names_statuses = convert_players_list_to_json(players)
            self.wfile.write(bytes(json.dumps(names_statuses), "utf-8"))
        elif (self.path[:19] == '/opponentAvailable?'):  # when a player is waiting for opponent
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            name = self.path[19:]  # getting player name
            player_index = getIndexPlayerByName(name)
            gameID = None
            game_index = getIndexGameByName(name)
            if game_index != -1:  # check that a game was created, if so there's an opponent
                gameID = games[game_index].id  # getting the game id
            new_player = {"Name": players[player_index].name, "Type": players[player_index].type,
                          "Status": players[player_index].status, "gameID": gameID}  # convert data to json
            self.wfile.write(bytes(json.dumps(new_player), "utf-8"))
        elif (self.path[:10] == '/findgame?'):  # if a player ask for finding a game
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            name = self.path[10:]  # getting the player name
            gameID = ""
            player_index = getIndexPlayerByName(name)
            if player_index != -1:
                waitingForGame.append(players[player_index])  # a new player wan to join a game
                if len(waitingForGame) == 1:  # if only one player waits than there is not enough players for a game
                    players[player_index].status = "Waiting"
                elif len(waitingForGame) == 2:  # if two players, than a game will be created
                    players[player_index].status = "Playing"  # the two playres status should be now "Playing"
                    waitingForGame[0].status = "Playing"
                    games.append(Game(waitingForGame[0], waitingForGame[1]))  # creating the game with those two playres
                    waitingForGame = []  # clearing the waiting for game list
                    game_index = getIndexGameByName(name)
                    gameID = games[game_index].id  # getting the game id
                    games[game_index].generate_random_player_types()  # generate random types and turns

                new_player = {"Name": players[player_index].name, "Type": players[player_index].type,
                              "Status": players[player_index].status,
                              "gameID": gameID}  # setting the player new data in a json format

                self.wfile.write(bytes(json.dumps(new_player), "utf-8"))  # send the data as response to the client
            else:
                self.wfile.write(bytes("Eror", "utf-8"))
        elif (self.path[:8] == '/isTurn?'):  # if a player ask for if it's his turn
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            data = self.path[8:]  # the data send is a json object
            data = parse.unquote(data)
            data = json.loads(data)  # loads the data
            type_of_player = data["player"]
            gameID = data["id"]
            gameIndex = getIndexGameByID(gameID)
            is_turn = False
            player_board = None  # updated board if needed
            if type_of_player == "PLAYER1":  # if client is player1 in the game
                player_num = 1
                if games[gameIndex].is_turn(str(player_num)):  # check if it's his turn
                    is_turn = True
            elif type_of_player == "PLAYER2":  # if client is player2 in the game
                player_num = 2
                if games[gameIndex].is_turn(str(player_num)):  # check if it's his turn
                    is_turn = True
            if is_turn:  # if it's his turn - set the current board
                player_board = games[gameIndex].board.cells
            player_won = games[gameIndex].won  # need to send if there's a winner
            game_status = {"is_turn": is_turn,
                           "board": player_board, "won": player_won}  # setting game status as json object
            self.wfile.write(bytes(json.dumps(game_status), "utf-8"))
        elif self.path[:13] == '/buttonClick?':  # if a button was clicked
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            data = self.path[13:]
            data = parse.unquote(data)
            data = json.loads(data)
            buttonNumber = data["buttonNumber"]
            gameID = data["id"]
            gameIndex = getIndexGameByID(gameID)
            games[gameIndex].insert_button_click(int(buttonNumber) - 1)  # insetting the button click into the game
            if games[gameIndex].is_win():  # checks if there's a winner
                won = games[gameIndex].get_current_player().type
            else:
                if games[gameIndex].is_tie():
                    won = "Tie"
            games[gameIndex].change_turn()  # change the game turn

            gameStatus = {}  # setting all of the data
            gameStatus.update({"board": games[gameIndex].board.cells})
            gameStatus.update({"buttonClick": buttonNumber})
            gameStatus.update({"won": games[gameIndex].won})
            asa = json.dumps(gameStatus)
            self.wfile.write(bytes(asa, "utf-8"))
        elif (self.path[:9] == '/endGame?'):  # if client want to leave the game
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            data = parse.unquote(self.path[9:])
            data = json.loads(data)
            gameID = data["id"]
            player = data["player"]
            name = data["name"]
            if player == "PLAYER1":
                player = "player1"
            elif player == "PLAYER2":
                player = "player2"
            gameIndex = getIndexGameByID(gameID)
            if gameIndex != -1:
                games[gameIndex].player_leave(player)  # throw the player from the game
                playerIndex = getIndexPlayerByName(name)
                players[playerIndex].status = "In Lobby"  # change player's status
                if games[gameIndex].on_game["player1"] == False and games[gameIndex].on_game["player2"] == False:  # if both players left
                    del games[gameIndex]  # remove the game
        elif self.path[:13] == "/playerOnApp?":  # if client ask this path, it means that he send signals that he is online
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            data = parse.unquote(self.path[13:])
            data = json.loads(data)
            name = data["name"]
            playerIndex = getIndexPlayerByName(name)
            players[playerIndex].disconnect_period = datetime.now()  # updating the time he sent the signal
            check_need_to_remove_players()  # check if it needed to remove someone
        elif self.path[:17] == "/refreshGameData?":  # uf user want to refresh the game
            data = parse.unquote(self.path[17:])
            data = json.loads(data)  # loading the json format data into python one
            player_name = data["name"]
            gameID = data["ID"]
            game_index = getIndexGameByID(gameID)
            if game_index != -1:
                game_data_to_send = {}
                turn = games[game_index].turn  # getting whose turn
                type = games[game_index].get_player_by_name(player_name).type  # getting player type
                board = games[game_index].board.cells  # getting updated boardd
                opponent_name = None
                type_of_player = None
                if games[game_index].player1.name == player_name:  # getting more game data for the client
                    type_of_player = "PLAYER1"
                    opponent_name = games[game_index].player2.name
                    if turn == 1:
                        turn = True
                    else:
                        turn = False
                else:
                    type_of_player = "PLAYER2"
                    opponent_name = games[game_index].player1.name
                    if turn == 2:
                        turn = True
                    else:
                        turn = False
                game_data_to_send.update({"typeOfPlayer": type_of_player})
                game_data_to_send.update({"turn": turn})
                game_data_to_send.update({"type": type})
                game_data_to_send.update({"board": board})
                game_data_to_send.update({"opponentName": opponent_name})
                game_data_to_send.update({"won": games[game_index].won})  # converting all data to json
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(game_data_to_send), "utf-8"))  # send the response
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)


httpd = socketserver.TCPServer(('', 8000), Handler)

httpd.serve_forever()

# python3 server.py
# 127.0.0.1 - - [11/Apr/2017 11:36:49] "GET / HTTP/1.1" 200 -
# http :8000
'''
HTTP/1.0 200 OK
Date: Tue, 11 Apr 2017 15:36:49 GMT
Server: SimpleHTTP/0.6 Python/3.5.2
Hello world
7'''
