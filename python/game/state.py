class GameState(object):
    def __init__(self, context, board, player):
        self._context = context
        self._board = board
        self._player = player

    def get_context(self):
        """ Related context
        """
        return self._context

    def get_board(self):
        """ The current board
        """
        return self._board

    def get_player(self):
        """ This player caused this state
        """
        return self._player

    def __eq__(self, other):
        return self._board == other.get_board() and self._player == other.get_player()

    def __hash__(self):
        return hash(self._board)
