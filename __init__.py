import os
from math import log2

# class implemented by creating a 9x9 grid of int values
# ints range from 0 to 511, and each int represents the range of possibilities for that square.
# each value is the logical and of 2 to the power of each possible value minus 1
# e.g. 3, 7 and 6 are possible values, the int will be (2 ** 2 & 2 ** 6 & 2 ** 5)


class Sudoku:
    def __init__(self):
        self.master = []
        self.count = 0
        self.queue = []
        self.impasse = False
        self.processed = [[False for x in range(9)] for y in range(9)]

    # coverts input to array of values
    def readPuzzle(self, content):
        content = [list(x)[:9] for x in content]
        content = [[2 ** (int(x) - 1) if x.isdigit() else 2 ** 9 - 1 for x in y] for y in content]
        if len(content) != 9 or len(content[0]) != 9:
            return False
        self.master = content

    def solve(self):
        self.initSweep()
        while not self.impasse:
            self.queueProcess()
            if self.count == 81:
                break
            x, y, c = self.getMin()
            c = self.bin2nums(c)
            for i in c:
                a = self.getRow(self.master, x)
                a[y] = 2 ** (i - 1)
                diag = self.pushRow(self.master, x, a)
                temp = self.printProgress(diag=diag, auto=False)
                if temp == 'fail':
                    continue
                sudo = Sudoku()
                print(temp)
                sudo.readPuzzle(temp.split('\n'))
                if sudo.solve():
                    self.master = sudo.master
                    self.impasse = sudo.impasse
                    return True

        if self.count == 81:
            return True
        else:
            return False

    def bin2nums(self, a):
        i = 1
        out = []
        while a > 0:
            if a % 2 == 1:
                out.append(i)
            i += 1
            a //= 2
        return out

    def getMin(self):
        min = 10
        for i in range(9):
            for j in range(9):
                a = self.bits(self.master[i][j])
                if 1 < a < min:
                    min = a
                    out = [i, j, self.master[i][j]]
                if min == 2:
                    return out
        return out

    def queueProcess(self):
        while len(self.queue) > 0 and not self.impasse and self.count < 81:
            x, y = self.queue[0]
            a = self.getBox(self.master, x, y)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushBox(self.master, x, y, a)
            a = self.getCol(self.master, y)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushCol(self.master, y, a)
            a = self.getRow(self.master, x)
            b = self.getHits(a)
            a = self.clearVals(a, b)
            self.master = self.pushRow(self.master, x, a)
            del self.queue[0]
        pass

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
        for i in range(9):
            for j in range(9):
                if self.done(self.master[i][j]):
                    self.queuePush(i, j)
        pass

    def done(self, a):
        if a == 0:
            return False
        return log2(a) == log2(a) // 1

    # pushes to queue if necessary
    def queuePush(self, x, y):
        if not self.processed[x][y] and self.done(self.master[x][y]) and self.master[x][y] != 0:
            self.queue.append([x, y])
            self.processed[x][y] = True
            self.count += 1
        elif self.master[x][y] == 0:
            self.impasse = True
        pass

    def clearVals(self, a, b):
        return [x & b if not self.done(x) else x for x in a]

    def bits(self, i):
        i = i - ((i >> 1) & 0x55555555)
        i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
        return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

    # returns string that prints current progress of
    def printProgress(self, diag=[], auto=True):
        if diag == []:
            diag = self.master
        try:
            out = '\n'.join([''.join([str(int(log2(x)) + 1) if log2(x) == log2(x) // 1 else '|' for x in y]) for y in diag])
        except:
            out = 'fail'
            print(self.master)
        if auto:
            print(out)
        return out


