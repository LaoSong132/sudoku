import random
import numpy as np


# if the dancing links matrix is empty
class EmptyDLMatrix(Exception):
    pass


# if can not add rows to matrix
class CannotAddRows(Exception):
    pass


# 4 pointers to neighbors (up, down, left, right)
# 1 pointer to column header, and associated indexse
class Cell:
    __slots__ = list("UDLRC") + ["indexes"]

    def __init__(self):
        self.U = self.D = self.L = self.R = self
        self.C = None
        self.indexes = None

    def __str__(self):
        return f"Node: {self.indexes}"

    def __repr__(self):
        return f"Cell[{self.indexes}]"


# column header cell which stores name and size
class HeaderCell(Cell):
    __slots__ = ["name", "size", "is_first"]

    def __init__(self, name):
        super(HeaderCell, self).__init__()
        self.size = 0
        self.name = name
        self.is_first = False


# Dancing links matrix stores a Doubly Circular Linked List and the column header of another list
# Each cell points to its Up, Down, Left, and Right neighbors
class DancingLinksMatrix:

    # Create a Dancing Links Matrix
    def __init__(self, columns):

        self.header = HeaderCell("<H>")
        self.header.is_first = True
        self.rows = self.cols = 0
        self.col_list = []
        self._create_column_headers(columns)

    # The column can be int or iterable
    # If column is int, columns are added to the matrix, named C + "N", where N = columns - 1
    # otherwise column is iterable, number and name of the columns are deduced
    # The iterable could be the name, or a tuple(name, primary)
    # Where primary is a bool, true if the column is primary, the defalut value is true
    def _create_column_headers(self, columns):
        if isinstance(columns, int):
            columns = int(columns)
            col_names = (f"C{i}" for i in range(columns))
        else:
            try:
                col_names = iter(columns)

            # if column is not a number neither an iterable
            except TypeError:
                raise TypeError("Argument is not valid")

        prev = self.header

        # create a for loop to link all the columns
        for name in col_names:
            if isinstance(name, tuple):
                name, primary = name
            else:
                primary = True
            cell = HeaderCell(name)
            cell.indexes = (-1, self.cols)
            cell.is_first = False
            self.col_list.append(cell)
            if primary:
                prev.R = cell
                cell.L = prev
                prev = cell
            self.cols += 1

        prev.R = self.header
        self.header.L = prev

    # Add a sparse row to the matrix
    # The row is in format [ind_0, ..., ind_n] where 0 <= ind_i < dl_matrix.ncols
    # row is a sequence of integers indicating the 1s in the row.
    def add_sparse_row(self, row, already_sorted=False):

        # if end_add was already called
        if self.col_list is None:
            raise CannotAddRows()

        prev = None
        start = None

        if not already_sorted:
            row = sorted(row)

        cell = None

        for ind in row:
            cell = Cell()
            cell.indexes = (self.rows, ind)

            if prev:
                prev.R = cell
                cell.L = prev
            else:
                start = cell

            col = self.col_list[ind]

            # link the cell with prev and right cells
            last = col.U
            last.D = cell
            cell.U = last
            col.U = cell
            cell.D = col
            cell.C = col
            col.size += 1
            prev = cell

        start.L = cell
        cell.R = start
        self.rows += 1

    # end when no more rows need add
    def end_add(self):
        self.col_list = None

    # return column header with least 1s
    def min_column(self):

        # if the matrix is empty
        if self.header.R.is_first:
            raise EmptyDLMatrix()

        col_min = self.header.R

        for col in iterate_cell(self.header, 'R'):
            if not col.is_first and col.size < col_min.size:
                col_min = col

        return col_min

    #  if no minimum 1s found, return a random column header
    def random_column(self):

        col = self.header.R

        # if the matrix is empty
        if col is self.header:
            raise EmptyDLMatrix()

        n = random.randint(0, self.cols - 1)

        for _ in range(n):
            col = col.R

        if col.is_first:
            col = col.R
        return col

    def __str__(self):
        names = []
        m = np.zeros((self.rows, self.cols), dtype=np.uint8)
        rows, cols = set(), []

        for col in iterate_cell(self.header, 'R'):
            cols.append(col.indexes[1])

            names.append(col.name)

            for cell in iterate_cell(col, 'D'):
                ind = cell.indexes
                rows.add(ind[0])
                m[ind] = 1

        m = m[list(rows)][:, cols]
        return "\n".join([", ".join(names), str(m)])

    @staticmethod

    # Covers the column c by removing the 1s in the column
    # also all the rows connected to them
    # c is column header of the column that has to be covered.
    def cover(c):

        # print("Cover column", c.name)
        c.R.L = c.L
        c.L.R = c.R

        for i in iterate_cell(c, 'D'):
            for j in iterate_cell(i, 'R'):
                j.D.U = j.U
                j.U.D = j.D
                j.C.size -= 1

    @staticmethod

    # Uncovers the column c by readding the 1s in the column
    # also all the rows connected to them.
    # c is the column header of the column that has to be uncovered.
    def uncover(c):

        for i in iterate_cell(c, 'U'):
            for j in iterate_cell(i, 'L'):
                j.C.size += 1
                j.D.U = j.U.D = j

        c.R.L = c.L.R = c


def iterate_cell(cell, direction):
    cur = getattr(cell, direction)
    while cur is not cell:
        yield cur
        cur = getattr(cur, direction)


class MatrixDisplayer:

    def __init__(self, matrix):
        dic = {}

        for col in iterate_cell(matrix.header, 'R'):
            dic[col.indexes] = col

        for col in iterate_cell(matrix.header, 'R'):
            first = col.D
            dic[first.indexes] = first
            for cell in iterate_cell(first, 'D'):
                if cell is not col:
                    dic[cell.indexes] = cell

        self.dic = dic
        self.rows = matrix.rows
        self.cols = matrix.cols

    def print_matrix(self):
        m = {}

        for i in range(-1, self.rows):
            for j in range(0, self.cols):
                cell = self.dic.get((i, j))
                if cell:
                    if i == -1:
                        m[0, 2 * j] = cell.name
                    else:
                        m[2 * (i + 1), 2 * j] = "X"

        for i in range(-1, self.rows * 2):
            for j in range(0, self.cols * 2):
                print(m.get((i, j), " "), end=" ")
            print()