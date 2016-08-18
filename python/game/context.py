class GameContext(object):
    """ This is an interface expected to be implemented in a board game class
    """
    @property
    def is_active(self):
        """ True if at least one of the players can continue playing
        """
        return False

    @property
    def valid_actions(self):
        """ Returns a list of valid actions for  current player
        """
        return []

    @property
    def agent(self):
        """ Returns the current player
        """
        return None

    @property
    def score(self):
        """ Returns the current score of the player
        """
        return -1

    @property
    def winner(self):
        """ Return the winner of the game
        """
        return None

    def apply(self, action):
        """ Returns a new game context (the current context copy + action applied)
        """
        return None

    @property
    def state(self):
        """ Returns the current game state
        """
        return None

    def print_summary(self):
        """ Prints the current board state
        """
        pass
