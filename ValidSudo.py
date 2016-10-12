# this function checks if sudoku solution is valid:

import os
from Sudoku import Sudoku
def validSudoku(input):
    # create object
    sudoku = Sudoku.Sudoku()
    sudoku.readPuzzle(input)
    ref = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    for i in range(9):
        a = sudoku.getRow(sudoku.master, i)
        b = sudoku.getCol(sudoku.master, i)
        c = sudoku.getBox(sudoku.master, i, (i // 3) * 3)
        for x in [a, b, c]:
            for j in ref:
                if j not in x:
                    print(x)
                    print(i)
                    print(a, b, c)
                    return False
    return True

# read sudoku txt
loc = os.path.dirname(os.path.realpath(__file__)) + '/p2.a'
with open(loc, 'r') as f:
    text = f.readlines()
f.close()

print(validSudoku(text))
