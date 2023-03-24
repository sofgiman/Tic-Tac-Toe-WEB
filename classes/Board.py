
# A file whose purpose is to represent the board class

class Board:
    """
    The class board - the board of the tic tac toe game
    """
    def __init__(self):
        """
        A method that create the board object
        """
        self.cells = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]]  # the cells are a two dimensions list of 3 by 3

    def insert(self, loc, typeXO):
        """
        A method that insert in the cells' location a type
        :param loc: the location of the list; [[int][int]]
        :param typeXO: 'X' or 'O'
        """
        self.cells[loc[0]][loc[1]] = str(typeXO)

    def check_board_full(self):
        """
        A method that checks if the board is full(each cell is 'X' or 'O')
        :return: True if board is full, else return false
        """
        for i in range(9):
            loc = self.caculate_location(i)
            if self.cells[loc[0]][loc[1]] != 'X' and self.cells[loc[0]][loc[1]] != 'O':
                return False
        return True

    def caculate_location(self, loc):
        """
        A method that convert one dimension location to and two dimensions location and return it
        :param loc: a one dimension location: int(0-8)
        :return: the converted location: a list - [[int(0-2)][int(0-2)]]
        """
        loc_cells = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]  # the two dimension indexes
        return loc_cells[loc]

    def check_diagonal(self, player_type):
        """
        A method who checks if the player type won the game in a diagonal way
        :param player_type: 'X' or 'O'
        :return: True if that player won
        """
        if self.cells[0][0] == self.cells[1][1] == self.cells[2][2] == player_type:  # if player won by the left diagonal line
            return True
        elif self.cells[0][2] == self.cells[1][1] == self.cells[2][0] == player_type:  # if player won by the right diagonal line
            return True
        else:
            return False

    def check_horizontal(self, player_type):
        """
        A method who checks if the player type won the game in a horizontal way(row)
        :param player_type: 'X' or 'O'
        :return: True if that player won
        """
        # if player won by the first row:
        if self.cells[0][0] == self.cells[0][1] == self.cells[0][2] == player_type:
            return True
        # if player won by the second row:
        elif self.cells[1][0] == self.cells[1][1] == self.cells[1][2] == player_type:
            return True
        # if player won by the third row:
        elif self.cells[2][0] == self.cells[2][1] == self.cells[2][2] == player_type:
            return True
        else:
            return False

    def check_verticals(self, player_type):
        """
        A method who checks if the player type won the game in a vertical way(column)
        :param player_type: 'X' or 'O'
        :return: True if that player won
        """
        # if player won by the first column:
        if self.cells[0][0] == self.cells[1][0] == self.cells[2][0] == player_type:
            return True
        # if player won by the second column:
        elif self.cells[0][1] == self.cells[1][1] == self.cells[2][1] == player_type:
            return True
        # if player won by the third column:
        elif self.cells[0][2] == self.cells[1][2] == self.cells[2][2] == player_type:
            return True
        else:
            return False

    #  A function that checks if some player won;
    #  Return: 0 if no one won, 1 if player 1 won or 2 if player 2 won
    def check_win(self, player_type):
        """
        A method who checks if the player type won the game
        :param player_type: 'X' or 'O'
        :return: True if that player won
        """
        verticals = self.check_verticals(player_type)  # check vertical lines
        if verticals:
            return True
        else:
            horizontal = self.check_horizontal(player_type)  # check horizontal lines
            if horizontal:
                return True
            else:
                diagonal = self.check_diagonal(player_type)  # check diagonals
                return diagonal

    def check_place_taken(self, loc):
        """
        A method that checks if a place is taken on the cells
        :param loc: two dimension index
        :return: True if place is taken
        """
        if self.cells[loc[0]][loc[1]] == "O" or self.cells[loc[0]][loc[1]] == "X":
            return True
        return False
