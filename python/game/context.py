class GameContext(object):
    """ This is an interface expected to be implemented in a board game class
    """
    def is_active(self):
        """ True if at least one of the players can continue playing
        """
        return False

    def get_valid_actions(self):
        """ Returns a list of valid actions for  current player
        """
        return []

    def get_state(self):
        """ Returns the current state of this game context
        """
        return None

    def get_score(self, player):
        """ Returns the current score of the player
        """
        return -1

    def get_plaery(self):
        """ Returns the current player
        """
        return None

    def apply(self, action):
        """ Returns a new game context (the current context copy + action applied)
        """
        return None

    def summary(self):
        """ Returns a string of the current board state
        """
        return ""
