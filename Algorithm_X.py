from DancingLinksMatrix import iterate_cell


# this is an implementation of Algorithm_X
class AlgorithmX:

    # Alg_X object to solve the problem translate into matrix
    def __init__(self, matrix, callback, find_min=True):

        self.solu_dict = {}
        self.stop = False
        self.matrix = matrix  # The DL_Matrix instance

        # The callback called on every solution
        # callback should be a function, which taking a dict argument
        # {row_index: linked list of the row}, and can return a bool value
        # The solver will keep running until the callback returns true
        self.callback = callback

        self.find_min = find_min

    def _create_sol(self, k):

        # generates a solution from the inner dict
        solu = {}
        for key, row in self.solu_dict.items():
            if key >= k:
                continue

            tmp_list = [row.C.name]
            tmp_list.extend(r.C.name for r in iterate_cell(row, 'R'))
            solu[row.indexes[0]] = tmp_list

        return solu

    def _search(self, k):

        if self.matrix.header.R == self.matrix.header:

            # matrix is empty now, solution founded, return true
            if self.callback(self._create_sol(k)):
                self.stop = True
            return

        # if true, choose the column with least 1s to iterate
        if self.find_min:
            col = self.matrix.min_column()

        # if false, randomly choose a column
        else:
            col = self.matrix.random_column()

        # cover column col
        self.matrix.cover(col)

        row = col.D

        for row in iterate_cell(col, 'D'):
            self.solu_dict[k] = row

            # cover the columns pointed by the 1s in the chosen row
            for j in iterate_cell(row, 'R'):
                self.matrix.cover(j.C)

            self._search(k + 1)
            if self.stop:
                return

            # if colunms uncover
            row = self.solu_dict[k]
            col = row.C

            for j in iterate_cell(row, 'L'):
                self.matrix.uncover(j.C)

        self.matrix.uncover(col)

    def __call__(self):

        # search starts
        self._search(0)