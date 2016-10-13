# create object
from Sudoku import Sudoku
import os


sudoku = Sudoku.Sudoku()

# read sudoku text
loc = os.path.dirname(os.path.realpath(__file__)) + '/p3'
with open(loc, 'r') as f:
    text = f.readlines()
f.close()
sudoku.readPuzzle(text)

#solve
if sudoku.solve():
    print('Solution Found!')
else:
    print('No solution...')
sudoku.printProgress()