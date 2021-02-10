import pygame
import pygame.freetype
from board import *
from nextblock import *
from assets import *

# CONSTANTS
# Screen
SCREEN_WIDTH = 600  # px
SCREEN_HEIGHT = 700  # px
FPS = 60

# Whitespace
PADDING = 50
NEAR = 10
FAR = 30

# Text
TXT_HEIGHT = 50

# Board
BOARD_CELL = 30  # 30 px square
BOARD_X = PADDING
BOARD_Y = PADDING

# Next block area
NEXT_BLOCK_AREA_X = BOARD_X + BOARD_WIDTH * BOARD_CELL + PADDING
NEXT_BLOCK_TEXT_AREA_Y = PADDING
NEXT_BLOCK_AREA_Y = NEXT_BLOCK_TEXT_AREA_Y + TXT_HEIGHT + NEAR

# Score
SCORE_AREA_X = NEXT_BLOCK_AREA_X
SCORE_AREA_Y = NEXT_BLOCK_AREA_Y + NEXT_BLOCK_AREA_HEIGHT * BOARD_CELL + FAR

# In-game buttons
BTN_HEIGHT = 68
GAME_BTNS_ARENA_X = NEXT_BLOCK_AREA_X
GAME_BTNS_ARENA_Y = SCREEN_HEIGHT - PADDING - 2 * BTN_HEIGHT - NEAR

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


# FUNCTIONS
# General
def drawText(text, x, y, size=100, color=WHITE, font=CHATHURA_RG):
    font.render_to(SCREEN, (x, y), text, color, size=size)


def drawButton(button, x, y):
    SCREEN.blit(button, (x, y))


# Game UI
def updateBoard(board):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                SCREEN.blit(EMPTY_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 1:
                SCREEN.blit(GREEN_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 2:
                SCREEN.blit(BRONZE_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 3:
                SCREEN.blit(PURPLE_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 4:
                SCREEN.blit(PINK_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 5:
                SCREEN.blit(RED_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 6:
                SCREEN.blit(YELLOW_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 7:
                SCREEN.blit(BLUE_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))


def updateNextBlockArea(next_block_area):
    for row in range(NEXT_BLOCK_AREA_HEIGHT):
        for col in range(NEXT_BLOCK_AREA_WIDTH):
            if next_block_area[row][col] == 0:
                SCREEN.blit(EMPTY_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 1:
                SCREEN.blit(GREEN_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 2:
                SCREEN.blit(BRONZE_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 3:
                SCREEN.blit(PURPLE_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 4:
                SCREEN.blit(PINK_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 5:
                SCREEN.blit(RED_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 6:
                SCREEN.blit(YELLOW_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))
            elif next_block_area[row][col] == 7:
                SCREEN.blit(BLUE_CELL, (NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL))

    drawText("Next", NEXT_BLOCK_AREA_X, NEXT_BLOCK_TEXT_AREA_Y)


def updateScore(score):
    drawText("Score", SCORE_AREA_X, SCORE_AREA_Y)
    drawText(str(score), SCORE_AREA_X, SCORE_AREA_Y + TXT_HEIGHT + NEAR, color=NEON_BLUE)


def updateGameButtons():
    drawButton(PAUSE_BTN, GAME_BTNS_ARENA_X, GAME_BTNS_ARENA_Y)
    drawButton(END_BTN, GAME_BTNS_ARENA_X, GAME_BTNS_ARENA_Y + BTN_HEIGHT + NEAR)


def updatePauseMenu():
    # Background
    transparent_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 175))  # 150 represents opacitiy [0 = no opacity]
    SCREEN.blit(transparent_bg, (0, 0))

    # Game buttons
    drawButton(RESUME_BTN, GAME_BTNS_ARENA_X, GAME_BTNS_ARENA_Y)
    drawButton(END_BTN, GAME_BTNS_ARENA_X, GAME_BTNS_ARENA_Y + BTN_HEIGHT + NEAR)
