import pygame
import pygame.freetype
import math
import datetime
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
NEAR = 15
FAR = 30

# Text

TITLE_SIZE = 120
HEADING1_SIZE = 100
HEADING2_SIZE = 80
TEXT_SIZE = 50

HEIGHT_SIZE_RATIO = 0.417

TITLE_HEIGHT = round(TITLE_SIZE * HEIGHT_SIZE_RATIO)  # 50
HEADING1_HEIGHT = round(HEADING1_SIZE * HEIGHT_SIZE_RATIO)  # 42
HEADING2_HEIGHT = round(HEADING2_SIZE * HEIGHT_SIZE_RATIO)  # 33
TEXT_HEIGHT = round(TEXT_SIZE * HEIGHT_SIZE_RATIO)  # 21


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
BOARD_SCREEN_WIDTH = BOARD_WIDTH * BOARD_CELL
BOARD_SCREEN_HEIGHT = BOARD_HEIGHT * BOARD_CELL

BOARD_X = PADDING
BOARD_Y = HIGH_SCORE_VAL_Y + TEXT_HEIGHT + FAR

BOARD_X_END = BOARD_X + BOARD_SCREEN_WIDTH
BOARD_Y_END = BOARD_Y + BOARD_SCREEN_HEIGHT

# Next block area
NEXT_BLOCK_TEXT_X = BOARD_X_END + PADDING
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

# Powers
POWERS_HEADING_X = NEXT_BLOCK_TEXT_X
POWERS_HEADING_Y = NEXT_BLOCK_AREA_Y + NEXT_BLOCK_AREA_HEIGHT * BOARD_CELL + FAR

ACTIVATE_POWER_BTN_X = POWERS_HEADING_X
ACTIVATE_POWER_BTN_Y = POWERS_HEADING_Y + HEADING1_HEIGHT + NEAR

CANCEL_POWER_BTN_X = END_BTN_X
CANCEL_POWER_BTN_Y = END_BTN_Y

POWER_HELP_TXT_X = PADDING
POWER_HELP_TXT_Y = BOARD_Y - TEXT_HEIGHT - NEAR

BLOCK_IMAGE_AREA = 75
BLOCK_SELECTION_X = BOARD_X_END + (SCREEN_WIDTH - BOARD_X_END - BLOCK_IMAGE_AREA) / 2
BLOCK_SELECTION_Y = PADDING
BLOCK_IMAGE_SPACING = BLOCK_IMAGE_AREA + NEAR

# Countdown
COUNTDOWN_X = BOARD_X + (BOARD_SCREEN_WIDTH - 10) / 2
COUNTDOWN_Y = BOARD_Y + (BOARD_SCREEN_HEIGHT - TITLE_HEIGHT) / 2

# Game over screen

GAME_OVER_TEXT_X = BOARD_X + (BOARD_SCREEN_WIDTH - 280) / 2
GAME_OVER_TEXT_Y = BOARD_Y + (BOARD_SCREEN_HEIGHT - TITLE_HEIGHT) / 2

NEW_GAME_BTN_X = PAUSE_BTN_X
NEW_GAME_BTN_Y = PAUSE_BTN_Y

# Options menu
BACK_BTN_X = PADDING
BACK_BTN_Y = PADDING

OPTIONS_TEXT_X = PADDING
OPTIONS_TEXT_Y = PADDING + BTN_HEIGHT + FAR

SOUND_TEXT_X = PADDING
SOUND_TEXT_Y = OPTIONS_TEXT_Y + TITLE_HEIGHT + 2 * FAR
SOUND_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
SOUND_SWITCH_Y = SOUND_TEXT_Y - 18

STAGES_TEXT_X = PADDING
STAGES_TEXT_Y = SOUND_TEXT_Y + HEADING1_HEIGHT + FAR
STAGES_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
STAGES_SWITCH_Y = STAGES_TEXT_Y - 18

BLOCK_SHADOW_TEXT_X = PADDING
BLOCK_SHADOW_TEXT_Y = STAGES_TEXT_Y + HEADING1_HEIGHT + FAR
BLOCK_SHADOW_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
BLOCK_SHADOW_SWITCH_Y = BLOCK_SHADOW_TEXT_Y - 18

POWER_UPS_TEXT_X = PADDING
POWER_UPS_TEXT_Y = BLOCK_SHADOW_TEXT_Y + HEADING1_HEIGHT + FAR
POWER_UPS_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
POWER_UPS_SWITCH_Y = POWER_UPS_TEXT_Y - 18

# Stats menu
PREVIOUS_BTN_X = PADDING
PREVIOUS_BTN_Y = SCREEN_HEIGHT - BTN_HEIGHT - PADDING
NEXT_BTN_X = SCREEN_WIDTH - BTN_WIDTH - PADDING
NEXT_BTN_Y = PREVIOUS_BTN_Y
PAGE_TXT_X = (PREVIOUS_BTN_X + NEXT_BTN_X) / 2 + NEAR
PAGE_TXT_Y = SCREEN_HEIGHT - BTN_HEIGHT - PADDING + 13

STAT_TEXT_X = PADDING
STAT_VAL_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH

STAT_1_Y = OPTIONS_TEXT_Y + TITLE_HEIGHT + 2 * FAR
STAT_Y = [STAT_1_Y + i * (HEADING1_HEIGHT + NEAR) for i in range(6)]  # Create a list of Y values [stat1_Y, stat2_Y, ...]

STATS_VALUES = [[["Highscore(Classic):", str(getStat("high_score"))],
                ["Highscore(Pwr-Up):", str(getStat("high_score_powers"))],
                ["Best stage:", str(getStat("highest_stage"))],
                ["Time in-game:", str(datetime.timedelta(seconds=getStat("time_ingame")))],
                ["Total games:", str(getStat("games_played"))],
                ["Blocks generated:", str(getStat("blocks_created"))]],            
                
                [["Rows cleared:", str(getStat("rows"))],
                ["Single rows:", str(getStat("rows_1"))],
                ["Double rows:", str(getStat("rows_2"))],
                ["Triple rows:", str(getStat("rows_3"))],
                ["Quadruple rows:", str(getStat("rows_4"))],
                ["Hard drops:", str(getStat("hard_drops"))]]]

# Trophies
PREVIOUS_BTN_X = PADDING
PREVIOUS_BTN_Y = SCREEN_HEIGHT - PADDING - BTN_HEIGHT
NEXT_BTN_X = SCREEN_WIDTH - PADDING - BTN_WIDTH
NEXT_BTN_Y = SCREEN_HEIGHT - PADDING - BTN_HEIGHT

PAGE_TEXT_X = PADDING + BTN_WIDTH + 20
PAGE_TEXT_Y = SCREEN_HEIGHT - PADDING - BTN_HEIGHT + 13

TROPHIES_TEXT_X = PADDING
TROPHIES_TEXT_Y = PADDING + BTN_HEIGHT + FAR

TROPHY1_HEADING_X = PADDING
TROPHY1_HEADING_Y = TROPHIES_TEXT_Y + TITLE_HEIGHT + 2 * FAR
TROPHY1_TEXT_X = TROPHY1_HEADING_X
TROPHY1_TEXT_Y = TROPHY1_HEADING_Y + HEADING2_HEIGHT + NEAR

TROPHY2_HEADING_X = PADDING
TROPHY2_HEADING_Y = TROPHY1_TEXT_Y + TEXT_HEIGHT + FAR
TROPHY2_TEXT_X = TROPHY2_HEADING_X
TROPHY2_TEXT_Y = TROPHY2_HEADING_Y + HEADING2_HEIGHT + NEAR

TROPHY3_HEADING_X = PADDING
TROPHY3_HEADING_Y = TROPHY2_TEXT_Y + TEXT_HEIGHT + FAR
TROPHY3_TEXT_X = TROPHY3_HEADING_X
TROPHY3_TEXT_Y = TROPHY3_HEADING_Y + HEADING2_HEIGHT + NEAR

TROPHY_PAGES = [["Legend", "Reach 500,000 points",
              "Master", "Reach 100,000 points",
              "Advanced", "Reach 50,000 points"],

              ["Novice", "Reach 10,000 points",
               "Tetris", "Quadruple row clear",
               "Clearer", "Clear 500 rows"]]

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


# GENERAL FUNCTIONS
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


def drawTransparentOverlay():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(TRANSPARENT_BLACK)  # Last number represents opacitiy [0 = no opacity]
    SCREEN.blit(overlay, (0, 0))


# GAME
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
    if optionsValues("stages"):
        drawText("Stage", STAGE_TEXT_X, STAGE_TEXT_Y, color=NEON_GREEN, font=BOLD_FONT)
        drawText(str(stage), STAGE_VAL_X, STAGE_VAL_Y)


def updateGameButtons():
    drawObject(PAUSE_BTN, PAUSE_BTN_X, PAUSE_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def updatePauseMenu():
    # Background
    drawTransparentOverlay()

    # Buttons
    drawObject(RESUME_BTN, RESUME_BTN_X, RESUME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def updateGameOverScreen():
    drawTransparentOverlay()

    # Message
    drawText("Game Over", GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)

    # Buttons
    drawObject(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def showCountdownToResumeGame(countdown):
    drawTransparentOverlay()
    drawText(str(countdown), COUNTDOWN_X, COUNTDOWN_Y, size=TITLE_SIZE, font=TITLE_FONT)

    pygame.display.update()  # Without it, countdown is shown with delay
    pygame.time.delay(1000)  # Show current count for a second


# MAIN MENU
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
    drawText("Sound:", SOUND_TEXT_X, SOUND_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Stages:", STAGES_TEXT_X, STAGES_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Block shadows:", BLOCK_SHADOW_TEXT_X, BLOCK_SHADOW_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Power ups:", POWER_UPS_TEXT_X, POWER_UPS_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)

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

def updateStatsMenu(page):
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)
    drawText("Stats", OPTIONS_TEXT_X, OPTIONS_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)
    drawText("Page " + str(page), PAGE_TXT_X, PAGE_TXT_Y, size=HEADING2_SIZE, font=TITLE_FONT)
    
    if(page==1):  # If first page, prev button blacknwhite, next colored
        drawObject(PREVIOUS_BTN_BW, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)
    elif(page==2):  # If last page, prev button colored, next blacknwhite
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN_BW, NEXT_BTN_X, NEXT_BTN_Y)
    else:  # Prev and next button colored
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)
    
    for i in range(len(STATS_VALUES[page-1])):
        drawText(STATS_VALUES[page-1][i][0], STAT_TEXT_X, STAT_Y[i], size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(STATS_VALUES[page-1][i][1], STAT_VAL_X, STAT_Y[i], size=HEADING2_SIZE, font=HEADING_FONT)
    
    
    """
    if(page==1):
        drawText(STATS_VALUES[page-1][0][0], STAT_TEXT_X, STAT_1_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(STATS_VALUES[page-1][0][1], STAT_VAL_X, STAT_1_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Highscore(Pwr-Up):", STAT_TEXT_X, STAT_2_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("high_score_powers")), STAT_VAL_X, STAT_2_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Best stage:", STAT_TEXT_X, STAT_3_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("highest_stage")), STAT_VAL_X, STAT_3_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Time in-game:", STAT_TEXT_X, STAT_4_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(datetime.timedelta(seconds=getStat("time_ingame"))), STAT_VAL_X, STAT_4_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Total games:", STAT_TEXT_X, STAT_5_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("games_played")), STAT_VAL_X, STAT_5_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Blocks generated:", STAT_TEXT_X, STAT_6_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("blocks_created")), STAT_VAL_X, STAT_6_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    if(page==2):
        drawText("Rows cleared:", STAT_TEXT_X, STAT_1_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("rows")), STAT_VAL_X, STAT_1_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Single rows:", STAT_TEXT_X, STAT_2_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("rows_1")), STAT_VAL_X, STAT_2_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Double rows:", STAT_TEXT_X, STAT_3_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("rows_2")), STAT_VAL_X, STAT_3_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Triple rows:", STAT_TEXT_X, STAT_4_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("rows_3")), STAT_VAL_X, STAT_4_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Quadruple rows:", STAT_TEXT_X, STAT_5_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("rows_4")), STAT_VAL_X, STAT_5_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText("Hard drops:", STAT_TEXT_X, STAT_6_Y, size=HEADING2_SIZE, font=HEADING_FONT)
        drawText(str(getStat("hard_drops")), STAT_VAL_X, STAT_6_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    """
    
def updateTrophiesScreen(page_nr):
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)
    if page_nr != 1:
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    if page_nr != 2:
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)
    drawText("Page "+str(page_nr)+"/2", PAGE_TEXT_X, PAGE_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Trophies", TROPHIES_TEXT_X, TROPHIES_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)

    drawText(TROPHY_PAGES[page_nr-1][0], TROPHY1_HEADING_X, TROPHY1_HEADING_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText(TROPHY_PAGES[page_nr-1][1], TROPHY1_TEXT_X, TROPHY1_TEXT_Y, size=TEXT_SIZE, font=TEXT_FONT)
    drawText(TROPHY_PAGES[page_nr-1][2], TROPHY2_HEADING_X, TROPHY2_HEADING_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText(TROPHY_PAGES[page_nr-1][3], TROPHY2_TEXT_X, TROPHY2_TEXT_Y, size=TEXT_SIZE, font=TEXT_FONT)
    drawText(TROPHY_PAGES[page_nr-1][4], TROPHY3_HEADING_X, TROPHY3_HEADING_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText(TROPHY_PAGES[page_nr-1][5], TROPHY3_TEXT_X, TROPHY3_TEXT_Y, size=TEXT_SIZE, font=TEXT_FONT)

# POWERS
def updatePowersSelection(power):
    drawText("Power", POWERS_HEADING_X, POWERS_HEADING_Y, size=HEADING1_SIZE, font=HEADING_FONT)

    if power.is_available:
        if power.name == "Laser":
            button = LASER_BTN
        elif power.name == "Wishlist":
            button = WISHLIST_BTN

        drawObject(button, ACTIVATE_POWER_BTN_X, ACTIVATE_POWER_BTN_Y)
    else:
        drawText("Not available", ACTIVATE_POWER_BTN_X, ACTIVATE_POWER_BTN_Y, size=TEXT_SIZE, font=HEADING_FONT,
                 color=LIGHT_GREY)


def showPowerHelpText(text):
    drawText(text, POWER_HELP_TXT_X, POWER_HELP_TXT_Y)


def highlightBoard():
    # Create pieces of screen covers
    top_side = pygame.Surface((SCREEN_WIDTH, BOARD_Y), pygame.SRCALPHA)
    left_side = pygame.Surface((BOARD_X, SCREEN_HEIGHT), pygame.SRCALPHA)
    right_side = pygame.Surface((SCREEN_WIDTH - BOARD_X_END, SCREEN_HEIGHT), pygame.SRCALPHA)
    bottom_side = pygame.Surface((BOARD_SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_Y_END), pygame.SRCALPHA)

    # Make every piece transparent
    top_side.fill(DARK_GREY)
    left_side.fill(DARK_GREY)
    right_side.fill(DARK_GREY)
    bottom_side.fill(DARK_GREY)

    # Place pieces on right positions
    SCREEN.blit(top_side, (0, 0))
    SCREEN.blit(left_side, (0, BOARD_Y))
    SCREEN.blit(right_side, (BOARD_X_END, BOARD_Y))
    SCREEN.blit(bottom_side, (BOARD_X, BOARD_Y_END))


# Wishlist
def wishlistScreen(block_under_cursor):
    highlightBoard()
    showPowerHelpText("Click on a block to use it")
    displayBlocksSelection()
    highlightBlockUnderCursor(block_under_cursor)


def displayBlocksSelection():
    for i, block in enumerate(BLOCK_IMAGES):
        SCREEN.blit(block, (BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * i))


def highlightBlockUnderCursor(block_under_cursor):
    if block_under_cursor is not None:
        index, block_area = block_under_cursor  # Unpack tuple

        SCREEN.blit(BLOCK_IMAGES_HL[index], (BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * index))


# Laser
def laserScreen(row):
    highlightBoard()
    highlightRow(row)
    showPowerHelpText("Click on a row to remove it")


def highlightRow(row):
    if row is not None:
        index, row_y = row  # Unpack tuple

        highlight = pygame.Surface((BOARD_SCREEN_WIDTH, BOARD_CELL), pygame.SRCALPHA)
        highlight.fill(TRANSPARENT_WHITE)
        SCREEN.blit(highlight, (BOARD_X, row_y))
