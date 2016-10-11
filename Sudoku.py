import os

# class implemented by creating a 9x9 grid of int values
# ints range from 0 to 511, and each int represents the range of possibilities for that square.
# each value is the logical and of 2 to the power of each possible value minus 1
# e.g. 3, 7 and 6 are possible values, the int will be (2 ** 2 & 2 ** 6 & 2 ** 5)

class Sudoku():
    def __init__(self, loc):
        self.master = self.readPuzzle(loc)
        if not self.master:
            return "bad diagram"
        print(self.master)

    def readPuzzle(self, loc):
        with open(loc, 'r') as f:
            content = f.readlines()
        f.close()
        content = [list(x)[:-1] for x in content]
        content = [[2 ** (int(x) - 1) if x.isdigit() else 2 ** 9 - 1 for x in y] for y in content]
        if len(content) != 9 or len(content[0]) != 9:
            return False
        return content

    def getColumn(self, diag, col):
        return [x[col] for x in self.]


sudoku = Sudoku(os.path.dirname(os.path.realpath(__file__)) + '/p1')

