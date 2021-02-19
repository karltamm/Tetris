import random
from screen import *

# CONSTANTS
POWERS = ["Laser"]


# CLASS
class Power:
    def __init__(self):
        self.is_active = False
        self.name = random.choice(POWERS)
        self.highlight_board = False
        self.is_available = True

        # Laser specific
        self.row = None

    def activate(self):
        self.is_active = True
        self.is_available = False  # By activating, the power is currently used

    def deactivate(self, laser=None):
        self.is_active = False
        #self.is_available = True  # Only for testing!

        if laser is not None:
            rewindCurrentBlock(*laser)

    def run(self, laser=None):
        if self.name == "Laser":
            self.laserPower(laser)

    def laserPower(self, laser_parameters):
        # Unpack tuple
        mouse_pos, events, board, current_block, shadow_block = laser_parameters

        temporarilyRemoveCurrentBlock(current_block, shadow_block, board)
        self.row = getRowUnderCursor(mouse_pos)  # (also for screen.py function)

        # Remove the row if player clicked on it
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playerChoseRow(mouse_pos, *self.row):
                    removeSelectedRow(board, *self.row, current_block, shadow_block)
                    LASER_SOUND.play()
                    self.deactivate(laser=(current_block, board))


# FUNCTIONS
# Laser
def temporarilyRemoveCurrentBlock(current_block, shadow_block, board):
    current_block.removeCellsFromBoard(board)
    shadow_block.clearShadow(board)


def rewindCurrentBlock(current_block, board):
    current_block.x = 4
    current_block.y = 0
    current_block.updateBoard(board)


def getRowUnderCursor(mouse_pos):
    row_index = None
    row_y = None

    # Is cursor even on game board?
    if mouse_pos[0] > BOARD_X and mouse_pos[0] < BOARD_X_END:
        if mouse_pos[1] > BOARD_Y and mouse_pos[1] < BOARD_Y_END:
            # Check on which row cursor currently is
            for index, y_pos in enumerate(range(BOARD_Y, BOARD_Y_END + BOARD_CELL, BOARD_CELL)):
                if mouse_pos[1] < y_pos:
                    # Found the row under the cursor
                    row_y = y_pos - BOARD_CELL  # Remove 30 px (BOARD_CELL), because previous row is actually correct
                    row_index = index - 1
                    break

    return (row_y, row_index)


def playerChoseRow(mouse_pos, row_y, row_index):
    # Find out wheter user clicked on a row or not
    if row_y is not None:
        if mouse_pos[1] >= row_y and mouse_pos[1] <= row_y + BOARD_CELL:
            return True


def removeSelectedRow(board, row_y, row_index, current_block, shadow_block):
    # Temporarily remove current block from board
    # because otherwise current_block leaves a ghost image
    current_block.removeCellsFromBoard(board)

    # Remove shadow to avoid glitch
    shadow_block.clearShadow(board)

    # Remove the row and add new one
    board.pop(row_index)
    board.insert(0, [0] * BOARD_WIDTH)
