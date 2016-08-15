from game.board import GameBoard
from game.context import GameContext
from game.player import choose_player
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


class Reversi(GameContext):
    def __init__(self, board, player, player_color, player_score, opponent, opponent_color, opponent_score):
        self._board = board
        self._player = player
        self._player_color = player_color
        self._player_score = player_score
        self._opponent = opponent
        self._opponent_color = opponent_color
        self._opponent_score = opponent_score
        self._player_valid_actions = self._calc_valid_actions(player)
        self._opponent_valid_actions = self._calc_valid_actions(opponent)

    @staticmethod
    def create(black_player, white_player):
        return Reversi(ReversiBoard(), black_player, BLACK, 2, white_player, WHITE, 2)

    def is_active(self):
        return len(self._player_valid_actions) > 0 or len(self._opponent_valid_actions) > 0

    def get_valid_actions(self):
        return self._player_valid_actions.keys()

    def _is_valid_action(self, action):
        return action in self._player_valid_actions

    def get_score(self):
        return self._player_score

    def get_player(self):
        return self._player

    def apply(self, action):
        if action in self._player_valid_actions:
            flips = self._player_valid_actions[action]
            board = self._board.apply([(self._player_color, flip) for flip in [action] + flips])
        else:
            flips = []
            board = self._board
        return Reversi(
            board,
            self._opponent,
            self._opponent_color,
            self._opponent_score - len(flips),
            self._player,
            self._player_color,
            self._player_score + len(flips) + 1  # including the given action itself
        )

    def _calc_valid_actions(self, player):
        action_flips = {cell: self._calc_flips(player, cell)
                        for cell in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE))
                        if self._board.is_empty(cell)}
        return {action: flips for action, flips in action_flips.items() if len(flips) > 0}

    def _calc_flips(self, player, (row, col)):
        player_color = self._player_color if player == self._player else self._opponent_color
        opponent_color = self._opponent_color if player == self._player else self._player_color
        flips = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if (dr, dc) == (0, 0):
                    continue
                flippable = []
                cell = (row + dr, col + dc)
                while self._board.in_bounds(cell):
                    cell_color = self._board.get_value(cell)
                    if cell_color == opponent_color:
                        flippable.append(cell)
                        cell = (cell[0]+dr, cell[1]+dc)
                    else:
                        if cell_color == player_color:
                            flips.extend(flippable)
                        break
        return flips

    def summary(self):
        black_score = self._player_score if self._player_color == BLACK else self._opponent_score
        white_score = self._player_score if self._player_color == WHITE else self._opponent_score
        print(self._board)
        print('Black: {} White: {}'.format(black_score, white_score))


if __name__ == "__main__":
    simple_match(Reversi.create(
        choose_player('Choose a black player type'),
        choose_player('Choose a white player type')))
