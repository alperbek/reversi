class State(object):
    def __init__(self, env, board, agent):
        self._env = env
        self._board = board
        self._agent = agent

    @property
    def env(self):
        """ Related env
        """
        return self._env

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
