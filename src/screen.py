import pygame
from board import *
from smallboard import *
from assets import *

# CONSTANTS
SCREEN_WIDTH = 400  # px
SCREEN_HEIGHT = 500  # px
FPS = 60

# Board UI
BOARD_CELL = 20  # 20 px square
BOARD_X = 50 # Number of px from left edge of the screen
BOARD_Y = 50 # Number of px from top of the screen

SMALLBOARD_X = 280 # Number of px from left edge of the screen
SMALLBOARD_Y = 50 # Number of px from top of the screen

# INITIALIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# FUNCTIONS
def updateMainBoard(board):
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

def updateSmallBoard(small_board):
    # Update board
    for row in range(SMALLBOARD_HEIGHT):
        for col in range(SMALLBOARD_WIDTH):
            if small_board[row][col] == 0:
                SCREEN.blit(EMPTY_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 1:
                SCREEN.blit(GREEN_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 2:
                SCREEN.blit(INDIGO_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 3:
                SCREEN.blit(ORANGE_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 4:
                SCREEN.blit(PINK_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 5:
                SCREEN.blit(RED_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 6:
                SCREEN.blit(YELLOW_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))
            elif small_board[row][col] == 7:
                SCREEN.blit(BLUE_CELL, (SMALLBOARD_X + col*BOARD_CELL, SMALLBOARD_Y + row*BOARD_CELL))

    pygame.display.update()

