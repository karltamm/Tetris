import random, copy
from shapes import *
from board import *
from screen import *
from database import *

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
        self.is_locked = False
        self.time_since_movement = 0

        if self.updateBoard(board) == False:  # No room for new block, so game over
            # Notify program that game is over
            pygame.event.post(pygame.event.Event(GAME_OVER))
            playSound(GAME_OVER_SOUND)

    def move(self, board, x_step=0, y_step=0, autofall=False):
        move_success = False
        self.x += x_step
        self.y += y_step

        if not self.updateBoard(board):
            # Error: block couldn't be moved
            self.x -= x_step
            self.y -= y_step

            if x_step == 0:  # Block didn't side collide with any other block
                self.is_placed = True  # Block can't go any lower, so it's placed
                self.is_locked = True  # Block can't be moved anymore
                move_success = True
        # Move was successful so play sound
        else:
            move_success = True
            self.is_locked = False
        if move_success and not autofall:
            self.time_since_movement = pygame.time.get_ticks()
            playSound(MOVE3_SOUND)
        return move_success


    def rotate(self, board):
        rotate_success = False

        if self.rotation == 3:
            self.rotation = -1
        self.rotation += 1

        if not self.updateBoard(board):  # Rotate failed
            # If block on the leftmost side (means rotate was out of bounds)
            if self.x == -1:
                self.x += 1
                if not self.updateBoard(board):
                    self.x -= 1
                else:
                    self.rotation += 1
                    rotate_success = True
            # If block on the rightmost side
            elif self.x == 8:
                if self.shape == SHAPE_I:
                    self.x -= 1
                self.x -= 1
                if not self.updateBoard(board):
                    if self.shape == SHAPE_I:
                        self.x += 1
                    self.x += 1
                else:
                    self.rotation += 1
                    rotate_success = True
            else:
                for i in range(1, 4):
                    self.y -= i
                    if not self.updateBoard(board):
                        self.y += i
                    else:
                        self.rotation += 1
                        rotate_success = True
                        break
            self.rotation -= 1

        else:
            rotate_success = True
        # Rotation was successful so play sound
        if rotate_success and self.shape != SHAPE_O:
            self.is_locked = False
            self.time_since_movement = pygame.time.get_ticks()
            playSound(ROTATE_SOUND)


    def removeCellsFromBoard(self, board):
        for row, col in self.used_board_cells:
            board[row][col] = 0

    def updateBoard(self, board):
        new_board = copyBoard(board)
        self.removeCellsFromBoard(new_board)
        temp_used_board_cells = []

        # Check whether block can be placed on board area (4x4 cells)
        for row in range(self.y, self.y + BLOCK_HEIGHT):
            for col in range(self.x, self.x + BLOCK_WIDTH):
                block_cell = self.shape[self.rotation][row - self.y][col - self.x]

                if block_cell != 0:
                    if -1 < col < BOARD_WIDTH and row < BOARD_HEIGHT:
                        if new_board[row][col] == 0 or new_board[row][
                            col] == 8:  # No collision with cells of 0 or 8 value
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

    def movedToCursor(self, board, mouse_pos):
        for index, x_pos in enumerate(range(BOARD_X, BOARD_X_END + BOARD_CELL, BOARD_CELL)):
            if mouse_pos[0] < x_pos:
                # Calculate distance between cursor and current block pos
                # index - 2 to grab the center of blocks
                distance = abs(self.x - (index - 2))
                if self.x > (index - 2):
                    for _ in range(distance):
                        self.move(board, x_step = -1)
                elif self.x < (index - 2):
                    for _ in range(distance):
                        self.move(board, x_step = +1)  
                self.updateBoard(board)
                return True
        return False

# CHILD CLASS OF "Block"
class ShadowBlock(Block):
    def __init__(self, current_block, board):
        if optionsValues("block_shadows"):  # If block shadows are turned on
            shape = copy.deepcopy(current_block.shape)
            rotation = current_block.rotation

            for row in range(len(shape[rotation])):
                for col in range(len(shape[rotation][row])):
                    if shape[rotation][row][col] != 0:
                        # Nt O kujund, [[0, 2, 2, 0][0, 2, 2, 0]...] -> [[0, 8, 8, 0][0, 8, 8, 0]...]
                        shape[rotation][row][col] = 8

            self.shape = shape
            self.rotation = rotation
            self.x = current_block.x
            self.y = current_block.y
            self.used_board_cells = []
            self.is_placed = False
            self.board = board

            # Drops shadow block down to position
            self.drop(board, current_block)

    def drop(self, board, current_block):
        while not self.is_placed:
            if self.placeShadow(board, current_block):
                self.y += 1
            else:
                self.is_placed = True

    def placeShadow(self, board, current_block):
        new_board = copyBoard(board)
        self.removeCellsFromBoard(new_board)
        temp_used_board_cells = []

        # Check whether block can be placed on board area (4x4 cells)
        for row in range(self.y, self.y + BLOCK_HEIGHT):
            for col in range(self.x, self.x + BLOCK_WIDTH):
                shadow_block_cell = self.shape[self.rotation][row - self.y][col - self.x]
                if shadow_block_cell != 0:
                    if -1 < col < BOARD_WIDTH and row < BOARD_HEIGHT:
                        # No collision with cells of 0 or 8 value
                        if new_board[row][col] == 0 or new_board[row][col] == 8:
                            # Cell isn't occupied by another block
                            new_board[row][col] = shadow_block_cell
                            temp_used_board_cells.append((row, col))
                        else:  # Ignores collision with current block
                            cb_collision = False
                            for cb_row in range(current_block.y, current_block.y + BLOCK_HEIGHT):
                                current_block_cell = current_block.shape[current_block.rotation][
                                    cb_row - current_block.y][col - current_block.x]
                                # Ignores, if shadow block collides with current block
                                # unless placed block is in current blocks 4x4 area
                                if cb_row == row and new_board[row][col] == current_block_cell:
                                    cb_collision = True
                                    break
                            if not cb_collision:
                                return False  # Error: blocks can't overlap
                    else:
                        return False  # Error: block would be out of bounds

        # Block placed, board updated
        self.used_board_cells = temp_used_board_cells
        copyBoard(new_board, board)
        return True  # Block placement was successful

    def clearShadow(self, board):
            for row in range(BOARD_HEIGHT):
                for col in range(BOARD_WIDTH):
                    if board[row][col] == 8:
                        board[row][col] = 0


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
        if len(self.blocks) == 0:
            self.newBatch()

        return self.blocks.pop()
