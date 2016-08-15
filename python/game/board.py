import copy
import os


class GameBoard(object):
    def __init__(self, grid, mapping):
        self._grid = grid
        self._width = len(grid[0])
        self._height = len(grid)
        self._mapping = mapping

    def in_bounds(self, (row, col)):
        return 0 <= row < self._height and 0 <= col < self._width

    def set_value(self, (row, col), val):
        self._grid[row][col] = val

    def get_value(self, (row, col)):
        return self._grid[row][col]

    def is_empty(self, (row, col)):
        return self.get_value((row, col)) == -1

    def apply(self, actions):
        grid = copy.deepcopy(self._grid)
        for action in actions:
            row, col = action[1]
            grid[row][col] = action[0]
        return GameBoard(grid, self._mapping)

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

