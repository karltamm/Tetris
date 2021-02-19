import random
from screen import *
from assets import *

# CONSTANTS
POWERS = ["Laser", "Wishlist"]


# CLASS
class Power:
    def __init__(self):
        self.is_available = True
        self.is_running = False
        # self.name = random.choice(POWERS)
        self.name = "Wishlist"  # Only for testing!

        self.highlight_board = False
        self.board = None
        self.current_block = None

        # Laser specific
        self.row = None

        # Wishlist
        self.selection = []

    def start(self, board_params=None):
        self.is_running = True

        if board_params is not None:
            self.board, self.current_block, shadow_block = board_params
            temporarilyRemoveCurrentBlock(self.board, self.current_block, shadow_block)

        if self.name == "Wishlist":
            self.createBlockSelection()

    def stop(self):
        self.is_running = False
        self.is_available = True  # TESTING!

        if self.name == "Laser":
            rewindCurrentBlock(self.current_block, self.board)

        elif self.name == "Wishlist":
            rewindCurrentBlock(self.current_block, self.board)

    def run(self, UI_control=None):
        if self.name == "Laser":
            self.runLaser(UI_control)
        elif self.name == "Wishlist":
            self.runWishlist(UI_control)

    # Laser
    def runLaser(self, UI_control):
        # Unpack tuple
        mouse_pos, events = UI_control

        self.row = getRowUnderCursor(mouse_pos)  # also for screen.py function

        # Remove the row if player clicked on it
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playerChoseRow(mouse_pos, *self.row):
                    removeSelectedRow(self.board, *self.row)
                    self.stop()  # Job done

    # Wishlist
    def runWishlist(self, UI_control):
        # Unpack tuple
        mouse_pos, events = UI_control

        self.getBlockUnderCursor(mouse_pos)

    def createBlockSelection(self):
        for i, block in enumerate(BLOCK_IMAGES):
            block = block.get_rect()
            block.topleft = ((BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * i))
            self.selection.append(block)

    def getBlockUnderCursor(self, mouse_pos):
        for index, block in enumerate(self.selection):
            if block.collidepoint(mouse_pos):
                break


# FUNCTIONS
def temporarilyRemoveCurrentBlock(board, current_block, shadow_block):
    current_block.removeCellsFromBoard(board)
    shadow_block.clearShadow(board)


def rewindCurrentBlock(current_block, board):
    current_block.x = 4
    current_block.y = 0
    current_block.updateBoard(board)


# Laser
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


def removeSelectedRow(board, row_y, row_index):
    board.pop(row_index)
    board.insert(0, [0] * BOARD_WIDTH)
    LASER_SOUND.play()
