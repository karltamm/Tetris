import pygame
import pygame.freetype
import math
from board import *
from nextblock import *
from assets import *

# CONSTANTS
# Screen
SCREEN_WIDTH = 600  # px
SCREEN_HEIGHT = 790  # px
FPS = 60

# Whitespace
PADDING = 50
NEAR = 10
FAR = 30

# Text
TXT_HEIGHT = 50
TXT_HEIGHT2 = 25

# Buttons
BTN_HEIGHT = 60
BTN_WIDTH = 150

# Main menu
LOGO_HEIGHT = 100
LOGO_WIDTH = 420
LOGO_X = (SCREEN_WIDTH - LOGO_WIDTH) / 2
LOGO_Y = PADDING

START_BTN_X = PADDING
START_BTN_Y = LOGO_Y + LOGO_HEIGHT + 2 * FAR

OPTIONS_BTN_X = PADDING
OPTIONS_BTN_Y = START_BTN_Y + BTN_HEIGHT + NEAR

STATS_BTN_X = PADDING
STATS_BTN_Y = OPTIONS_BTN_Y + BTN_HEIGHT + NEAR

QUIT_BTN_X = PADDING
QUIT_BTN_Y = STATS_BTN_Y + BTN_HEIGHT + 2 * FAR

INSTRUCTION_X = START_BTN_X + BTN_WIDTH + 2 * FAR
INSTRUCTION_Y = LOGO_Y + LOGO_HEIGHT + 2 * FAR

# Score
SCORE_SIZE = 50

SCORE_TEXT_X = PADDING
SCORE_TEXT_Y = PADDING

SCORE_VAL_X = SCORE_TEXT_X + 70
SCORE_VAL_Y = SCORE_TEXT_Y

HIGH_SCORE_TEXT_X = SCORE_TEXT_X
HIGH_SCORE_TEXT_Y = SCORE_TEXT_Y + TXT_HEIGHT2 + NEAR

HIGH_SCORE_VAL_X = HIGH_SCORE_TEXT_X + 70
HIGH_SCORE_VAL_Y = HIGH_SCORE_TEXT_Y

# Stage
STAGE_TEXT_X = SCORE_TEXT_X + 220
STAGE_TEXT_Y = PADDING

STAGE_VAL_X = STAGE_TEXT_X + 70
STAGE_VAL_Y = STAGE_TEXT_Y

# Board
BOARD_CELL = 30  # 30 px square

BOARD_X = PADDING
BOARD_Y = HIGH_SCORE_VAL_Y + TXT_HEIGHT2 + FAR

# Next block area
NEXT_BLOCK_TEXT_X = BOARD_X + BOARD_WIDTH * BOARD_CELL + PADDING
NEXT_BLOCK_TEXT_Y = BOARD_Y - (TXT_HEIGHT + NEAR)

NEXT_BLOCK_AREA_X = NEXT_BLOCK_TEXT_X
NEXT_BLOCK_AREA_Y = BOARD_Y

# In-game buttons
PAUSE_BTN_X = NEXT_BLOCK_TEXT_X
PAUSE_BTN_Y = SCREEN_HEIGHT - PADDING - 2 * BTN_HEIGHT - NEAR

RESUME_BTN_X = PAUSE_BTN_X
RESUME_BTN_Y = PAUSE_BTN_Y

END_BTN_X = PAUSE_BTN_X
END_BTN_Y = PAUSE_BTN_Y + BTN_HEIGHT + NEAR

# Game over screen
GAME_OVER_TEXT_X = (SCREEN_WIDTH - 235) / 2
GAME_OVER_TEXT_Y = (SCREEN_HEIGHT - TXT_HEIGHT) / 2
NEW_GAME_BTN_X = PAUSE_BTN_X
NEW_GAME_BTN_Y = PAUSE_BTN_Y

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


def checkButtonPress(mouse_pos, button_pos):
    mouse_x, mouse_y = mouse_pos
    button_x, button_y = button_pos

    height_box = pygame.Rect(button_x + 11, button_y, BTN_WIDTH - 22, BTN_HEIGHT)  # Rect with correct height, without left and right edge
    width_box = pygame.Rect(button_x, button_y + 11, BTN_WIDTH, BTN_HEIGHT - 22)  # Rect with correct width, without top and bottom

    top_left_corner = checkButtonCorner(mouse_x, mouse_y, button_x + 11, button_y + 11)
    top_right_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_WIDTH - 11, button_y + 11)
    bottom_left_corner = checkButtonCorner(mouse_x, mouse_y, button_x + 11, button_y + BTN_HEIGHT - 11)
    bottom_right_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_WIDTH - 11, button_y + BTN_HEIGHT - 11)

    if height_box.collidepoint(mouse_pos) or width_box.collidepoint(mouse_pos):
        return True
    elif top_left_corner or top_right_corner or bottom_left_corner or bottom_right_corner:
        return True


def checkButtonCorner(mouse_x, mouse_y, button_x, button_y):  # Checks if mouse is inside rounded corner
    xsq = math.pow(mouse_x - button_x, 2)
    ysq = math.pow(mouse_y - button_y, 2)
    if math.sqrt(xsq + ysq) < 10:
        return True


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

    drawText("Next", NEXT_BLOCK_TEXT_X, NEXT_BLOCK_TEXT_Y)


def updateScore(score, high_score, stage):
    # Display current score
    drawText("Score", SCORE_TEXT_X, SCORE_TEXT_Y, size=SCORE_SIZE, color=NEON_BLUE, font=CHATHURA_XBOLD)
    drawText(str(score), SCORE_VAL_X, SCORE_VAL_Y, size=SCORE_SIZE)

    # Display high score
    drawText("High", HIGH_SCORE_TEXT_X, HIGH_SCORE_TEXT_Y, size=SCORE_SIZE, color=LIGHT_ORANGE, font=CHATHURA_XBOLD)
    drawText(str(high_score), HIGH_SCORE_VAL_X, HIGH_SCORE_VAL_Y, size=SCORE_SIZE)
    
    # Display stage
    drawText("Stage", STAGE_TEXT_X, STAGE_TEXT_Y, size=SCORE_SIZE, color=LAVENDER, font=CHATHURA_XBOLD)
    drawText(str(stage), STAGE_VAL_X, STAGE_VAL_Y, size=SCORE_SIZE)


def updateGameButtons():
    drawButton(PAUSE_BTN, PAUSE_BTN_X, PAUSE_BTN_Y)
    drawButton(END_BTN, END_BTN_X, END_BTN_Y)


def updatePauseMenu():
    # Background
    transparent_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 200))  # Last number represents opacitiy [0 = no opacity]
    SCREEN.blit(transparent_bg, (0, 0))

    # Buttons
    drawButton(RESUME_BTN, RESUME_BTN_X, RESUME_BTN_Y)
    drawButton(END_BTN, END_BTN_X, END_BTN_Y)


def updateGameOverScreen():
    # Background
    transparent_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 200))  # Last number represents opacitiy [0 = no opacity]
    SCREEN.blit(transparent_bg, (0, 0))

    # Message
    drawText("Game Over", GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y, font=CHATHURA_XBOLD)

    # Buttons
    drawButton(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawButton(END_BTN, END_BTN_X, END_BTN_Y)


def updateMainMenu():
    SCREEN.blit(LOGO, (LOGO_X, LOGO_Y))

    drawButton(START_BTN, START_BTN_X, START_BTN_Y)
    drawButton(OPTIONS_BTN, OPTIONS_BTN_X, OPTIONS_BTN_Y)
    drawButton(STATS_BTN, STATS_BTN_X, STATS_BTN_Y)
    drawButton(QUIT_BTN, QUIT_BTN_X, QUIT_BTN_Y)

    SCREEN.blit(INSTRUCTION_IMAGE, (INSTRUCTION_X, INSTRUCTION_Y))
