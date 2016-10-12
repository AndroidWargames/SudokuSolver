import os
from math import log2

# class implemented by creating a 9x9 grid of int values
# ints range from 0 to 511, and each int represents the range of possibilities for that square.
# each value is the logical and of 2 to the power of each possible value minus 1
# e.g. 3, 7 and 6 are possible values, the int will be (2 ** 2 & 2 ** 6 & 2 ** 5)


class Sudoku:
    def __init__(self, loc):
        self.master = self.readPuzzle(loc)
        if not self.master:
            exit(76)
        print(list(map(len, self.master)))
        self.queue = []
        self.processed = [[False for x in range(9)] for y in range(9)]
        print(len(self.master))
        self.initSweep()
        print(self.printProgress(self.master))

    # coverts input to array of values
    def readPuzzle(self, loc):
        with open(loc, 'r') as f:
            content = f.readlines()
        f.close()
        content = [list(x)[:9] for x in content]
        print(content)
        content = [[2 ** (int(x) - 1) if x.isdigit() else 2 ** 9 - 1 for x in y] for y in content]
        if len(content) != 9 or len(content[0]) != 9:
            return False
        return content

    # given y coordinate, returns array of values in containing column
    def getCol(self, diag, col):
        return [x[col] for x in diag]

    # given x, y coordinates, returns array of values in containing box
    def getBox(self, diag, x, y):
        x //= 3
        y //= 3
        out = []
        for i in range(3):
            for j in range(3):
                out.append(diag[x * 3 + i][y * 3 + j])
        return out

    def getRow(self, diag, x):
        return diag[x]

    def pushRow(self, diag, x, a):
        for i in range(9):
            diag[x][i] = a[i]
            self.queuePush(x, i)
        return diag

    # given diagram, x, y, and array, returns diagram with box updated with array values
    def pushBox(self, diag, x, y, a):
        x //= 3
        y //= 3
        for i in range(3):
            for j in range(3):
                diag[x * 3 + i][y * 3 + j] = a[i * 3 + j]
                self.queuePush(x * 3 + i, y * 3 + j)
        return diag

    # given diagram, y coordinate, and array, returns diagram with column updated with array values
    def pushCol(self, diag, y, a):
        for i in range(9):
            diag[i][y] = a[i]
            self.queuePush(i, y)
        return diag

    # returns amalgam of known values in given array
    def getHits(self, a):
        out = 0
        for i in a:
            if self.done(i):
                out |= i
        return out ^ 511

    def initSweep(self):
        print(list(map(len, self.master)))
        for i in range(9):
            print(list(map(len, self.master)))
            a = self.getBox(self.master, i, (i % 3) * 3)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushBox(self.master, i, (i % 3) * 3, a)
            print(list(map(len, self.master)))
            a = self.getCol(self.master, i)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushCol(self.master, i, a)
            print(list(map(len, self.master)))
            a = self.getRow(self.master, i)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushRow(self.master, i, a)
        pass

    def done(self, a):
        return log2(a) == log2(a) // 1

    # pushes to queue if necessary
    def queuePush(self, x, y):
        if not self.processed[x][y] and self.done(self.master[x][y]):
            self.queue.append([x, y])
            self.processed[x][y] = True
        pass

    def clearVals(self, a, b):
        if len(a) < 9:
            print(a)
            print(a[9])
        return [x & b if not self.done(x) else x for x in a]

    # returns string that prints current progress of
    def printProgress(self, diag=[]):
        if diag == []:
            diag = self.master
        out = '\n'.join([''.join([str(int(log2(x)) + 1) if log2(x) == log2(x) // 1 else ' ' for x in y]) for y in diag])
        return out


sudoku = Sudoku(os.path.dirname(os.path.realpath(__file__)) + '/p1')

