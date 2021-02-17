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
TILE_SIZE = 150
HEADING1_SIZE = 100
TEXT_SIZE = 50

TILE_HEIGHT = 100
HEADING1_HEIGHT = 50
TEXT_HEIGHT = 25

TITLE_FONT = CHATHURA_XBOLD
HEADING_FONT = CHATHURA_RG
TEXT_FONT = CHATHURA_RG
BOLD_FONT = CHATHURA_BOLD

# Buttons
BTN_HEIGHT = 60
BTN_WIDTH = 150
BTN_CORNER_RAD = 11

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

TROPHIES_BTN_X = PADDING
TROPHIES_BTN_Y = STATS_BTN_Y + BTN_HEIGHT + NEAR

QUIT_BTN_X = PADDING
QUIT_BTN_Y = TROPHIES_BTN_Y + BTN_HEIGHT + 2 * FAR

INSTRUCTION_X = START_BTN_X + BTN_WIDTH + 2 * FAR
INSTRUCTION_Y = LOGO_Y + LOGO_HEIGHT + 2 * FAR

# Score
SCORE_TEXT_X = PADDING
SCORE_TEXT_Y = PADDING

SCORE_VAL_X = SCORE_TEXT_X + 70
SCORE_VAL_Y = SCORE_TEXT_Y

HIGH_SCORE_TEXT_X = SCORE_TEXT_X
HIGH_SCORE_TEXT_Y = SCORE_TEXT_Y + TEXT_HEIGHT + NEAR

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
BOARD_Y = HIGH_SCORE_VAL_Y + TEXT_HEIGHT + FAR

# Next block area
NEXT_BLOCK_TEXT_X = BOARD_X + BOARD_WIDTH * BOARD_CELL + PADDING
NEXT_BLOCK_TEXT_Y = BOARD_Y - (HEADING1_HEIGHT + NEAR)

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
GAME_OVER_TEXT_X = (SCREEN_WIDTH - 350) / 2
GAME_OVER_TEXT_Y = (SCREEN_HEIGHT - HEADING1_HEIGHT) / 2
NEW_GAME_BTN_X = PAUSE_BTN_X
NEW_GAME_BTN_Y = PAUSE_BTN_Y

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


# FUNCTIONS
# General
def drawText(text, x, y, size=TEXT_SIZE, color=WHITE, font=TEXT_FONT):
    font.render_to(SCREEN, (x, y), text, color, size=size)


def drawButton(button, x, y):
    SCREEN.blit(button, (x, y))


def checkButtonPress(mouse_pos, button_pos):
    mouse_x, mouse_y = mouse_pos
    button_x, button_y = button_pos

    height_box = pygame.Rect(button_x + BTN_CORNER_RAD, button_y, BTN_WIDTH - BTN_CORNER_RAD * 2,
                             BTN_HEIGHT)  # Rect with correct height, without left and right edge
    width_box = pygame.Rect(button_x, button_y + BTN_CORNER_RAD, BTN_WIDTH,
                            BTN_HEIGHT - BTN_CORNER_RAD * 2)  # Rect with correct width, without top and bottom

    top_left_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_CORNER_RAD, button_y + BTN_CORNER_RAD)
    top_right_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_WIDTH - BTN_CORNER_RAD,
                                         button_y + BTN_CORNER_RAD)
    bottom_left_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_CORNER_RAD,
                                           button_y + BTN_HEIGHT - BTN_CORNER_RAD)
    bottom_right_corner = checkButtonCorner(mouse_x, mouse_y, button_x + BTN_WIDTH - BTN_CORNER_RAD,
                                            button_y + BTN_HEIGHT - BTN_CORNER_RAD)

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
            elif board[row][col] == 8:
                SCREEN.blit(SHADOW_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))


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

    drawText("Next", NEXT_BLOCK_TEXT_X, NEXT_BLOCK_TEXT_Y, size=HEADING1_SIZE)


def updateScore(score, high_score, stage):
    # Display current score
    drawText("Score", SCORE_TEXT_X, SCORE_TEXT_Y, color=NEON_BLUE, font=BOLD_FONT)
    drawText(str(score), SCORE_VAL_X, SCORE_VAL_Y)

    # Display high score
    drawText("High", HIGH_SCORE_TEXT_X, HIGH_SCORE_TEXT_Y, color=LIGHT_ORANGE, font=BOLD_FONT)
    drawText(str(high_score), HIGH_SCORE_VAL_X, HIGH_SCORE_VAL_Y)

    # Display stage
    drawText("Stage", STAGE_TEXT_X, STAGE_TEXT_Y, color=NEON_GREEN, font=BOLD_FONT)
    drawText(str(stage), STAGE_VAL_X, STAGE_VAL_Y)


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
    drawText("Game Over", GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y, size=TILE_SIZE, font=TITLE_FONT)

    # Buttons
    drawButton(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawButton(END_BTN, END_BTN_X, END_BTN_Y)


def updateMainMenu():
    SCREEN.blit(LOGO, (LOGO_X, LOGO_Y))

    drawButton(START_BTN, START_BTN_X, START_BTN_Y)
    drawButton(OPTIONS_BTN, OPTIONS_BTN_X, OPTIONS_BTN_Y)
    drawButton(STATS_BTN, STATS_BTN_X, STATS_BTN_Y)
    drawButton(TROPHIES_BTN, TROPHIES_BTN_X, TROPHIES_BTN_Y)
    drawButton(QUIT_BTN, QUIT_BTN_X, QUIT_BTN_Y)

    SCREEN.blit(INSTRUCTION_IMAGE, (INSTRUCTION_X, INSTRUCTION_Y))
