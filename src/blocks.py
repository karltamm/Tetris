import random
from shapes import *
from board import *
from screen import *

# CLASS
class Block:
    def __init__(self, shape, board):
        self.shape = shape
        self.rotation = 0

        self.x = 0  # In which board column is top-left block cell?
        self.y = 0  # In which board row is top-left block cell?

        self.used_board_cells = [] # [(row, col), (row, col) etc]

        self.is_placed = False

        if self.updateBoard(board) == False: # No room for new block, so game over
            pass # TODO: pygame custom event: game_over

    def move(self, board, x_step = 0, y_step = 0):
        self.x += x_step;
        self.y += y_step;

        if self.updateBoard(board) == False:
            # Error: block couldn't be moved
            self.x -= x_step
            self.y -= y_step 

            if x_step == 0: # Block didn't side collide with any other block
                self.is_placed = True # Block can't go any lower, so it's placed


    def rotate(self, board):
        if self.rotation == 3:
            self.rotation = -1
        
        self.rotation += 1
        
        if self.updateBoard(board) == False:
            self.rotation -= 1

    def removeOldCellsFromBoard(self, board):
        for row, col in self.used_board_cells:
            board[row][col] = 0

    def updateBoard(self, board):
        new_board = copyBoard(board)
        self.removeOldCellsFromBoard(new_board)
        
        temp_used_board_cells = []

        # Check whether block can be placed on board area (4x4 cells)
        for row in range(self.y, self.y + BLOCK_HEIGHT):
            for col in range(self.x, self.x + BLOCK_WIDTH):
                block_cell = self.shape[self.rotation][row - self.y][col - self.x]

                if block_cell != 0:
                    if col < BOARD_WIDTH and col > -1 and row < BOARD_HEIGHT:
                        if new_board[row][col] == 0:
                            # Cell isn't occupied by another block
                            new_board[row][col] = block_cell
                            temp_used_board_cells.append((row, col))
                        else:
                            return False  # Error: blocks can't overlap
                    else:
                        return False  # Error: block would be out of bounds

        # Block placed, board updated
        self.used_board_cells = temp_used_board_cells
        copyBoard(new_board, board)
        return True  # Block placement was successful

# FUNCTIONS
def randomBlock(board):
    return Block(random.choice(SHAPES), board)
