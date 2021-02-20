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
        self.block_selection = []
        self.block_under_cursor = None
        self.start_time = None

    def start(self, board_params=None):
        self.is_running = True

        if board_params is not None:
            self.board, self.current_block, shadow_block = board_params
            temporarilyRemoveCurrentBlock(self.board, self.current_block, shadow_block)

        if self.name == "Wishlist":
            self.createBlockSelection()

            # A part of blocks selection shares screen area with power activation button. If user clicks on a button then this can automaticly triger certain block selection. Do not allow to choose a block if certain amount of time hasn't elapsed since selection area became avaialable. This gives time for player to actually see the selection and make a choice
            self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.is_running = False
        self.is_available = False  # TESTING!

        if self.name == "Laser":
            rewindCurrentBlock(self.current_block, self.board)

        elif self.name == "Wishlist":
            rewindCurrentBlock(self.current_block, self.board)

    def run(self, UI_control=None):
        if self.name == "Laser":
            self.runLaser(UI_control)
        elif self.name == "Wishlist":
            self.runWishlist(UI_control)

    # LASER
    def runLaser(self, UI_control):
        mouse_pos, events = UI_control  # Unpack tuple
        self.getRowUnderCursor(mouse_pos)

        # Remove the row if player clicked on it
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.row is not None:
                    self.removeSelectedRow()
                    self.stop()

    def getRowUnderCursor(self, mouse_pos):
        self.row = None

        # Is cursor even on game board?
        if mouse_pos[0] > BOARD_X and mouse_pos[0] < BOARD_X_END:
            if mouse_pos[1] > BOARD_Y and mouse_pos[1] < BOARD_Y_END:
                # Check on which row cursor currently is
                for index, y_pos in enumerate(range(BOARD_Y, BOARD_Y_END + BOARD_CELL, BOARD_CELL)):
                    if mouse_pos[1] < y_pos:
                        # Found the row under the cursor
                        self.row = (index - 1, y_pos - BOARD_CELL)
                        break

    def removeSelectedRow(self):
        self.board.pop(self.row[0])
        self.board.insert(0, [0] * BOARD_WIDTH)
        LASER_SOUND.play()

    # WISHLIST
    def runWishlist(self, UI_control):
        mouse_pos, events = UI_control  # Unpack tuple
        self.getBlockUnderCursor(mouse_pos)

        # Select the block if player clicked on it
        if pygame.time.get_ticks() - self.start_time > 500:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.block_under_cursor is not None:
                        self.changeCurrentBlockShape()
                        self.stop()

    def createBlockSelection(self):
        for index, block_image in enumerate(BLOCK_IMAGES):
            block_area = block_image.get_rect()
            block_area.topleft = ((BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * index))
            self.block_selection.append((index, block_area))

    def getBlockUnderCursor(self, mouse_pos):
        self.block_under_cursor = None

        for block in self.block_selection:
            if block[1].collidepoint(mouse_pos):  # block[1] = block_area
                self.block_under_cursor = block
                break  # Found the block, no need to continue

    def changeCurrentBlockShape(self):
        self.current_block.shape = SHAPES[self.block_under_cursor[0]]
        APPEAR_SOUND.play()


# FUNCTIONS
def temporarilyRemoveCurrentBlock(board, current_block, shadow_block):
    current_block.removeCellsFromBoard(board)
    shadow_block.clearShadow(board)


def rewindCurrentBlock(current_block, board):
    current_block.x = 4
    current_block.y = 0
    current_block.rotation = 0
    current_block.updateBoard(board)
