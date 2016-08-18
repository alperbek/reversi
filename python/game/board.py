import copy
import os


class GameBoard(object):
    def __init__(self, grid, empty, mapping):
        self._grid = grid
        self._width = len(grid[0])
        self._height = len(grid)
        self._empty = empty
        self._mapping = mapping

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def in_bounds(self, cell):
        row, col = cell
        return 0 <= row < self._height and 0 <= col < self._width

    def __getitem__(self, cell):
        row, col = cell
        return self._grid[row][col]

    def is_empty(self, cell):
        return self[cell] == self._empty

    def apply(self, actions):
        grid = copy.deepcopy(self._grid)
        for action in actions:
            row, col = action[1]
            grid[row][col] = action[0]
        return GameBoard(grid, self._empty, self._mapping)

    def __str__(self):
        s = ' | '
        for col in range(self._width):
            s += str(col) + ' | '
        s += os.linesep + '-' * (self._width * 4 + 2)
        for row in range(self._height):
            s += os.linesep + str(row) + '| '
            for col in range(self._width):
                s += self._mapping[self._grid[row][col]] + ' | '
            s += os.linesep
            s += '-' * (self._width * 4 + 2)
        return s

    def __eq__(self, other):
        return self._grid == other._grid

    def __hash__(self):
        return hash(str(self._grid))

