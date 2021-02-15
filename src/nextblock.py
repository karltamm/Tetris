import random
from shapes import *
from board import *

# CONSTANTS
NEXT_BLOCK_AREA_WIDTH = 4  # Number of board cells in a row
NEXT_BLOCK_AREA_HEIGHT = 5  # Number of board cells in a column


# CLASS
class NextBlock:
    def __init__(self, shape, next_block_area, x=0, y=1):
        self.shape = shape
        self.x = x
        self.y = y

        self.updateBlockPreview(next_block_area)

    def updateBlockPreview(self, next_block_area):
        new_area = copyNextBlockArea(next_block_area)

        for row in range(self.y, self.y + BLOCK_HEIGHT):
            for col in range(self.x, self.x + BLOCK_WIDTH):
                block_cell = self.shape[1][row - self.y][col - self.x]
                new_area[row][col] = block_cell

        copyNextBlockArea(new_area, next_block_area)


# FUNCTIONS
def createNextBlockArea():
    return [[0] * NEXT_BLOCK_AREA_WIDTH for row in
            range(NEXT_BLOCK_AREA_HEIGHT)]  # 2D array, where "0" represents empty cell


def copyNextBlockArea(src, dest=0):
    if dest == 0:
        dest = createNextBlockArea()

    for row in range(NEXT_BLOCK_AREA_HEIGHT):
        for col in range(NEXT_BLOCK_AREA_WIDTH):
            dest[row][col] = src[row][col]

    return dest


def getNextBlock(block, next_block_area):
    NextBlock(block, next_block_area)
    return block
