import pygame
import pygame.freetype
import math
import time
import datetime
from board import *
from nextblock import *
from assets import *
from database import *
from themes import *

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

SWITCH_MASK_OFFSET_X = 5
SWITCH_MASK_OFFSET_Y = 4

# Slider
SLIDER_BG_HEIGHT = 30
SLIDER_BG_WIDTH = 200

DRAGGER_HEIGHT = 54
DRAGGER_WIDTH = 33
DRAGGER_CORNER_RAD = 5
SLIDING_DISTANCE = SLIDER_BG_WIDTH - DRAGGER_WIDTH - 8

SLIDER_MASK_OFFSET_X = 4
SLIDER_MASK_OFFSET_Y = 4

# Selector
SELECTOR_BTN_WIDTH = 50
SELECTOR_BTN_HEIGHT = 50
SELECTOR_BTN_CORNER_RAD = round(15 / (
        100 / SELECTOR_BTN_WIDTH))  # In .ai file, selector button is 100 px wide and it's border radius is 15. If the button is scaled down, makes sure that corner radius is also in right propotion

SELECTION_NAME_BOX_WIDTH = 125
SELECTION_NAME_BOX_HEIGHT = 50

SELECTOR_WIDTH = 2 * SELECTOR_BTN_WIDTH + 2 * NEAR + SELECTION_NAME_BOX_WIDTH

# Main menu
LOGO_HEIGHT = 100
LOGO_WIDTH = 420
LOGO_X = (SCREEN_WIDTH - LOGO_WIDTH) / 2
LOGO_Y = PADDING

START_BTN_X = PADDING
START_BTN_Y = PADDING

CONTINUE_BTN_X = START_BTN_X
CONTINUE_BTN_Y = START_BTN_Y + BTN_HEIGHT + NEAR

SHORTCUTS_BTN_X = START_BTN_X
SHORTCUTS_BTN_Y = CONTINUE_BTN_Y + BTN_HEIGHT + NEAR

OPTIONS_BTN_X = START_BTN_X
OPTIONS_BTN_Y = SHORTCUTS_BTN_Y + BTN_HEIGHT + NEAR

STATS_BTN_X = START_BTN_X
STATS_BTN_Y = OPTIONS_BTN_Y + BTN_HEIGHT + NEAR

TROPHIES_BTN_X = START_BTN_X
TROPHIES_BTN_Y = STATS_BTN_Y + BTN_HEIGHT + NEAR

THEMES_BTN_X = START_BTN_X
THEMES_BTN_Y = TROPHIES_BTN_Y + BTN_HEIGHT + NEAR

QUIT_BTN_X = START_BTN_X
QUIT_BTN_Y = THEMES_BTN_Y + BTN_HEIGHT + NEAR

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

BOARD_BG_BORDER_RADIUS_Y = BOARD_Y - 10

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

# Game over screen
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

# Shortcuts menu
GAME_SC_KEYS = (ESC_KEY_IMG, P_KEY_IMG, S_KEY_IMG, E_KEY_IMG, N_KEY_IMG)
GAME_SC_DESC = ("Pause/unpause", "Activate/deactivate power", "Save game", "End game", "New game (if game is over)")

MENU_SC_KEYS = (UP_KEY_IMG, DOWN_KEY_IMG, RIGHT_KEY_IMG, LEFT_KEY_IMG)
MENU_SC_DESC = ("Move up", "Move down", "Increase slider or show next page", "Decrease slider or show previous page")
SPACE_KEY_DESC = "Press button or move switch"

SPACE_KEY_WIDTH = 150
KEY_WIDTH = 50
KEY_HEIGHT = 54

SHORTCUTS_TITLE_X = PAGE_TITLE_X
SHORTCUTS_TITLE_Y = PAGE_TITLE_Y

SHORTCUTS_TYPE_X = SHORTCUTS_TITLE_X
SHORTCUTS_TYPE_Y = SHORTCUTS_TITLE_Y + TITLE_HEIGHT + FAR

SC_ROW_X = SHORTCUTS_TYPE_X
SC_ROW_TXT_X = SC_ROW_X + KEY_WIDTH + NEAR
SC_ROW_HEIGHT = KEY_HEIGHT + NEAR
SC_ROW1_Y = SHORTCUTS_TYPE_Y + HEADING2_HEIGHT + FAR

SPACE_KEY_DESC_X = SC_ROW_X + SPACE_KEY_WIDTH + NEAR

# Options menu
OPTIONS_TITLE_X = PAGE_TITLE_X
OPTIONS_TITLE_Y = PAGE_TITLE_Y

MUSIC_TEXT_X = BACK_BTN_X
MUSIC_TEXT_Y = OPTIONS_TITLE_Y + TITLE_HEIGHT + FAR
MUSIC_SLIDER_BG_X = SCREEN_WIDTH - PADDING - SLIDER_BG_WIDTH
MUSIC_SLIDER_BG_Y = MUSIC_TEXT_Y + (HEADING2_HEIGHT - SLIDER_BG_HEIGHT) / 2
MUSIC_DRAGGER_X = MUSIC_SLIDER_BG_X + 4
MUSIC_DRAGGER_Y = MUSIC_SLIDER_BG_Y - 12
MUSIC_VAL_Y = MUSIC_SLIDER_BG_Y + 4

SOUND_TEXT_X = BACK_BTN_X
SOUND_TEXT_Y = MUSIC_TEXT_Y + HEADING2_HEIGHT + FAR
SOUND_SLIDER_BG_X = MUSIC_SLIDER_BG_X
SOUND_SLIDER_BG_Y = SOUND_TEXT_Y + (HEADING2_HEIGHT - SLIDER_BG_HEIGHT) / 2
SOUND_DRAGGER_X = MUSIC_DRAGGER_X
SOUND_DRAGGER_Y = SOUND_SLIDER_BG_Y - 12
SOUND_VAL_Y = SOUND_SLIDER_BG_Y + 4

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

# Trophies menu
TROPHIES_TITLE_X = PAGE_TITLE_X
TROPHIES_TITLE_Y = PAGE_TITLE_Y

TROPHY_HEADING_X = PADDING
TROPHY_HEADING_Y = TROPHIES_TITLE_Y + TITLE_HEIGHT + FAR
TROPHY_TEXT_X = TROPHY_HEADING_X
TROPHY_TEXT_Y = TROPHY_HEADING_Y + HEADING2_HEIGHT + NEAR

TROPHY_HEADING_GAP = HEADING2_HEIGHT + NEAR + TEXT_HEIGHT + FAR

# Themes menu
THEMES_TITLE_X = PAGE_TITLE_X
THEMES_TITLE_Y = PAGE_TITLE_Y

THEME_NAME_BOX_WIDTH = 150
THEME_NAME_BOX_HEIGHT = 60

THEME_OPTION_X = THEMES_TITLE_X
THEME_OPTION_NAME_BOX_X = THEME_OPTION_X + BTN_WIDTH + NEAR
THEME_OPTION_HELP_TXT_X = THEME_OPTION_NAME_BOX_X + THEME_NAME_BOX_WIDTH + NEAR
THEME_OPTION_HELP_TXT_SIZE = 40
THEME_OPTION_HEIGHT = THEME_NAME_BOX_HEIGHT + FAR
THEME_OPTION1_Y = THEMES_TITLE_Y + TITLE_HEIGHT + FAR

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
def txtArea(text, size=TEXT_SIZE, font=TEXT_FONT):
    return font.render(text, size=size)[1]


def drawText(text, x, y, size=TEXT_SIZE, color=WHITE, font=TEXT_FONT, align_right=False):
    if align_right:
        font.render_to(SCREEN, (x - txtArea(text).width, y), text, color, size=size)
    else:
        font.render_to(SCREEN, (x, y), text, color, size=size)


def drawObject(object, x, y):
    return SCREEN.blit(object, (x, y))


# Detecting clicks on UI element
def clickBox(el_pos=(0, 0), element=0, slider_value=0):  # 0-Button, 1-switch, 2-slider
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
        height = DRAGGER_HEIGHT
        width = DRAGGER_WIDTH
        corner_rad = DRAGGER_CORNER_RAD
        el_x = el_pos[0] + (SLIDING_DISTANCE * optionsValues(slider_value)) + 4
        el_y = el_pos[1] - 12
    elif element == 3:
        height = SELECTOR_BTN_HEIGHT
        width = SELECTOR_BTN_WIDTH
        corner_rad = SELECTOR_BTN_CORNER_RAD
        el_x, el_y = el_pos  # Element position

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


# Setting UI element states
def activateButtonClickState(button):
    if button is not None:
        btn_x, btn_y = button
        drawObject(CLICK_MASK, btn_x, btn_y)


def activateButtonHoverState(button):
    if button is not None:
        btn_x, btn_y = button
        drawObject(HOVER_MASK, btn_x, btn_y - 1)


def activateSwitchHoverState(switch):
    if switch is not None:
        switch_x, switch_y = switch
        drawObject(SWITCH_MASK, switch_x - SWITCH_MASK_OFFSET_X, switch_y - SWITCH_MASK_OFFSET_Y)
        drawOptionsSwitches()


def activateSliderHoverState(slider):
    if slider is not None:
        slider_x, slider_y = slider
        drawObject(SLIDER_MASK, slider_x - SLIDER_MASK_OFFSET_X, slider_y - SLIDER_MASK_OFFSET_Y)
        drawSliders()


def activateSelectorClickState(selector, side):
    if selector is not None:
        selector_x, selector_y = selector
        if side == "left":
            drawObject(L_SELECTOR_CLICKED, selector_x, selector_y)
        else:
            drawObject(R_SELECTOR_CLICKED, selector_x, selector_y)


# Sound
def playSound(sound):
    sound.set_volume(optionsValues("sound") / 2)
    sound.play()


def musicControl(change_volume=False):
    pygame.mixer.music.set_volume(optionsValues("music") / 2)
    if not change_volume:
        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.play(-1)


# Misc
def drawTransparentOverlay(opacity=200, dark=True):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    if dark:
        overlay.fill((0, 0, 0, opacity))
    else:
        overlay.fill((255, 255, 255, opacity))

    SCREEN.blit(overlay, (0, 0))


def updateScreenAndDelayNextUpdate(delay=1000):
    pygame.display.update()  # Without it, UI content wouldn't be displayed for determined time
    pygame.time.delay(delay)  # default delay is 1000 ms
    pygame.event.clear()  # Don't accept inputs during delay, because game wasn't active


# GAME
def showBoard(board, theme):
    if theme.bg is not None:
        drawObject(theme.bg, BOARD_X, BOARD_Y)
        makeGameBoardBordersRound()

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                drawObject(theme.empty_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 1:
                drawObject(theme.I_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 2:
                drawObject(theme.O_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 3:
                drawObject(theme.L_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 4:
                drawObject(theme.J_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 5:
                drawObject(theme.T_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 6:
                drawObject(theme.Z_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 7:
                drawObject(theme.S_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)
            elif board[row][col] == 8:
                drawObject(theme.shadow_cell, BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL)


def makeGameBoardBordersRound():
    drawObject(THEME_BG_BORDER_RADIUS, BOARD_X, BOARD_BG_BORDER_RADIUS_Y)


def showNextBlockArea(next_block_area, theme):
    for row in range(NEXT_BLOCK_AREA_HEIGHT):
        for col in range(NEXT_BLOCK_AREA_WIDTH):
            if next_block_area[row][col] == 0:
                drawObject(CLASSIC_EMPTY_CELL, NEXT_BLOCK_AREA_X + col * BOARD_CELL,
                           NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 1:
                drawObject(theme.I_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 2:
                drawObject(theme.O_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 3:
                drawObject(theme.L_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 4:
                drawObject(theme.J_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 5:
                drawObject(theme.T_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 6:
                drawObject(theme.Z_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 7:
                drawObject(theme.S_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL, NEXT_BLOCK_AREA_Y + row * BOARD_CELL)
            elif next_block_area[row][col] == 8:
                drawObject(theme.shadow_cell, NEXT_BLOCK_AREA_X + col * BOARD_CELL,
                           NEXT_BLOCK_AREA_Y + row * BOARD_CELL)

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


def showGameOverScreen(theme):
    drawTransparentOverlay()

    # Message
    if theme.name == "XP":
        drawObject(XP_GAME_OVER_SCREEN, BOARD_X, BOARD_Y)
    elif theme.name == "Yin-Yang":
        drawObject(YIN_YANG_GAME_OVER_SCREEN, BOARD_X, BOARD_Y)
    else:
        txt_area = txtArea("Game Over", size=TITLE_SIZE, font=TITLE_FONT)
        x_pos = BOARD_X + (BOARD_SCREEN_WIDTH - txt_area.width) / 2
        y_pos = BOARD_Y + (BOARD_SCREEN_HEIGHT - txt_area.height) / 2
        drawText("Game Over", x_pos, y_pos, size=TITLE_SIZE, font=TITLE_FONT)

    # Buttons
    drawObject(NEW_GAME_BTN, NEW_GAME_BTN_X, NEW_GAME_BTN_Y)
    drawObject(END_BTN, END_BTN_X, END_BTN_Y)


def showCountdown(countdown):
    drawTransparentOverlay()

    txt_area = txtArea(str(countdown), size=TITLE_SIZE, font=TITLE_FONT)
    x_pos = BOARD_X + (BOARD_SCREEN_WIDTH - txt_area.width) / 2
    y_pos = BOARD_Y + (BOARD_SCREEN_HEIGHT - txt_area.height) / 2
    drawText(str(countdown), x_pos, y_pos, size=TITLE_SIZE, font=TITLE_FONT)

    updateScreenAndDelayNextUpdate()


def showSaveConfirmation(resume_game_if_saved):
    if not resume_game_if_saved:
        showPauseMenu()

    drawTransparentOverlay(dark=False)
    drawText("Saved", SAVED_TXT_X, SAVED_TXT_Y, size=TITLE_SIZE, font=TITLE_FONT, color=DARK_GREY)
    updateScreenAndDelayNextUpdate()


def isMouseOnGameBoard(mouse_pos):
    # Is cursor on game board?
    if BOARD_X < mouse_pos[0] < BOARD_X_END:
        if BOARD_Y < mouse_pos[1] < BOARD_Y_END:
            return True
    return False


def getPosOnMouse(mouse_pos, shape):
    # Return what Block's self.x is under mouse
    for index, x_pos in enumerate(range(BOARD_X, BOARD_X_END + BOARD_CELL, BOARD_CELL)):
        if mouse_pos[0] < x_pos:
            position = (index - 2)  # For cursor to grab center of block
            if position == -1:  # Edge cases for unique shapes
                if shape == SHAPES[1]:  # Shape - O
                    position = -1
                else:
                    position = 0
            if position == 7 or position == 8:
                if shape == SHAPES[0]:  # Shape - I
                    position = 6
                else:
                    position = 7
            return position


# MAIN MENU
def showMainMenu(game_is_saved):
    drawObject(START_BTN, START_BTN_X, START_BTN_Y)
    drawObject(SHORTCUTS_BTN, SHORTCUTS_BTN_X, SHORTCUTS_BTN_Y)
    drawObject(OPTIONS_BTN, OPTIONS_BTN_X, OPTIONS_BTN_Y)
    drawObject(STATS_BTN, STATS_BTN_X, STATS_BTN_Y)
    drawObject(TROPHIES_BTN, TROPHIES_BTN_X, TROPHIES_BTN_Y)
    drawObject(THEMES_BTN, THEMES_BTN_X, THEMES_BTN_Y)
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

    if current_page == 1:
        # First page: prev button grayed out, next colored
        drawObject(PREVIOUS_BTN_BW, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)
    elif current_page == num_of_pages:
        # Last page: prev button colored, next grayed out
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN_BW, NEXT_BTN_X, NEXT_BTN_Y)
    else:
        # Page in between: both buttons colored
        drawObject(PREVIOUS_BTN, PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
        drawObject(NEXT_BTN, NEXT_BTN_X, NEXT_BTN_Y)


# Shortcuts menu
def showShortcutsMenu(page, max_pages):
    drawNavigation(page, max_pages)

    drawText("Shortcuts", SHORTCUTS_TITLE_X, SHORTCUTS_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)

    if page == 1:
        drawText("In-game", SHORTCUTS_TYPE_X, SHORTCUTS_TYPE_Y, size=HEADING2_SIZE, font=HEADING_FONT)

        for i in range(len(GAME_SC_KEYS)):
            row_y = getShortcutRowY(i)
            text_y = getShortcutTextY(row_y, GAME_SC_DESC[i])
            drawObject(GAME_SC_KEYS[i], SC_ROW_X, row_y)
            drawText(GAME_SC_DESC[i], SC_ROW_TXT_X, text_y)
    elif page == 2:
        drawText("Main menu", SHORTCUTS_TYPE_X, SHORTCUTS_TYPE_Y, size=HEADING2_SIZE, font=HEADING_FONT)

        for i in range(len(MENU_SC_KEYS)):
            row_y = getShortcutRowY(i)
            text_y = getShortcutTextY(row_y, MENU_SC_DESC[i])
            drawObject(MENU_SC_KEYS[i], SC_ROW_X, row_y)
            drawText(MENU_SC_DESC[i], SC_ROW_TXT_X, text_y)

            if (i + 1) == len(MENU_SC_KEYS):
                row_y = getShortcutRowY(i + 1)
                text_y = getShortcutTextY(row_y, SPACE_KEY_DESC)
                drawObject(SPACE_KEY_IMG, SC_ROW_X, row_y)
                drawText(SPACE_KEY_DESC, SPACE_KEY_DESC_X, text_y)


def getShortcutRowY(index):
    return SC_ROW1_Y + index * SC_ROW_HEIGHT


def getShortcutTextY(row_y, text):
    return row_y + (KEY_HEIGHT - txtArea(text).height) / 2


# Options menu
def showOptionsMenu():
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)

    drawText("Options", OPTIONS_TITLE_X, OPTIONS_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)
    drawText("Music", MUSIC_TEXT_X, MUSIC_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Sound", SOUND_TEXT_X, SOUND_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Stages", STAGES_TEXT_X, STAGES_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Block shadows", BLOCK_SHADOW_TEXT_X, BLOCK_SHADOW_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)
    drawText("Powers", POWERS_TEXT_X, POWERS_TEXT_Y, size=HEADING2_SIZE, font=HEADING_FONT)

    drawOptionsSwitches()
    drawSliders()
    drawSliders()  # 2x because volume text is dim and if slider mask is activated, volume text becomes bright (because mask fn calls drawSliders)


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


def drawSliders():
    music_value = round(optionsValues("music") * 100)
    sound_value = round(optionsValues("sound") * 100)

    drawText(str(music_value), MUSIC_SLIDER_BG_X - 10, MUSIC_VAL_Y, align_right=True)
    drawText(str(sound_value), SOUND_SLIDER_BG_X - 10, SOUND_VAL_Y, align_right=True)

    drawObject(SLIDER_BG, MUSIC_SLIDER_BG_X, MUSIC_SLIDER_BG_Y)
    drawObject(DRAGGER, getMusicDraggerPos()[0], MUSIC_DRAGGER_Y)
    drawObject(SLIDER_BG, SOUND_SLIDER_BG_X, SOUND_SLIDER_BG_Y)
    drawObject(DRAGGER, getSoundDraggerPos()[0], SOUND_DRAGGER_Y)


def getMusicDraggerPos():
    x = MUSIC_DRAGGER_X + (SLIDING_DISTANCE * optionsValues("music"))
    y = MUSIC_DRAGGER_Y
    return x, y


def getSoundDraggerPos():
    x = SOUND_DRAGGER_X + (SLIDING_DISTANCE * optionsValues("sound"))
    y = SOUND_DRAGGER_Y
    return x, y


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


def unlockedTrophies():
    unlocked = 0
    for i in range(len(TROPHIES)):
        for j in range(len(TROPHIES[i])):
            if trophyCompletion(TROPHIES[i][j][2], TROPHIES[i][j][3]) == WHITE:
                unlocked += 1
    saveStat("trophies", unlocked, compare=1)


# Themes menu
def themeButtonPos(i):
    return THEME_OPTION_X, THEME_OPTION1_Y + i * THEME_OPTION_HEIGHT


def showThemesScreen(themes):
    drawObject(BACK_BTN, BACK_BTN_X, BACK_BTN_Y)
    drawText("Themes", OPTIONS_TITLE_X, OPTIONS_TITLE_Y, size=TITLE_SIZE, font=TITLE_FONT)

    for i, j in enumerate(themes):
        option_y = THEME_OPTION1_Y + i * THEME_OPTION_HEIGHT
        name_x = THEME_OPTION_NAME_BOX_X + (THEME_NAME_BOX_WIDTH - txtArea(themes[j]["name"]).width) / 2
        name_y = option_y + (THEME_NAME_BOX_HEIGHT - txtArea(themes[j]["name"]).height) / 2

        if themes[j]["unlocked"]:
            theme_button = ACTIVATE_THEME_BTN
        else:
            theme_button = DISABLED_THEME_BTN
            message = "Need %d more trophies" % (themes[j]["trophies_needed"])
            text_y = option_y + (THEME_NAME_BOX_HEIGHT - txtArea(message, size=THEME_OPTION_HELP_TXT_SIZE).height) / 2
            drawText(message, THEME_OPTION_HELP_TXT_X, text_y, size=THEME_OPTION_HELP_TXT_SIZE)

        if themes[j]["active"]:
            theme_name_box = THEME_SELECTED_OPTION_BOX
            theme_button = pygame.Surface((0, 0))  # No button for active theme
        else:
            theme_name_box = THEME_OPTION_BOX

        drawObject(theme_button, THEME_OPTION_X, option_y)
        drawObject(theme_name_box, THEME_OPTION_NAME_BOX_X, option_y)
        drawText(themes[j]["name"], name_x, name_y)


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
def showWishlistScreen(block_under_cursor, theme):
    highlightBoard()
    showPowerHelpText("Click on a block to use it")
    displayBlocksSelection(theme)
    highlightBlockUnderCursor(block_under_cursor, theme)


def displayBlocksSelection(theme):
    for i, block in enumerate(theme.block_images):
        SCREEN.blit(block, (BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * i))


def highlightBlockUnderCursor(block_under_cursor, theme):
    if block_under_cursor is not None:
        index, block_area = block_under_cursor  # Unpack tuple

        SCREEN.blit(theme.block_images_hl[index], (BLOCK_SELECTION_X, BLOCK_SELECTION_Y + BLOCK_IMAGE_SPACING * index))


# Laser
def showLaserScreen(row, theme):
    highlightBoard()
    highlightRow(row, theme)
    makeGameBoardBordersRound()
    showPowerHelpText("Click on a row to remove it")


def highlightRow(row, theme):
    if row is not None:
        index, row_y = row  # Unpack tuple
        highlight = pygame.Surface((BOARD_SCREEN_WIDTH, BOARD_CELL), pygame.SRCALPHA)

        if theme.name == "Yin-Yang":
            highlight.fill(TRANSPARENT_BLACK)
        else:
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
