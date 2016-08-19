import itertools

from enum import Enum
from game.framework.board import Board
from game.framework.environment import Environment
from game.framework.match import simple_match
from game.framework.state import State
from game.console import choose_agent


class Disc(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = 1

    def __str__(self):
        return self.name


class Reversi(Environment):
    def __init__(self, black, white):
        self._black = black
        self._white = white
        self._valid_actions = {}  # { action: flips } where flips = [cell1, cell2, ..]

    def valid_actions(self, state):
        if state not in self._valid_actions:
            self._valid_actions[state] = self._calc_valid_actions(state)
        return self._valid_actions[state].keys()

    def apply(self, state, action):
        board, agent = state.board, state.agent
        if action in self.valid_actions(state):
            flips = self._valid_actions[state][action]
            disc_color = self._disc_color(state.agent)
            board = board.apply([(disc_color, flip) for flip in [action] + flips])
            return state.turn(board, len(flips)+1, -len(flips))
        return state.opposite()

    def print_summary(self, state):
        black_score = state.score(self._black)
        white_score = state.score(self._white)
        print('{}: {} ({})'.format(Disc.BLACK, black_score, self._black))
        print('{}: {} ({})'.format(Disc.WHITE, white_score, self._white))

    def _disc_color(self, agent):
        return Disc.BLACK if agent == self._black else Disc.WHITE

    def _calc_valid_actions(self, state):
        board, agent = state.board, state.agent
        disc_color = self._disc_color(agent)
        valid_actions = {}
        for cell in itertools.product(range(board.height), range(board.width)):
            if not board.is_empty(cell):
                continue
            flips = self._calc_flips(disc_color, board, cell)
            if len(flips) > 0:
                valid_actions[cell] = flips
        return valid_actions

    def _calc_flips(self, disc_color, board, cell):
        flips = []
        for dr, dc in itertools.product(range(-1, 2), range(-1, 2)):
            if (dr, dc) == (0, 0):
                continue
            flips.extend(self._find_flips(disc_color, board, cell, dr, dc, []))
        return flips

    def _find_flips(self, disc_color, board, prev_cell, dr, dc, flippable):
        cell = prev_cell[0] + dr, prev_cell[1] + dc
        if not board.in_bounds(cell) or board.is_empty(cell):
            return []
        if board[cell] == disc_color:
            return flippable
        flippable.append(cell)  # not empty and not player's kind ==> opponent kind
        return self._find_flips(disc_color, board, cell, dr, dc, flippable)


def create_board(board_size=8):
    row, col = board_size/2-1, board_size/2-1
    grid = [[Disc.EMPTY for _ in range(board_size)] for _ in range(board_size)]
    grid[row][col] = Disc.WHITE
    grid[row][col+1] = Disc.BLACK
    grid[row+1][col] = Disc.BLACK
    grid[row+1][col+1] = Disc.WHITE
    return Board(grid, Disc.EMPTY, {Disc.EMPTY: ' ', Disc.BLACK: '@', Disc.WHITE: 'O'})


def main():
    black = choose_agent('Choose a black agent type')
    white = choose_agent('Choose a white agent type')
    simple_match(Reversi(black, white), State(create_board(), black, white, 2, 2))


if __name__ == "__main__":
    main()
