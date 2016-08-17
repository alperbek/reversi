from game.board import GameBoard
from game.context import GameContext
from game.console import choose_player
from game.match import simple_match
import itertools

# constants
EMPTY = -1
BLACK = 0
WHITE = 1
BOARD_SIZE = 8


class ReversiBoard(GameBoard):
    def __init__(self):
        row, col = BOARD_SIZE/2-1, BOARD_SIZE/2-1
        grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        grid[row][col] = WHITE
        grid[row][col+1] = BLACK
        grid[row+1][col] = BLACK
        grid[row+1][col+1] = WHITE
        GameBoard.__init__(self, grid, {BLACK: '@', WHITE: 'O', EMPTY: ' '})


class ReversiPlayer(object):
    def __init__(self, player, color, score):
        self._player = player
        self._color = color
        self._score = score

    def get_player(self):
        return self._player

    def get_color(self):
        return self._color

    def is_black(self):
        return self._color == BLACK

    def is_white(self):
        return self._color == WHITE

    def get_score(self):
        return self._score

    def apply(self, score_change):
        return ReversiPlayer(self._player, self._color, self._score + score_change)

    def __eq__(self, other):
        return self.get_player() == other.get_player()


class Reversi(GameContext):
    def __init__(self, board, player, opponent):
        self._board = board
        self._player = player
        self._opponent = opponent
        self._player_valid_actions = self._calc_valid_actions(player.get_color())

    @staticmethod
    def create(black_player, white_player):
        return Reversi(ReversiBoard(),
                       ReversiPlayer(black_player, BLACK, 2),
                       ReversiPlayer(white_player, WHITE, 2))

    def is_active(self):
        return len(self._player_valid_actions) > 0 or \
               len(self._calc_valid_actions(self._opponent.get_color())) > 0  # check if opponent still has any move

    def get_valid_actions(self):
        return self._player_valid_actions.keys()

    def _is_valid_action(self, action):
        return action in self._player_valid_actions

    def get_player(self):
        return self._player.get_player()

    def get_score(self):
        return self._player.get_score()

    def apply(self, action):
        if action in self._player_valid_actions:
            flips = self._player_valid_actions[action]
            board = self._board.apply([(self._player.get_color(), flip) for flip in [action] + flips])
        else:
            flips = []
            board = self._board
        return Reversi(
            board,
            self._opponent.apply(-len(flips)),
            self._player.apply(len(flips) + 1)  # including the given action itself
        )

    def _calc_valid_actions(self, player_color):
        valid_actions = {}
        for cell in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if not self._board.is_empty(cell):
                continue
            flips = self._calc_flips(player_color, cell)
            if len(flips) > 0:
                valid_actions[cell] = flips
        return valid_actions

    def _calc_flips(self, player_color, cell):
        flips = []
        for dr, dc in itertools.product(range(-1, 2), range(-1, 2)):
            if (dr, dc) == (0, 0):
                continue
            flips.extend(self._find_flips(player_color, cell, dr, dc, []))
        return flips

    def _find_flips(self, player_color, prev_cell, dr, dc, flippable):
        cell = prev_cell[0] + dr, prev_cell[1] + dc
        if not self._board.in_bounds(cell) or self._board.is_empty(cell):
            return []
        if self._board.get_value(cell) == player_color:
            return flippable
        flippable.append(cell)  # not empty and not player's color ==> opponent color
        return self._find_flips(player_color, cell, dr, dc, flippable)

    def print_summary(self):
        if self._player.is_black():
            black_score = self._player.get_score()
            white_score = self._opponent.get_score()
        else:
            black_score = self._opponent.get_score()
            white_score = self._player.get_score()
        print(self._board)
        print('Black: {} White: {}'.format(black_score, white_score))


if __name__ == "__main__":
    simple_match(Reversi.create(
        choose_player('Choose a black player type'),
        choose_player('Choose a white player type')))
