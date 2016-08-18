from game.board import Board
from game.environment import Environment
from game.player import Player
from game.state import State
from game.console import choose_agent
from game.match import simple_match
from enum import Enum
import itertools


class Disc(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = 1

    def __str__(self):
        return self.name


class Reversi(Environment):
    def __init__(self, board, player, opponent):
        self._board = board
        self._player = player
        self._opponent = opponent
        self._state = State(self, board, opponent.agent)
        self._player_valid_actions = self._calc_valid_actions(player)

    @staticmethod
    def create(black_player, white_player, board_size=8):
        row, col = board_size/2-1, board_size/2-1
        grid = [[Disc.EMPTY for _ in range(board_size)] for _ in range(board_size)]
        grid[row][col] = Disc.WHITE
        grid[row][col+1] = Disc.BLACK
        grid[row+1][col] = Disc.BLACK
        grid[row+1][col+1] = Disc.WHITE
        return Reversi(Board(grid, Disc.EMPTY,
                             {Disc.EMPTY: ' ', Disc.BLACK: '@', Disc.WHITE: 'O'}),
                       Player(black_player, Disc.BLACK, 2),
                       Player(white_player, Disc.WHITE, 2))

    @property
    def is_active(self):
        return len(self._player_valid_actions) > 0 or \
               len(self._calc_valid_actions(self._opponent)) > 0  # check if opponent still has any move

    @property
    def valid_actions(self):
        return self._player_valid_actions.keys()

    def _is_valid_action(self, action):
        return action in self._player_valid_actions

    @property
    def agent(self):
        return self._player.agent

    @property
    def score(self):
        return self._player.score

    @property
    def winner(self):
        if self.is_active:
            return None
        if self._player.score > self._opponent.score:
            return self._player.agent
        return self._opponent.agent

    def apply(self, action):
        if action in self._player_valid_actions:
            flips = self._player_valid_actions[action]
            board = self._board.apply([(self._player.kind, flip) for flip in [action] + flips])
        else:
            flips = []
            board = self._board
        return Reversi(
            board,
            self._opponent.apply(-len(flips)),
            self._player.apply(len(flips) + 1)  # including the given action itself
        )

    @property
    def state(self):
        return self._state

    def print_summary(self):
        player_kind = self._player.kind
        black = self._player if player_kind == Disc.BLACK else self._opponent
        white = self._player if player_kind == Disc.WHITE else self._opponent
        print(self._board)
        print('{}'.format(black))
        print('{}'.format(white))

    def _calc_valid_actions(self, player):
        player_kind = player.kind
        valid_actions = {}
        for cell in itertools.product(range(self._board.height),
                                      range(self._board.width)):
            if not self._board.is_empty(cell):
                continue
            flips = self._calc_flips(player_kind, cell)
            if len(flips) > 0:
                valid_actions[cell] = flips
        return valid_actions

    def _calc_flips(self, player_kind, cell):
        flips = []
        for dr, dc in itertools.product(range(-1, 2), range(-1, 2)):
            if (dr, dc) == (0, 0):
                continue
            flips.extend(self._find_flips(player_kind, cell, dr, dc, []))
        return flips

    def _find_flips(self, player_kind, prev_cell, dr, dc, flippable):
        cell = prev_cell[0] + dr, prev_cell[1] + dc
        if not self._board.in_bounds(cell) or self._board.is_empty(cell):
            return []
        if self._board[cell] == player_kind:
            return flippable
        flippable.append(cell)  # not empty and not player's kind ==> opponent kind
        return self._find_flips(player_kind, cell, dr, dc, flippable)


if __name__ == "__main__":
    simple_match(Reversi.create(
        choose_agent('Choose a black agent type'),
        choose_agent('Choose a white agent type')))
