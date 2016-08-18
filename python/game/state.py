class GameState(object):
    def __init__(self, context, board, agent):
        self._context = context
        self._board = board
        self._agent = agent

    def get_context(self):
        """ Related context
        """
        return self._context

    def get_board(self):
        """ The current board
        """
        return self._board

    def get_agent(self):
        """ This player caused this state
        """
        return self._agent

    def __eq__(self, other):
        return self._board == other.get_board() and self._agent == other.get_agent()

    def __hash__(self):
        return hash(self._board)
