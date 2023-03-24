from classes.Player import Player
from classes.Board import Board
import random


# A file whose purpose is to represent the game class


class Game:
    """
    The game class
    """
    id = 0  # game id that increases each time

    def __init__(self, player1: Player = None, player2: Player = None):
        """
        A method that creates the game object
        :param player1: the first player; default - None
        :param player2: the second player; default - None
        """
        self.won = None  # which player won can be: 'None'/ 'X'/ 'O'/ 'Tie'
        self.winner = None
        self.player1 = player1
        self.player2 = player2
        # represent that each player is on the game or left it
        self.on_game = {"player1": True, "player2": True}
        # is the game live( if there are two players on the game)
        self.game_live = True
        self.board = Board()  # creating board
        self.turn = None  # whose turn; if equal 1 it's player1 turn, if 2 it's player2 turn
        self.id = Game.id  # represent the id of the game, that way the server can find the game
        Game.id += 1
        if player1 is not None and player2 is not None:
            self.turn = 1

    def insert_button_click(self, button_num):
        """
        A method that insert a button click('X' or 'O') to the game board
        :param button_num: the button number
        """
        loc = self.board.caculate_location(
            button_num)  # getting the two dimension index from the button click
        self.board.insert(loc, self.get_current_player().type)

    def is_win(self):
        """
        A method that checks if there is a winner, if there is, it values the self.won variable by the winner's type
        :return: True if there is a winner
        """
        if self.board.check_win(self.get_current_player().type):
            self.winner = "player" + str(self.turn)
            # setting the won onto the winner's type
            self.won = self.get_current_player().type
            return True
        else:
            return False

    def is_tie(self):
        """
        checks if there is a Tie
        :return: True if there has been a tie
        """
        if self.board.check_board_full():
            self.won = "Tie"
            return True

    def insert_player1(self, player1):
        """
        A method that defines the player1 object
        :param player1: a player object
        """
        self.player1 = player1

    def insert_player2(self, player2, turn=None):
        """
        A method that defines the player2 object
        :param player2: a player object
        :param turn: the new turn; default - None
        """
        self.player2 = player2
        if turn is not None:
            self.turn = turn
        else:
            self.turn = 1

    def is_turn(self, player_num):
        """
        A method that checks if it's the player turn
        :param player_num: if needs to check player1, the variable equal to 1, if player2 it's 2
        :return: True if that's the player turn
        """
        if player_num == str(self.turn):
            return True
        return False

    def change_turn(self):
        """
        A method that changes the current game's turn
        """
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def generate_random_player_types(self):
        """
        A method that defines the players types with a random way, and determines the game's turn;
        the player with the 'X' type is always starting
        """
        types = ["X", "O"]
        random.shuffle(types)
        self.player1.type = types[0]
        self.player2.type = types[1]
        if self.player1.type == 'X':
            self.turn = 1
        else:
            self.turn = 2

    def player_leave(self, player):
        """
        A method that throws a player from the game
        :param player: which player needs to be thrown; equal to "player1" or to "player2"
        """
        if player == "player1":
            self.on_game["player1"] = False
        elif player == "player2":
            self.on_game["player2"] = False
        self.game_live = False  # a player left so the game is not live

    def player_leave_by_name(self, name):
        """
        A method that throws a player from the game
        :param name: which player needs to be thrown; equal to player1 name or to the players2 name
        """
        if name == self.player1.name:
            self.on_game["player1"] = False
        elif name == self.player2.name:
            self.on_game["player2"] = False
        self.game_live = False

    def get_current_player(self):
        """
        A function that return the current player that has it's turn now
        :return: the player object whose currently has the turn
        """
        if self.turn == 1:
            return self.player1
        else:
            return self.player2

    def get_player_by_name(self, name):
        """
        A function that return the player by name
        :param name: the name of player1 or player2
        :return: a player object that his name is the name given
        """
        if name == self.player1.name:
            return self.player1
        elif name == self.player2.name:
            return self.player2
