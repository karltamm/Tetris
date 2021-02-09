from settings import *
from functions import *

class Block:
    def __init__(self, shape, board):
        self.shape = shape
        self.rotation = 0
        self.x = 0  # In which board column is top-left block cell?
        self.y = 0  # In which board row is top-left block cell?
        self.used_board_cells = [] # [(row, col), (row, col) etc]
        self.updateBoard(board)

    def move(self, board, x_step = 0, y_step = 0):
        self.x += x_step;
        self.y += y_step;
        if self.updateBoard(board) == False:
            # Error: block couldn't be moved
            self.x -= x_step
            self.y -= y_step

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
                    if row < BOARD_HEIGHT and col < BOARD_WIDTH and col > -1:
                        if new_board[row][col] == 0:
                            # Cell isn't occupied by another block
                            new_board[row][col] = block_cell
                            temp_used_board_cells.append((row, col))
                        else:
                            return False  # Error: block can't overlap
                    else:
                        return False  # Error: block would be out of bounds
        # Block placed, board updated
        self.used_board_cells = temp_used_board_cells
        copyBoard(new_board, board)
        return True  # Block placement was successful

def randomShape(board):
    return Block(random.choice(shapes), board)