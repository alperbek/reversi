class GameState(object):
    def __init__(self, context, board, agent):
        self._context = context
        self._board = board
        self._agent = agent

    @property
    def context(self):
        """ Related context
        """
        return self._context

    @property
    def board(self):
        """ The current board
        """
        return self._board

    @property
    def agent(self):
        """ This player caused this state
        """
        return self._agent

    def __eq__(self, other):
        return self.board == other.board and self.agent == other.agent

    def __hash__(self):
        return hash(self.board)
