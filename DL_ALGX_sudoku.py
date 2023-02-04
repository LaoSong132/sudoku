import itertools as it
import numpy as np

from Algorithm_X import AlgorithmX
from DancingLinksMatrix import DancingLinksMatrix
from Board import Sudoku_Board


def column_names():
    # 81, RiCj = j + 9i
    for i, j in it.product(range(1, 10), repeat=2):
        yield f"R{i}C{j}"
    # 81, Ri#v = v + 9i
    for i, j in it.product(range(1, 10), repeat=2):
        yield f"R{i}#{j}"
    # 81, Cj#v = v + 9j
    for i, j in it.product(range(1, 10), repeat=2):
        yield f"C{i}#{j}"
    # 81, Bn#v = v + 9n
    for i, j in it.product(range(1, 10), repeat=2):
        yield f"B{i}#{j}"


def get_square_index(m, n):
    m, n = m // 3, n // 3
    return 3 * m + n


def compute_row(m, n, v):
    m -= 1
    n -= 1
    v -= 1
    i1 = n + 9 * m
    i2 = 81 + v + 9 * m
    i3 = 81 * 2 + v + 9 * n
    i4 = 81 * 3 + v + 9 * get_square_index(m, n)
    return [i1, i2, i3, i4]


class GetFirstSol:

    def __init__(self):
        self.sol = None

    def __call__(self, sol):
        matrix = np.zeros((9, 9), dtype=np.uint8)

        for v in sol.values():
            m, n, val = 0, 0, 0
            for el in v:
                if el[2] == "#":
                    val = int(el[3])
                else:
                    m, n = map(int, [el[1], el[3]])
            matrix[m - 1, n - 1] = val

        self.sol = matrix
        return True


class CountSolutions:

    def __init__(self):
        self.count = 0

    def __call__(self, _):
        self.count += 1


def read_from_file(file_path):
    test_file = {}
    with open(file_path) as f_in:
        for m, line in enumerate(f_in, start=1):
            for n, char in enumerate(line.rstrip(), start=1):
                try:
                    test_file[m, n] = int(char)
                except ValueError:
                    pass
    return test_file


def to_np(test_file):
    matrix = np.zeros((9, 9), dtype=np.uint8)

    for ((m, n), v) in test_file.items():
        matrix[m - 1, n - 1] = v

    return matrix


import sys

filename = sys.argv[1]


def main():
    matrix = DancingLinksMatrix(column_names())

    test_file = read_from_file(filename)

    inital_board = Sudoku_Board(to_np(test_file))

    print("----------INITAL BOARD-----------")
    print(inital_board)

    for i, j in it.product(range(1, 10), repeat=2):
        if (i, j) in test_file:
            row = compute_row(i, j, test_file[i, j])
            matrix.add_sparse_row(row, already_sorted=True)
        else:
            for v in range(1, 10):
                row = compute_row(i, j, v)
                matrix.add_sparse_row(row, already_sorted=True)

    matrix.end_add()

    sol = GetFirstSol()

    try:
        alg = AlgorithmX(matrix, sol)
        alg()

        board = Sudoku_Board(sol.sol)
        print()
        print("----------SOLUTION BOARD---------")
        print(board)
        print()
        print("Is the board vaild:", board.valid())
        print()
    except KeyboardInterrupt:
        pass
    finally:
        pass


import time
import tracemalloc

if __name__ == '__main__':

    # calculate the running time

    start_time = time.time()
    tracemalloc.start()

    main()

    run_time1 = (time.time() - start_time) * 1000

    print("%s milliseconds" % run_time1)
    print()

    # space using
    print("space using:", tracemalloc.get_traced_memory())

    tracemalloc.stop()

# test runs
total_time = 0


def avg_run_time(total_time, i):

    for i in range(i):

        start_time = time.time()

        main()

        run_time = (time.time() - start_time) * 1000

        total_time += run_time

        i = i - 1

        print("#", i + 2, "run:", run_time)

    print("average time for", (total_time / i), "milliseconds")


# avg_run_time(total_time, 30)
