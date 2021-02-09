import random
from shapes import *
from board import *

SMALLBOARD_WIDTH = 4  # Number of board cells in a row
SMALLBOARD_HEIGHT = 11  # Number of board cells in a column


# CLASS
class NextBlocks:
    def __init__(self, shape, small_board, x=0, y=0):
        self.shape = shape

        self.x = x
        self.y = y

        self.updateBoard(small_board)

    def updateBoard(self, small_board):
        new_board = copySmallBoard(small_board)
        for row in range(self.y, self.y + BLOCK_HEIGHT):
            for col in range(self.x, self.x + BLOCK_WIDTH):
                block_cell = self.shape[1][row - self.y][col - self.x]
                copySmallBoard(new_board, small_board)
                new_board[row][col] = block_cell

# FUNCTIONS
def createSmallBoard():
    return [[0]*SMALLBOARD_WIDTH for row in range(SMALLBOARD_HEIGHT)] # 2D array, where "0" represents empty cell

def copySmallBoard(src, dest=0):
    if dest == 0:
        dest = createSmallBoard()

    for row in range(SMALLBOARD_HEIGHT):
        for col in range(SMALLBOARD_WIDTH):
            dest[row][col] = src[row][col]
    return dest

def randomBlock(small_board,x,y):
    block = random.choice(SHAPES)
    NextBlocks(block,small_board,x,y)
    return block
