from game.board import GameBoard
from game.context import GameContext
from game.match import simple_match
from game.player import RandomPlayer, MiniMaxPlayer
import itertools

# constants
EMPTY = -1
BLACK = 0
WHITE = 1
BOARD_SIZE = 8


class Reversi(GameContext):
    def __init__(self, black_player, white_player, black_score, white_score, board, actionable_cells):
        self._black_player = black_player
        self._white_player = white_player
        self._black_score = black_score
        self._white_score = white_score
        self._board = board
        self._actionable_cells = actionable_cells

    @staticmethod
    def create(black_player, white_player):
        row, col = BOARD_SIZE/2-1, BOARD_SIZE/2-1
        grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        grid[row][col] = WHITE
        grid[row][col+1] = BLACK
        grid[row+1][col] = BLACK
        grid[row+1][col+1] = WHITE
        board = GameBoard(grid, {BLACK: '@', WHITE: 'O', EMPTY: ' '})
        actionable_cells = {cell for cell in itertools.product(range(row-1, row+3), range(col-1, col+3))
                            if board.is_empty(cell)}
        return Reversi(black_player, white_player, 2, 2, board, actionable_cells)

    def is_active(self):
        for cell in self._actionable_cells:
            if self._is_valid_action(self._black_player, cell) or \
               self._is_valid_action(self._white_player, cell):
                return True
        return False

    def get_valid_actions(self, player):
        return [cell for cell in self._actionable_cells if self._is_valid_action(player, cell)]

    def _is_valid_action(self, player, action):
        return self._board.in_bounds(action) \
               and self._board.is_empty(action) \
               and len(self._calc_flips(player, action)) > 0

    def get_state(self):
        return self._board

    def get_score(self, player):
        return self.__if_black_else(player, self._black_score, self._white_score)

    def get_opponent(self, player):
        return self.__if_black_else(player, self._white_player, self._black_player)

    def __if_black_else(self, player, a, b):
        return a if player == self._black_player else b

    def apply(self, player, action):
        player_color = self.__if_black_else(player, BLACK, WHITE)
        flips = self._calc_flips(player, action)
        if len(flips) == 0:
            return self  # invalid move - no change
        score = len(flips)
        flips.append(action)
        board = self._board.apply([(player_color, action) for action in flips])
        # update actionable cells
        row, col = action
        actionable_cells = {cell for cell in self._actionable_cells if cell != action}
        actionable_cells.update(
            [cell for cell in itertools.product(range(row-1, row+2), range(col-1, col+2))
             if self._board.in_bounds(cell) and self._board.is_empty(cell)])
        return Reversi(
            self._black_player,
            self._white_player,
            self._black_score + self.__if_black_else(player, score+1, -score),
            self._white_score + self.__if_black_else(player, -score, score+1),
            board,
            actionable_cells
        )

    def _calc_flips(self, player, (row, col)):
        player_color, opponent_color = self.__if_black_else(player, (BLACK, WHITE), (WHITE, BLACK))
        flips = []
        for dr, dc in [delta for delta in itertools.product(range(-1, 2), range(-1, 2)) if delta != (0, 0)]:
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
        return 'Black: {} White: {}'.format(self._black_score, self._white_score)


def main():
    print("Game start")
    black_player = RandomPlayer()
    white_player = MiniMaxPlayer(3)
    context = Reversi.create(black_player, white_player)
    simple_match(context)
    print("Game end")

if __name__ == "__main__":
    main()
