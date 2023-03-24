from datetime import datetime
# A file whose purpose is to represent the player class


class Player:
    """
    The player class
    """
    id = 1  # each player has significant id but it's currently not used(for future purposes)

    def __init__(self, type=None, name="user"):
        """
        A method that creates the player object
        ------
        :param type: the type of the player at tic tac toe( 'X' or 'O'); default - None
        :param name: the name of player; default - "user" + player id
        """
        self.id = Player.id
        Player.id += 1
        self.type = type  # an variable that identify the player type (X or O)
        self.name = name  # identify the name
        if self.name == "user":
            # if the name wasn't chosed, create a significant one
            self.name = self.name + str(Player.id)
        # the status of the player( "In Lobby" - player is on the lobby,
        self.status = "In Lobby"
        #  "Waiting" - waiting for an opponent to connected, "Playing" - currently playing in a game
        self.on_app = True
        #  when a player client is active, he sends signals that he is online(if a signal don't come for 60 sec) the server disconnect him
        # the time when the player send a single that he is on the app
        self.disconnect_period = datetime.now()

    def insertType(self, type):
        """
        A method to insert a type for the player
        :param type: the type of the tic tac toe( 'X' or 'O')
        """
        self.type = type
