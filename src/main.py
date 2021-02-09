import pygame
import os
import random

from shapes import *

# CONSTANTS
# Screen
SCREEN_WIDTH = 300  # px
SCREEN_HEIGHT = 500  # px

FPS = 60

# Board
BOARD_WIDTH = 10  # Number of cells in a row
BOARD_HEIGHT = 20  # Number of cells in a column

BOARD_CELL = 20  # 20 px square

BOARD_X = 50 # Number of px from left edge of the screen
BOARD_Y = 50 # Number of px from top of the screen

BLOCK_WIDTH = BLOCK_HEIGHT = 4  # Block is made of 4x4 board cells

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Tetris")

# ASSETS
# Cells
EMPTY_CELL = pygame.image.load(os.path.join("assets/cells", "empty.png"))
GREEN_CELL = pygame.image.load(os.path.join("assets/cells", "green.png"))
INDIGO_CELL = pygame.image.load(os.path.join("assets/cells", "indigo.png"))
ORANGE_CELL = pygame.image.load(os.path.join("assets/cells", "orange.png"))
PINK_CELL = pygame.image.load(os.path.join("assets/cells", "pink.png"))
RED_CELL = pygame.image.load(os.path.join("assets/cells", "red.png"))
YELLOW_CELL = pygame.image.load(os.path.join("assets/cells", "yellow.png"))
BLUE_CELL = pygame.image.load(os.path.join("assets/cells", "blue.png"))

# FUNCTIONS
# Game states
def gameOver():
    pass

# Board
def createBoard():
    return [[0]*BOARD_WIDTH for row in range(BOARD_HEIGHT)] # 2D array, where "0" represents empty cell

def printBoard(board):
    for row in range(BOARD_HEIGHT):
        print()
        for col in range(BOARD_WIDTH):
            print(board[row][col], end = " ")

    print()
    
def copyBoard(src, dest = 0):
    if dest == 0:
        dest = createBoard()
        
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            dest[row][col] = src[row][col]

    return dest

def clearFullRows(board):
    # Go through every board row and check if row is full
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                break # Row isn't full

            if col == BOARD_WIDTH - 1: # Last column has been checked and row is full
                board.pop(row)
                board.insert(0, [0]*BOARD_WIDTH)

# Block
class Block:
    def __init__(self, shape, board):
        self.shape = shape
        self.rotation = 0

        self.x = 0  # In which board column is top-left block cell?
        self.y = 0  # In which board row is top-left block cell?

        self.used_board_cells = [] # [(row, col), (row, col) etc]

        if self.updateBoard(board) == False: # No room for new block, so game over
            gameOver()


    def move(self, board, x_step = 0, y_step = 0):
        self.x += x_step;
        self.y += y_step;
        if self.updateBoard(board) == False:
            # Error: block couldn't be moved
            self.x -= x_step
            self.y -= y_step
            return True
        return False


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

def randomBlock(board):
    return Block(random.choice(SHAPES), board)

# UI
def updateScreen(board):
    # Update board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                SCREEN.blit(EMPTY_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 1:
                SCREEN.blit(GREEN_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 2:
                SCREEN.blit(INDIGO_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 3:
                SCREEN.blit(ORANGE_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 4:
                SCREEN.blit(PINK_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 5:
                SCREEN.blit(RED_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 6:
                SCREEN.blit(YELLOW_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))
            elif board[row][col] == 7:
                SCREEN.blit(BLUE_CELL, (BOARD_X + col*BOARD_CELL, BOARD_Y + row*BOARD_CELL))

    pygame.display.update()

# MAIN
def main():
    board = createBoard() # 2D array, where "0" represents empty cell

    downPressed = False # For holding down "DOWN" key
    leftPressed = False
    rightPressed = False
    keyPress_timer = 0

    currentBlock = randomBlock(board) # Generates random shape into currentBlock
    changeBlock = False
    fall_timer = 0
    fall_speed = 25 # Lower value -> Faster drop speed

    run = True
    while run:
        CLOCK.tick(FPS)
        
        keyPress_timer += 1 # For block moving "speed" when holding down a key
        # Block automatic dropping
        fall_timer += 1
        if fall_timer > fall_speed:
            fall_timer = 0
            changeBlock = currentBlock.move(board, 0, 1)

        # Input
        for event in pygame.event.get():
            # Close game
            if event.type == pygame.QUIT:
                run = False
                exit()
            
            if event.type == pygame.KEYDOWN: # If a key is pressed down
                if event.key == pygame.K_UP:
                    currentBlock.rotate(board)
                elif event.key == pygame.K_DOWN:
                    downPressed = True
                    keyPress_timer = 0
                elif event.key == pygame.K_RIGHT:
                    rightPressed = True
                    keyPress_timer = 0
                elif event.key == pygame.K_LEFT:
                    leftPressed = True
                    keyPress_timer = 0
                    
            elif event.type == pygame.KEYUP: # If a key is released
                if event.key == pygame.K_DOWN:
                    downPressed = False
                elif event.key == pygame.K_RIGHT:
                    rightPressed = False
                elif event.key == pygame.K_LEFT:
                    leftPressed = False
                    
        if downPressed and keyPress_timer % 3 == 0:
                changeBlock = currentBlock.move(board, 0, 1)
        if rightPressed and keyPress_timer % 10 == 0:
                currentBlock.move(board, 1, 0)
        if leftPressed and keyPress_timer % 10 == 0:
                currentBlock.move(board, -1, 0)
        if changeBlock:
            clearFullRows(board)
            currentBlock = randomBlock(board)
            changeBlock = False

        # UI
        updateScreen(board)

main()