import random
from shapes import *
from board import *
from screen import *

# EVENTS
GAME_OVER = pygame.USEREVENT + 1


# CLASS
class Block:
    def __init__(self, shape, board):
        self.shape = shape
        self.rotation = 0
        self.x = 4  # In which board column is top-left block cell?
        self.y = 0  # In which board row is top-left block cell?
        self.used_board_cells = []  # [(row, col), (row, col) etc]
        self.is_placed = False

        if self.updateBoard(board) == False:  # No room for new block, so game over
            # Notify program that game is over
            pygame.event.post(pygame.event.Event(GAME_OVER))
            GAME_OVER_SOUND.play()

    def move(self, board, x_step=0, y_step=0, autofall=False):
        move_success = False
        self.x += x_step
        self.y += y_step

        if self.updateBoard(board) == False:
            # Error: block couldn't be moved
            self.x -= x_step
            self.y -= y_step

            if x_step == 0:  # Block didn't side collide with any other block
                self.is_placed = True  # Block can't go any lower, so it's placed
                move_success = True
        # Move was successful so play sound
        else:
            move_success = True
        if move_success and not autofall:
            MOVE_SOUND.play()

    def rotate(self, board):
        rotate_success = False
        if self.rotation == 3:
            self.rotation = -1

        self.rotation += 1

        if self.updateBoard(board) == False:  # Rotate failed
            # If block on the leftmost side (means rotate was out of bounds)
            if self.x == -1:
                self.x += 1
                if self.updateBoard(board) == False:
                    self.x -= 1
                else:
                    self.rotation += 1
                    rotate_success = True
            # If block on the rightmost side
            elif self.x == 8:
                if self.shape == SHAPE_I:
                    self.x -= 1
                self.x -= 1
                if self.updateBoard(board) == False:
                    if self.shape == SHAPE_I:
                        self.x += 1
                    self.x += 1
                else:
                    self.rotation += 1
                    rotate_success = True
            self.rotation -= 1
        else:
            rotate_success = True
        # Rotation was successful so play sound
        if rotate_success and self.shape != SHAPE_O:
            ROTATE_SOUND.play()

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


class BlocksBatch:
    def __init__(self):
        self.blocks = []
        self.newBatch()

    def newBatch(self):
        # Generate generic batch
        for index, shape in enumerate(SHAPES):
            self.blocks.append(shape)

        # Shuffle/randomize the order of shapes
        for i in range(50):
            block_1 = random.randint(0, len(SHAPES) - 1)
            block_2 = random.randint(0, len(SHAPES) - 1)

            temp = self.blocks[block_1]
            self.blocks[block_1] = self.blocks[block_2]
            self.blocks[block_2] = temp

    def getBlock(self):
        if len(self.blocks) > 0:
            return self.blocks.pop()
        else:
            self.newBatch()
            return self.blocks.pop()
