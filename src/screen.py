import pygame
import pygame.freetype
import math
import time
import datetime
from board import *
from nextblock import *
from assets import *
from database import *

# CONSTANTS
# Screen
# Screen width, height and screen itself are initialized in assets.py for image loading!
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
BTN_CORNER_RAD = 10

# Switches
SWITCH_HEIGHT = 40
SWITCH_WIDTH = 100
SWITCH_CORNER_RAD = round(40 / (
        250 / SWITCH_WIDTH))  # In .ai file, switch is 250 px wide and it's border radius is 40. If the switch is scaled down, makes sure that corner radius is also in right propotion

# Slider backround
SLIDER_BG_HEIGHT = 30
SLIDER_BG_WIDTH = 200

# Dragger
DRAGGER_HEIGHT = 54
DRAGGER_WIDTH = 33
DRAGGER_CORNER_RAD = 5
SLIDING_DISTANCE = SLIDER_BG_WIDTH - DRAGGER_WIDTH - 8

# Main menu
LOGO_HEIGHT = 100
LOGO_WIDTH = 420
LOGO_X = (SCREEN_WIDTH - LOGO_WIDTH) / 2
LOGO_Y = PADDING

START_BTN_X = PADDING
START_BTN_Y = PADDING

CONTINUE_BTN_X = START_BTN_X
CONTINUE_BTN_Y = START_BTN_Y + BTN_HEIGHT + NEAR

OPTIONS_BTN_X = START_BTN_X
OPTIONS_BTN_Y = CONTINUE_BTN_Y + BTN_HEIGHT + NEAR

STATS_BTN_X = START_BTN_X
STATS_BTN_Y = OPTIONS_BTN_Y + BTN_HEIGHT + NEAR

TROPHIES_BTN_X = START_BTN_X
TROPHIES_BTN_Y = STATS_BTN_Y + BTN_HEIGHT + NEAR

QUIT_BTN_X = START_BTN_X
QUIT_BTN_Y = TROPHIES_BTN_Y + BTN_HEIGHT + NEAR

INSTRUCTION_X = START_BTN_X + BTN_WIDTH + 40
INSTRUCTION_Y = START_BTN_Y

CREDITS_X = PADDING
CREDITS_Y = SCREEN_HEIGHT - PADDING - TEXT_HEIGHT

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
PAUSE_BTN_Y = SCREEN_HEIGHT - PADDING - 3 * BTN_HEIGHT - 2 * NEAR

RESUME_BTN_X = PAUSE_BTN_X
RESUME_BTN_Y = PAUSE_BTN_Y

SAVE_BTN_X = PAUSE_BTN_X
SAVE_BTN_Y = PAUSE_BTN_Y + BTN_HEIGHT + NEAR

END_BTN_X = PAUSE_BTN_X
END_BTN_Y = SAVE_BTN_Y + BTN_HEIGHT + NEAR

# Save confirmation
SAVED_TXT_X = (SCREEN_WIDTH - 200) / 2
SAVED_TXT_Y = (SCREEN_HEIGHT - TITLE_HEIGHT) / 2

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

# Navigation
BACK_BTN_X = PADDING
BACK_BTN_Y = PADDING

PREVIOUS_BTN_X = PADDING
PREVIOUS_BTN_Y = SCREEN_HEIGHT - BTN_HEIGHT - PADDING
NEXT_BTN_X = SCREEN_WIDTH - BTN_WIDTH - PADDING
NEXT_BTN_Y = PREVIOUS_BTN_Y

PAGE_NR_X = (PREVIOUS_BTN_X + NEXT_BTN_X) / 2 + NEAR
PAGE_NR_Y = SCREEN_HEIGHT - BTN_HEIGHT - PADDING + 13

# Main menu page
PAGE_TITLE_X = BACK_BTN_X
PAGE_TITLE_Y = BACK_BTN_Y + BTN_HEIGHT + 2 * FAR

# Options menu
OPTIONS_TITLE_X = PAGE_TITLE_X
OPTIONS_TITLE_Y = PAGE_TITLE_Y

SOUND_TEXT_X = BACK_BTN_X
SOUND_TEXT_Y = OPTIONS_TITLE_Y + TITLE_HEIGHT + FAR
SOUND_SLIDER_BG_X = SCREEN_WIDTH - PADDING - SLIDER_BG_WIDTH
SOUND_SLIDER_BG_Y = SOUND_TEXT_Y + (HEADING2_HEIGHT - SLIDER_BG_HEIGHT) / 2
SOUND_DRAGGER_X = SOUND_SLIDER_BG_X + 4
SOUND_DRAGGER_Y = SOUND_SLIDER_BG_Y - 12
SOUND_VAL_Y = SOUND_DRAGGER_Y - 30

STAGES_TEXT_X = SOUND_TEXT_X
STAGES_TEXT_Y = SOUND_TEXT_Y + HEADING2_HEIGHT + FAR
STAGES_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
STAGES_SWITCH_Y = STAGES_TEXT_Y + (SWITCH_HEIGHT - HEADING2_HEIGHT) / 2

BLOCK_SHADOW_TEXT_X = SOUND_TEXT_X
BLOCK_SHADOW_TEXT_Y = STAGES_TEXT_Y + HEADING2_HEIGHT + FAR
BLOCK_SHADOW_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
BLOCK_SHADOW_SWITCH_Y = BLOCK_SHADOW_TEXT_Y + (SWITCH_HEIGHT - HEADING2_HEIGHT) / 2

POWERS_TEXT_X = SOUND_TEXT_X
POWERS_TEXT_Y = BLOCK_SHADOW_TEXT_Y + HEADING2_HEIGHT + FAR
POWERS_SWITCH_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH
POWERS_SWITCH_Y = POWERS_TEXT_Y + (SWITCH_HEIGHT - HEADING2_HEIGHT) / 2

# Stats menu
STATS_TITLE_X = PAGE_TITLE_X
STATS_TITLE_Y = PAGE_TITLE_Y

STAT_TEXT_X = PADDING
STAT_VAL_X = SCREEN_WIDTH - PADDING - SWITCH_WIDTH

STAT1_Y = OPTIONS_TITLE_Y + TITLE_HEIGHT + FAR
STAT_Y = [STAT1_Y + i * (TEXT_HEIGHT + FAR) for i in
          range(6)]  # Create a list of stat Y values [STAT1_Y, STAT2_Y, ...STAT6_Y]

# Trophies
TROPHIES_TITLE_X = PAGE_TITLE_X
TROPHIES_TITLE_Y = PAGE_TITLE_Y

TROPHY_HEADING_X = PADDING
TROPHY_HEADING_Y = TROPHIES_TITLE_Y + TITLE_HEIGHT + FAR
TROPHY_TEXT_X = TROPHY_HEADING_X
TROPHY_TEXT_Y = TROPHY_HEADING_Y + HEADING2_HEIGHT + NEAR

TROPHY_HEADING_GAP = HEADING2_HEIGHT + NEAR + TEXT_HEIGHT + FAR

# INITIALIZE
pygame.init()


# CLASSES
class FPSController:
    def __init__(self):
        # All time measured in ms
        self.current_time = 0
        self.prev_time = 0
        self.frame_duration = 1000 / FPS

    def keepFrameDurationCorrect(self):
        self.current_time = time.time() * 1000  # Convert seconds to ms
        elapsed_time = self.current_time - self.prev_time  # How much time has elapsed since last frame?
        needed_delay = int(self.frame_duration - elapsed_time)  # Delay length to make this frame duration match FPS

        if needed_delay > 0:
            pygame.time.delay(needed_delay)

        self.prev_time = time.time() * 1000


# GENERAL FUNCTIONS
def drawText(text, x, y, size=TEXT_SIZE, color=WHITE, font=TEXT_FONT):
    font.render_to(SCREEN, (x, y), text, color, size=size)


def drawObject(object, x, y):
    SCREEN.blit(object, (x, y))


def clickBox(el_pos=(0, 0), element=0):  # 0-Button, 1-switch, 2-slider
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Determine for which UI element this clickbox is for
    if element == 0:
        width = BTN_WIDTH
        height = BTN_HEIGHT
        corner_rad = BTN_CORNER_RAD
        el_x, el_y = el_pos  # Element position

        drawObject(CLICK_MASK, el_x, el_y)
    elif element == 1:
        width = SWITCH_WIDTH
        height = SWITCH_HEIGHT
        corner_rad = SWITCH_CORNER_RAD
        el_x, el_y = el_pos  # Element position
    elif element == 2:
        width = DRAGGER_WIDTH
        height = DRAGGER_HEIGHT
        corner_rad = DRAGGER_CORNER_RAD
        el_x = SOUND_SLIDER_BG_X + (SLIDING_DISTANCE * optionsValues("sound")) + 4
        el_y = SOUND_SLIDER_BG_Y - 12

    # Two rects that cover everything but rounded corners
    height_box = pygame.Rect(el_x + corner_rad, el_y, width - corner_rad * 2, height)
    width_box = pygame.Rect(el_x, el_y + corner_rad, width, height - corner_rad * 2)

    top_left_corner = checkCornerRad(mouse_x, mouse_y, el_x + corner_rad, el_y + corner_rad, corner_rad)
    top_right_corner = checkCornerRad(mouse_x, mouse_y, el_x + width - corner_rad, el_y + corner_rad, corner_rad)
    bottom_left_corner = checkCornerRad(mouse_x, mouse_y, el_x + corner_rad, el_y + height - corner_rad, corner_rad)
    bottom_right_corner = checkCornerRad(mouse_x, mouse_y, el_x + width - corner_rad,
                                         el_y + height - corner_rad, corner_rad)
    # Check for click
    if height_box.collidepoint(mouse_x, mouse_y) or width_box.collidepoint(mouse_x, mouse_y):
        return True
    elif top_left_corner or top_right_corner or bottom_left_corner or bottom_right_corner:
        return True


def checkCornerRad(mouse_x, mouse_y, button_x, button_y, radius):  # Checks if mouse is inside rounded corner
    xsq = math.pow(mouse_x - button_x, 2)
    ysq = math.pow(mouse_y - button_y, 2)
    if math.sqrt(xsq + ysq) < radius - 1:
        return True


def activateButtonClickState(button):
    if button is not None:
        btn_x, btn_y = button
        drawObject(CLICK_MASK, btn_x, btn_y)


def activateButtonHoverState(button):
    if button is not None:
        btn_x, btn_y = button
        drawObject(HOVER_MASK, btn_x, btn_y - 1)


def drawTransparentOverlay(opacity=200, dark=True):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    if dark:
        overlay.fill((0, 0, 0, opacity))
    else:
        overlay.fill((255, 255, 255, opacity))

    SCREEN.blit(overlay, (0, 0))


def playSound(sound):
    sound.set_volume(optionsValues("sound"))
    sound.play()


def updateScreenAndDelayNextUpdate(delay=1000):
    pygame.display.update()  # Without it, UI content wouldn't be displayed for determined time
    pygame.time.delay(delay)  # default delay is 1000 ms
    pygame.event.clear()  # Don't accept inputs during delay, because game wasn't active


# GAME
def showBoard(board):
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


def showNextBlockArea(next_block_area):
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


def showScore(score, high_score, stage):
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


def showGameButtons():
    drawObject(PAUSE_BTN, PAUSE_BTN_X, PAUSE_BTN_Y)
    drawObject(SAVE_BTN, SAVE_BTN_X, SAVE_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def showPauseMenu():
    # Background
    drawTransparentOverlay()

    # Buttons
    drawObject(RESUME_BTN, RESUME_BTN_X, RESUME_BTN_Y)
    drawObject(SAVE_BTN, SAVE_BTN_X, SAVE_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def showGameOverScreen():
    drawTransparentOverlay()

    # Message
    drawText("Game Over", GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y, size=TITLE_SIZE, font=TITLE_FONT)

    # Buttons
    drawObject(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def showCountdown(countdown):
    drawTransparentOverlay()
    drawText(str(countdown), COUNTDOWN_X, COUNTDOWN_Y, size=TITLE_SIZE, font=TITLE_FONT)
    updateScreenAndDelayNextUpdate()


def showSaveConfirmation(resume_game_if_saved):
    if not resume_game_if_saved:
        showPauseMenu()

    drawTransparentOverlay(dark=False)
    drawText("Saved", SAVED_TXT_X, SAVED_TXT_Y, size=TITLE_SIZE, font=TITLE_FONT, color=DARK_GREY)
    updateScreenAndDelayNextUpdate()


# MAIN MENU
def showMainMenu(game_is_saved):
    drawObject(START_BTN, START_BTN_X, START_BTN_Y)
    drawObject(OPTIONS_BTN, OPTIONS_BTN_X, OPTIONS_BTN_Y)
    drawObject(STATS_BTN, STATS_BTN_X, STATS_BTN_Y)
    drawObject(TROPHIES_BTN, TROPHIES_BTN_X, TROPHIES_BTN_Y)
    drawObject(QUIT_BTN, QUIT_BTN_X, QUIT_BTN_Y)
    drawObject(INSTRUCTION_IMAGE, INSTRUCTION_X, INSTRUCTION_Y)

    if game_is_saved:
        drawObject(CONTINUE_BTN, CONTINUE_BTN_X, CONTINUE_BTN_Y)
    else:
        drawObject(CONTINUE_BTN_BW, CONTINUE_BTN_X, CONTINUE_BTN_Y)

    drawText("Made by Kasper, Danel and Karl-Heinrich", CREDITS_X, CREDITS_Y)


def drawNavigation(current_page, num_of_pages):
    # Back to main menu
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)

    # Pagination
    drawText("Page " + str(current_page), PAGE_NR_X, PAGE_NR_Y, size=HEADING2_SIZE, font=TITLE_FONT)

    if (current_page == 1):
        # First page: prev button grayed out, next colored
        drawObject(PREVIOUS_BTN_BW, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)
    elif (current_page == num_of_pages):
        # Last page: prev button colored, next grayed out
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN_BW, NEXT_BTN_X, NEXT_BTN_Y)
    else:
        # Page in between: both buttons colored
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)


# Options menu
def showOptionsMenu():
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)

    drawText("Options", OPTIONS_TITLE_X, OPTIONS_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)
    drawText("Sound", SOUND_TEXT_X, SOUND_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Stages", STAGES_TEXT_X, STAGES_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Block shadows", BLOCK_SHADOW_TEXT_X, BLOCK_SHADOW_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Powers", POWERS_TEXT_X, POWERS_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)

    drawOptionsSwitches()
    drawSoundSlider()


def drawOptionsSwitches():
    if optionsValues("stages"):
        drawObject(ON_SWITCH, STAGES_SWITCH_X, STAGES_SWITCH_Y)
    elif not optionsValues("stages"):
        drawObject(OFF_SWITCH, STAGES_SWITCH_X, STAGES_SWITCH_Y)

    if optionsValues("block_shadows"):
        drawObject(ON_SWITCH, BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    elif not optionsValues("block_shadows"):
        drawObject(OFF_SWITCH, BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)

    if optionsValues("powers"):
        drawObject(ON_SWITCH, POWERS_SWITCH_X, POWERS_SWITCH_Y)
    elif not optionsValues("powers"):
        drawObject(OFF_SWITCH, POWERS_SWITCH_X, POWERS_SWITCH_Y)


def drawSoundSlider():
    dragger_x = SOUND_DRAGGER_X + (SLIDING_DISTANCE * optionsValues("sound"))
    sound_val = round(optionsValues("sound") * 100)

    # Keep the value in the middle of the dragger
    if sound_val == 100:
        drawText(str(sound_val), dragger_x - 2, SOUND_VAL_Y)
    elif sound_val > 9:
        drawText(str(sound_val), dragger_x + 3, SOUND_VAL_Y)
    else:
        drawText(str(sound_val), dragger_x + 10, SOUND_VAL_Y)

    drawObject(SLIDER_BG, SOUND_SLIDER_BG_X, SOUND_SLIDER_BG_Y)
    drawObject(DRAGGER, dragger_x, SOUND_DRAGGER_Y)


# Stats menu
def showStatsMenu(current_page):
    stats = updateStats()

    drawNavigation(current_page, num_of_pages=len(stats))
    drawText("Stats", STATS_TITLE_X, STATS_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)

    # Display stat name and value
    for i in range(len(stats[current_page - 1])):
        drawText(stats[current_page - 1][i][0], STAT_TEXT_X, STAT_Y[i])
        drawText(stats[current_page - 1][i][1], STAT_VAL_X, STAT_Y[i])


def updateStats():
    return [[["Highscore (Classic)", str(getStat("high_score"))],
             ["Highscore (Powers)", str(getStat("high_score_powers"))],
             ["Best stage", str(getStat("highest_stage"))],
             ["Time in-game", str(datetime.timedelta(seconds=getStat("time_ingame")))],
             ["Total games", str(getStat("games_played"))],
             ["Blocks generated", str(getStat("blocks_created"))]],

            [["Rows cleared", str(getStat("rows"))],
             ["Single rows", str(getStat("rows_1"))],
             ["Double rows", str(getStat("rows_2"))],
             ["Triple rows", str(getStat("rows_3"))],
             ["Quadruple rows", str(getStat("rows_4"))],
             ["Hard drops", str(getStat("hard_drops"))]],

            [["Perfect clears", str(getStat("perfect_clears"))],
             ["Single-line perfect clears", str(getStat("perfect_clears_1"))],
             ["Double-line perfect clears", str(getStat("perfect_clears_2"))],
             ["Triple-line perfect clears", str(getStat("perfect_clears_3"))],
             ["Quadruple-line perfect clears", str(getStat("perfect_clears_4"))],
             ["Number of trophies unlocked", str(getStat("trophies"))]]]


# Trophies menu
def showTrophiesScreen(current_page):
    drawNavigation(current_page, num_of_pages=len(TROPHIES))
    drawText("Trophies", TROPHIES_TITLE_X, TROPHIES_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)
    for i in range(len(TROPHIES[current_page - 1])):
        color = trophyCompletion(TROPHIES[current_page - 1][i][2], TROPHIES[current_page - 1][i][3])
        drawText(TROPHIES[current_page - 1][i][0], TROPHY_HEADING_X, TROPHY_HEADING_Y + TROPHY_HEADING_GAP * i,
                 size=HEADING2_SIZE, color=color, font=HEADING_FONT)
        drawText(TROPHIES[current_page - 1][i][1], TROPHY_TEXT_X, TROPHY_TEXT_Y + TROPHY_HEADING_GAP * i,
                 color=color)


def trophyCompletion(stat, value):
    if getStat(stat) >= value:
        return WHITE
    else:
        return GREY


# POWERS
def showPowersSelection(powers_are_enabled, power):
    drawText("Power", POWERS_HEADING_X, POWERS_HEADING_Y, size=HEADING1_SIZE, font=HEADING_FONT)

    if powers_are_enabled and power.is_available:
        if power.name == "Laser":
            button = LASER_BTN
        elif power.name == "Wishlist":
            button = WISHLIST_BTN
        elif power.name == "Timeless":
            button = TIMELESS_BTN

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
def showWishlistScreen(block_under_cursor):
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
def showLaserScreen(row):
    highlightBoard()
    highlightRow(row)
    showPowerHelpText("Click on a row to remove it")


def highlightRow(row):
    if row is not None:
        index, row_y = row  # Unpack tuple
        highlight = pygame.Surface((BOARD_SCREEN_WIDTH, BOARD_CELL), pygame.SRCALPHA)
        highlight.fill(TRANSPARENT_WHITE)
        SCREEN.blit(highlight, (BOARD_X, row_y))


# Timeless
def showTimelessScreen(num_of_blocks_left):
    if num_of_blocks_left > 1:
        phrase = "%d blocks" % num_of_blocks_left
    else:
        phrase = "block"

    highlightBoard()
    if num_of_blocks_left > 0:
        showPowerHelpText("Next %s will not fall" % phrase)
    else:
        showPowerHelpText("Next block will fall")
