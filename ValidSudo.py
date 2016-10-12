# this function checks if sudoku solution is valid:

import os
from Sudoku import Sudoku
def validSudoku(input):
    # create object
    sudoku = Sudoku.Sudoku()
    sudoku.readPuzzle(input)
    for i in range(9):
        a = sudoku.getRow(sudoku.master, i)
        b = sudoku.getCol(sudoku.master, i)
        c = sudoku.getBox(sudoku.master, i, (i // 3) * 3)
        print(b)
        a.sort()
        b.sort()
        print(b)
        print(a == b)

# read sudoku txt
loc = os.path.dirname(os.path.realpath(__file__)) + '/p1.a'
with open(loc, 'r') as f:
    text = f.readlines()
f.close()

validSudoku(text)
