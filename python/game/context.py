class GameContext(object):
    """ This is an interface expected to be implemented in a board game class
    """
    def is_active(self):
        """ True if at least one of the players can continue playing
        """
        return False

    def get_valid_actions(self, player):
        """ Returns a list of valid actions for the give player

        :param player: a player instance
        :return: a list of valid actions
        """
        return []

    def get_state(self):
        """ Returns the current state of this game context

        :return: the current state of this game context
        """
        return None

    def get_score(self, player):
        """ Returns the current score of the player

        :param player: a player instance
        :return: the current score of the given player
        """
        return -1

    def get_opponent(self, player):
        """ Returns the opponent player

        :param player: a player instance
        :return: the opponent player
        """
        return None

    def apply(self, player, action):
        """ Returns a new game context (the current context copy + action applied)

        :param player: a player instance who is applying the action
        :param action: an action to be applied
        :return:
        """
        return None

    def summary(self):
        """ Returns a string of the current board state

        :return: a string of the current board state
        """
        return ""
