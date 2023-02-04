import numpy as np
from numpy.lib.stride_tricks import as_strided


# create sudoku board, if m not none, it is copied
class Sudoku_Board:

    def __init__(self, m=None):

        # m is a n_d_array or a list of lists
        if m is not None:
            self._board = np.array(m, dtype=np.uint8)
        else:
            self._board = np.zeros((9, 9), dtype=np.uint8)
        self.squares = as_strided(self._board,
                                  shape=(3, 3, 3, 3),
                                  strides=(27, 3, 9, 1))

    # return true if all cells are filled
    def all_filled(self):

        return np.count_nonzero(self._board) == 81

    # return the board object
    def board(self):
        return self._board

    # retun item at position key
    # key is a tuple of 0-based index
    # return a int from 0 to 9, 0 if the cell is empty
    def __getitem__(self, key):
        if self._valid_position(key):
            return self._board[key]

        # if invalid position
        else:
            raise ValueError("Invalid position")

    # sets the item at position key
    # key is a tuple of 0-based index
    # value is an int between 0 and 9, or 0 if the cell has to be emptied.
    def __setitem__(self, key, value):
        if self._valid_position(key) and 0 <= value <= 9:
            self._board[key] = value

        # if invalid position
        else:
            raise ValueError("Invalid position")

    def _valid_position(self, pos):
        return all(0 <= i <= 8 for i in pos)

    # return true if the board is a valid sudoku puzzle
    def valid(self):
        for m in range(9):
            ui = np.unique(self._board[m, :])
            if ui.shape[0] < 9 or np.count_nonzero(ui) < 9:
                return False
            ui = np.unique(self._board[:, m])
            if ui.shape[0] < 9 or np.count_nonzero(ui) < 9:
                return False
            ui = np.unique(self.squares[divmod(m, 3)])
            if ui.shape[0] < 9 or np.count_nonzero(ui) < 9:
                return False
        return True

    # board format
    def __str__(self):
        rows = []
        for m in range(9):
            row = []
            for n in range(9):
                el = self._board[m, n]
                if el:
                    row.append(str(el))
                else:
                    row.append(" ")
            rows.append(" | ".join(row))
        return "\n".join(rows)
