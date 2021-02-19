import pygame
import pygame.freetype
import math
from board import *
from nextblock import *
from assets import *
from database import *

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
TITLE_SIZE = 150
HEADING_SIZE = 100
TEXT_SIZE = 50

TITLE_HEIGHT = 100
HEADING_HEIGHT = 50
TEXT_HEIGHT = 25

TITLE_FONT = CHATHURA_XBOLD
HEADING_FONT = CHATHURA_RG
TEXT_FONT = CHATHURA_RG
BOLD_FONT = CHATHURA_BOLD

# Buttons
BTN_HEIGHT = 60
BTN_WIDTH = 150
BTN_CORNER_RAD = 11

# Switches
SWITCH_HEIGHT = BTN_HEIGHT
SWITCH_WIDTH = BTN_WIDTH
SWITCH_CORNER_RAD = 19

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
NEXT_BLOCK_TEXT_Y = BOARD_Y - (HEADING_HEIGHT + NEAR)

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
GAME_OVER_TEXT_Y = (SCREEN_HEIGHT - HEADING_HEIGHT) / 2
NEW_GAME_BTN_X = PAUSE_BTN_X
NEW_GAME_BTN_Y = PAUSE_BTN_Y

# Options menu
BACK_BTN_X = PADDING
BACK_BTN_Y = PADDING

OPTIONS_TEXT_X = PADDING
OPTIONS_TEXT_Y = PADDING + BTN_HEIGHT + FAR

SOUND_TEXT_X = PADDING
SOUND_TEXT_Y = OPTIONS_TEXT_Y + TITLE_HEIGHT + FAR
SOUND_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
SOUND_SWITCH_Y = SOUND_TEXT_Y - 10

STAGES_TEXT_X = PADDING
STAGES_TEXT_Y = SOUND_TEXT_Y + HEADING_HEIGHT + FAR
STAGES_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
STAGES_SWITCH_Y = STAGES_TEXT_Y - 10

BLOCK_SHADOW_TEXT_X = PADDING
BLOCK_SHADOW_TEXT_Y = STAGES_TEXT_Y + HEADING_HEIGHT + FAR
BLOCK_SHADOW_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
BLOCK_SHADOW_SWITCH_Y = BLOCK_SHADOW_TEXT_Y - 10

POWER_UPS_TEXT_X = PADDING
POWER_UPS_TEXT_Y = BLOCK_SHADOW_TEXT_Y + HEADING_HEIGHT + FAR
POWER_UPS_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
POWER_UPS_SWITCH_Y = POWER_UPS_TEXT_Y - 10

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


# FUNCTIONS
# General
def drawText(text, x, y, size=TEXT_SIZE, color=WHITE, font=TEXT_FONT):
    font.render_to(SCREEN, (x, y), text, color, size=size)

def drawObject(object, x, y):
    SCREEN.blit(object, (x, y))

def clickBox(mouse_pos, button_pos, radius):
    mouse_x, mouse_y = mouse_pos
    button_x, button_y = button_pos
    # Two rects that cover everything but rounded corners
    height_box = pygame.Rect(button_x + radius, button_y, BTN_WIDTH - radius * 2, BTN_HEIGHT)
    width_box = pygame.Rect(button_x, button_y + radius, BTN_WIDTH, BTN_HEIGHT - radius * 2)

    top_left_corner = checkCornerRad(mouse_x, mouse_y, button_x + radius, button_y + radius, radius)
    top_right_corner = checkCornerRad(mouse_x, mouse_y, button_x + BTN_WIDTH - radius, button_y + radius, radius)
    bottom_left_corner = checkCornerRad(mouse_x, mouse_y, button_x + radius,button_y + BTN_HEIGHT - radius, radius)
    bottom_right_corner = checkCornerRad(mouse_x, mouse_y, button_x + BTN_WIDTH - radius,
                                            button_y + BTN_HEIGHT - radius, radius)

    if height_box.collidepoint(mouse_pos) or width_box.collidepoint(mouse_pos):
        return True
    elif top_left_corner or top_right_corner or bottom_left_corner or bottom_right_corner:
        return True


def checkCornerRad(mouse_x, mouse_y, button_x, button_y, radius):  # Checks if mouse is inside rounded corner
    xsq = math.pow(mouse_x - button_x, 2)
    ysq = math.pow(mouse_y - button_y, 2)
    if math.sqrt(xsq + ysq) < radius-1:
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

    drawText("Next", NEXT_BLOCK_TEXT_X, NEXT_BLOCK_TEXT_Y, size=HEADING_SIZE)


def updateScore(score, high_score, stage):
    # Display current score
    drawText("Score", SCORE_TEXT_X, SCORE_TEXT_Y, color=NEON_BLUE, font=BOLD_FONT)
    drawText(str(score), SCORE_VAL_X, SCORE_VAL_Y)

    # Display high score
    drawText("High", HIGH_SCORE_TEXT_X, HIGH_SCORE_TEXT_Y, color=LIGHT_ORANGE, font=BOLD_FONT)
    drawText(str(high_score), HIGH_SCORE_VAL_X, HIGH_SCORE_VAL_Y)

    # Display stage
    if optionsValues("stages"):
        drawText("Stage", STAGE_TEXT_X, STAGE_TEXT_Y, color=NEON_GREEN, font=BOLD_FONT)
        drawText(str(stage), STAGE_VAL_X, STAGE_VAL_Y)


def updateGameButtons():
    drawObject(PAUSE_BTN, PAUSE_BTN_X, PAUSE_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def updatePauseMenu():
    # Background
    transparent_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 200))  # Last number represents opacitiy [0 = no opacity]
    SCREEN.blit(transparent_bg, (0, 0))

    # Buttons
    drawObject(RESUME_BTN, RESUME_BTN_X, RESUME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def updateGameOverScreen():
    # Background
    transparent_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 200))  # Last number represents opacitiy [0 = no opacity]
    SCREEN.blit(transparent_bg, (0, 0))

    # Message
    drawText("Game Over", GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)

    # Buttons
    drawObject(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def updateMainMenu():
    SCREEN.blit(LOGO, (LOGO_X, LOGO_Y))

    drawObject(START_BTN, START_BTN_X, START_BTN_Y)
    drawObject(OPTIONS_BTN, OPTIONS_BTN_X, OPTIONS_BTN_Y)
    drawObject(STATS_BTN, STATS_BTN_X, STATS_BTN_Y)
    drawObject(TROPHIES_BTN, TROPHIES_BTN_X, TROPHIES_BTN_Y)
    drawObject(QUIT_BTN, QUIT_BTN_X, QUIT_BTN_Y)

    SCREEN.blit(INSTRUCTION_IMAGE, (INSTRUCTION_X, INSTRUCTION_Y))

def updateOptionsMenu():
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)

    drawText("Options", OPTIONS_TEXT_X, OPTIONS_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)
    drawText("Sound:", SOUND_TEXT_X, SOUND_TEXT_Y, size=HEADING_SIZE, font=HEADING_FONT)
    drawText("Stages:", STAGES_TEXT_X, STAGES_TEXT_Y, size=HEADING_SIZE, font=HEADING_FONT)
    drawText("Block shadows:", BLOCK_SHADOW_TEXT_X, BLOCK_SHADOW_TEXT_Y, size=HEADING_SIZE, font=HEADING_FONT)
    drawText("Power ups:", POWER_UPS_TEXT_X, POWER_UPS_TEXT_Y, size=HEADING_SIZE, font=HEADING_FONT)

    if optionsValues("sound"):
        drawObject(ON_SWITCH, SOUND_SWITCH_X, SOUND_SWITCH_Y)
    elif not optionsValues("sound"):
        drawObject(OFF_SWITCH, SOUND_SWITCH_X, SOUND_SWITCH_Y)
    if optionsValues("stages"):
        drawObject(ON_SWITCH, STAGES_SWITCH_X, STAGES_SWITCH_Y)
    elif not optionsValues("stages"):
        drawObject(OFF_SWITCH, STAGES_SWITCH_X, STAGES_SWITCH_Y)
    if optionsValues("block_shadows"):
        drawObject(ON_SWITCH, BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    elif not optionsValues("block_shadows"):
        drawObject(OFF_SWITCH, BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    if optionsValues("power_ups"):
        drawObject(ON_SWITCH, POWER_UPS_SWITCH_X, POWER_UPS_SWITCH_Y)
    elif not optionsValues("power_ups"):
        drawObject(OFF_SWITCH, POWER_UPS_SWITCH_X, POWER_UPS_SWITCH_Y)

