import pygame
import pygame.freetype
import os

# INITIALIZE
pygame.init()

# Initialize screen for image loading (to use convert_alpha())
SCREEN_WIDTH = 600  # px
SCREEN_HEIGHT = 790  # px
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# FUNCTIONS
def loadImage(folder, file_name):
    return pygame.image.load(os.path.join("../assets/images", folder, file_name)).convert_alpha()


def loadFont(folder, file_name):
    return pygame.freetype.Font(os.path.join("../assets/fonts", folder, file_name))


def loadSound(folder, file_name):
    return pygame.mixer.Sound(os.path.join("../assets/sounds", folder, file_name))


def getMusicFilePath(file_name):
    return os.path.join("../assets/music", file_name)


# THEMES
TRANSPARENT_CELL = loadImage("themes", "transparent_cell.png")
THEME_BG_BORDER_RADIUS = loadImage("themes", "theme_bg_border_radius.png")

# Classic
CLASSIC_EMPTY_CELL = loadImage("themes/classic/cells", "empty.png")
CLASSIC_SHADOW_CELL = loadImage("themes/classic/cells", "shadow.png")
CLASSIC_GREEN_CELL = loadImage("themes/classic/cells", "green.png")
CLASSIC_BRONZE_CELL = loadImage("themes/classic/cells", "bronze.png")
CLASSIC_PURPLE_CELL = loadImage("themes/classic/cells", "purple.png")
CLASSIC_PINK_CELL = loadImage("themes/classic/cells", "pink.png")
CLASSIC_RED_CELL = loadImage("themes/classic/cells", "red.png")
CLASSIC_YELLOW_CELL = loadImage("themes/classic/cells", "yellow.png")
CLASSIC_BLUE_CELL = loadImage("themes/classic/cells", "blue.png")
CELLS_IMAGES = [CLASSIC_GREEN_CELL, CLASSIC_BRONZE_CELL, CLASSIC_PURPLE_CELL, CLASSIC_PINK_CELL, CLASSIC_RED_CELL,
                CLASSIC_YELLOW_CELL, CLASSIC_BLUE_CELL]  # For animation

# XP
XP_SHADOW_CELL = CLASSIC_SHADOW_CELL
XP_BLUE_CELL = loadImage("themes/XP", "blue_cell.png")
XP_BG = loadImage("themes/XP", "bg.png")
XP_GAME_OVER_SCREEN = loadImage("themes/XP", "game_over.png")
XP_GAME_OVER_SOUND = loadSound("gamestate", "XP_gameover.mp3")

# Yin yang
YIN_YANG_SHADOW_CELL = loadImage("themes/yin_yang/cells", "shadow.png")
YIN_YANG_BLACK_CELL = loadImage("themes/yin_yang/cells", "black.png")
YIN_YANG_BG = loadImage("themes/yin_yang", "bg.png")
YIN_YANG_GAME_OVER_SCREEN = loadImage("themes/yin_yang", "game_over.png")
YIN_YANG_GAME_OVER_SOUND = loadSound("gamestate", "yin_yang_gameover.mp3")

# COLORS
LIGHT_GREY = (209, 209, 209)
GREY = (120, 120, 120)
DARK_GREY = (43, 43, 43)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (18, 71, 219)
NEON_BLUE = (78, 250, 252)
LIGHT_ORANGE = (252, 144, 78)
LAVENDER = (230, 230, 250)
NEON_GREEN = (66, 245, 114)
RICH_YELLOW = (252, 186, 3)
TRANSPARENT_WHITE = (255, 255, 255, 100)
TRANSPARENT_BLACK = (0, 0, 0, 189)

# FONTS
CHATHURA_LIGHT = loadFont("chathura", "chathura-light.ttf")
CHATHURA_RG = loadFont("chathura", "chathura-regular.ttf")
CHATHURA_XBOLD = loadFont("chathura", "chathura-extrabold.ttf")
CHATHURA_BOLD = loadFont("chathura", "chathura-bold.ttf")

# BUTTONS
CLICK_MASK = loadImage("buttons", "click_mask.png")
HOVER_MASK = loadImage("buttons", "hover_mask.png")

# Main Menu
START_BTN = loadImage("buttons", "Start.png")
CONTINUE_BTN = loadImage("buttons", "Continue.png")
CONTINUE_BTN_BW = loadImage("buttons", "ContinueBW.png")
OPTIONS_BTN = loadImage("buttons", "Options.png")
STATS_BTN = loadImage("buttons", "Stats.png")
TROPHIES_BTN = loadImage("buttons", "Trophies.png")
THEMES_BTN = loadImage("buttons", "Themes.png")
SHORTCUTS_BTN = loadImage("buttons", "Shortcuts.png")
QUIT_BTN = loadImage("buttons", "Quit.png")

# Game
RESUME_BTN = loadImage("buttons", "Resume.png")
SAVE_BTN = loadImage("buttons", "Save.png")
PAUSE_BTN = loadImage("buttons", "Pause.png")
END_BTN = loadImage("buttons", "End.png")
NEW_GAME_BTN = loadImage("buttons", "NewGame.png")

# Powers
LASER_BTN = loadImage("buttons", "Laser.png")
WISHLIST_BTN = loadImage("buttons", "Wishlist.png")
TIMELESS_BTN = loadImage("buttons", "Timeless.png")
CANCEL_POWER_BTN = loadImage("buttons", "Cancel.png")

# Navigation
BACK_BTN = loadImage("buttons", "Back.png")
PREVIOUS_BTN = loadImage("buttons", "Previous.png")
NEXT_BTN = loadImage("buttons", "Next.png")
PREVIOUS_BTN_BW = loadImage("buttons", "PreviousBW.png")
NEXT_BTN_BW = loadImage("buttons", "NextBW.png")

# SWITCHES
ON_SWITCH = loadImage("switches", "On.png")
OFF_SWITCH = loadImage("switches", "Off.png")

# SLIDERS
SLIDER_BG = loadImage("sliders", "SliderBackground.png")
DRAGGER = loadImage("sliders", "Dragger.png")

# THEME OPTIONS
THEME_OPTION_BOX = loadImage("themes/list", "ListOption.png")
THEME_SELECTED_OPTION_BOX = loadImage("themes/list", "SelectedOption.png")
ACTIVATE_THEME_BTN = loadImage("buttons", "ThemeActivate.png")
DISABLED_THEME_BTN = loadImage("buttons", "ThemeDisabled.png")

# MISC
INSTRUCTION_IMAGE = loadImage("misc", "instruction.png")

# KEYBOARD
ESC_KEY_IMG = loadImage("keys", "esc_key.png")
E_KEY_IMG = loadImage("keys", "E_key.png")
P_KEY_IMG = loadImage("keys", "P_key.png")
S_KEY_IMG = loadImage("keys", "S_key.png")
N_KEY_IMG = loadImage("keys", "N_key.png")

# SOUNDS
MOVE_SOUND = loadSound("playing", "move.mp3")
MOVE3_SOUND = loadSound("playing", "move3.mp3")
ROTATE_SOUND = loadSound("playing", "rotate.mp3")
ROW_CLEARED_SOUND = loadSound("playing", "rowcleared.mp3")
GAME_OVER_SOUND = loadSound("gamestate", "gameover.mp3")
GAME_SAVE_SOUND = loadSound("gamestate", "gamesave.mp3")
RESUME_SOUND = loadSound("countdown", "resume.mp3")
TICK_SOUND = loadSound("countdown", "tick.mp3")
LASER_SOUND = loadSound("powers", "laser.mp3")
APPEAR_SOUND = loadSound("powers", "appear.mp3")
REWIND_SOUND = loadSound("powers", "rewind.mp3")
TAKEOFF_SOUND = loadSound("powers", "takeoff.mp3")

# MUSIC
MUSIC = getMusicFilePath("music.mp3")

# POWERS
# Classic theme
CLASSIC_BLOCK_I = loadImage("themes/classic/blocks", "I_block.png")
CLASSIC_BLOCK_O = loadImage("themes/classic/blocks", "O_block.png")
CLASSIC_BLOCK_L = loadImage("themes/classic/blocks", "L_block.png")
CLASSIC_BLOCK_J = loadImage("themes/classic/blocks", "J_block.png")
CLASSIC_BLOCK_T = loadImage("themes/classic/blocks", "T_block.png")
CLASSIC_BLOCK_Z = loadImage("themes/classic/blocks", "Z_block.png")
CLASSIC_BLOCK_S = loadImage("themes/classic/blocks", "S_block.png")
CLASSIC_BLOCK_IMAGES = [CLASSIC_BLOCK_I, CLASSIC_BLOCK_O, CLASSIC_BLOCK_L, CLASSIC_BLOCK_J, CLASSIC_BLOCK_T,
                        CLASSIC_BLOCK_Z, CLASSIC_BLOCK_S]  # Do not change the order!

CLASSIC_BLOCK_I_HL = loadImage("themes/classic/blocks", "I_block_HL.png")
CLASSIC_BLOCK_O_HL = loadImage("themes/classic/blocks", "O_block_HL.png")
CLASSIC_BLOCK_L_HL = loadImage("themes/classic/blocks", "L_block_HL.png")
CLASSIC_BLOCK_J_HL = loadImage("themes/classic/blocks", "J_block_HL.png")
CLASSIC_BLOCK_T_HL = loadImage("themes/classic/blocks", "T_block_HL.png")
CLASSIC_BLOCK_Z_HL = loadImage("themes/classic/blocks", "Z_block_HL.png")
CLASSIC_BLOCK_S_HL = loadImage("themes/classic/blocks", "S_block_HL.png")
CLASSIC_BLOCK_IMAGES_HL = [CLASSIC_BLOCK_I_HL, CLASSIC_BLOCK_O_HL, CLASSIC_BLOCK_L_HL, CLASSIC_BLOCK_J_HL,
                           CLASSIC_BLOCK_T_HL, CLASSIC_BLOCK_Z_HL,
                           CLASSIC_BLOCK_S_HL]  # Do not change the order!

# XP theme
XP_BLOCK_I = loadImage("themes/XP/blocks", "I_block.png")
XP_BLOCK_O = loadImage("themes/XP/blocks", "O_block.png")
XP_BLOCK_L = loadImage("themes/XP/blocks", "L_block.png")
XP_BLOCK_J = loadImage("themes/XP/blocks", "J_block.png")
XP_BLOCK_T = loadImage("themes/XP/blocks", "T_block.png")
XP_BLOCK_Z = loadImage("themes/XP/blocks", "Z_block.png")
XP_BLOCK_S = loadImage("themes/XP/blocks", "S_block.png")
XP_BLOCK_IMAGES = [XP_BLOCK_I, XP_BLOCK_O, XP_BLOCK_L, XP_BLOCK_J, XP_BLOCK_T, XP_BLOCK_Z,
                   XP_BLOCK_S]  # Do not change the order!

XP_BLOCK_I_HL = loadImage("themes/XP/blocks", "I_block_HL.png")
XP_BLOCK_O_HL = loadImage("themes/XP/blocks", "O_block_HL.png")
XP_BLOCK_L_HL = loadImage("themes/XP/blocks", "L_block_HL.png")
XP_BLOCK_J_HL = loadImage("themes/XP/blocks", "J_block_HL.png")
XP_BLOCK_T_HL = loadImage("themes/XP/blocks", "T_block_HL.png")
XP_BLOCK_Z_HL = loadImage("themes/XP/blocks", "Z_block_HL.png")
XP_BLOCK_S_HL = loadImage("themes/XP/blocks", "S_block_HL.png")
XP_BLOCK_IMAGES_HL = [XP_BLOCK_I_HL, XP_BLOCK_O_HL, XP_BLOCK_L_HL, XP_BLOCK_J_HL, XP_BLOCK_T_HL, XP_BLOCK_Z_HL,
                      XP_BLOCK_S_HL]  # Do not change the order!

# Yin yang theme
YIN_YANG_BLOCK_I = loadImage("themes/yin_yang/blocks", "I_block.png")
YIN_YANG_BLOCK_O = loadImage("themes/yin_yang/blocks", "O_block.png")
YIN_YANG_BLOCK_L = loadImage("themes/yin_yang/blocks", "L_block.png")
YIN_YANG_BLOCK_J = loadImage("themes/yin_yang/blocks", "J_block.png")
YIN_YANG_BLOCK_T = loadImage("themes/yin_yang/blocks", "T_block.png")
YIN_YANG_BLOCK_Z = loadImage("themes/yin_yang/blocks", "Z_block.png")
YIN_YANG_BLOCK_S = loadImage("themes/yin_yang/blocks", "S_block.png")
YIN_YANG_BLOCK_IMAGES = [YIN_YANG_BLOCK_I, YIN_YANG_BLOCK_O, YIN_YANG_BLOCK_L, YIN_YANG_BLOCK_J, YIN_YANG_BLOCK_T,
                         YIN_YANG_BLOCK_Z, YIN_YANG_BLOCK_S]  # Do not change the order!

YIN_YANG_BLOCK_I_HL = loadImage("themes/yin_yang/blocks", "I_block_HL.png")
YIN_YANG_BLOCK_O_HL = loadImage("themes/yin_yang/blocks", "O_block_HL.png")
YIN_YANG_BLOCK_L_HL = loadImage("themes/yin_yang/blocks", "L_block_HL.png")
YIN_YANG_BLOCK_J_HL = loadImage("themes/yin_yang/blocks", "J_block_HL.png")
YIN_YANG_BLOCK_T_HL = loadImage("themes/yin_yang/blocks", "T_block_HL.png")
YIN_YANG_BLOCK_Z_HL = loadImage("themes/yin_yang/blocks", "Z_block_HL.png")
YIN_YANG_BLOCK_S_HL = loadImage("themes/yin_yang/blocks", "S_block_HL.png")
YIN_YANG_BLOCK_IMAGES_HL = [YIN_YANG_BLOCK_I_HL, YIN_YANG_BLOCK_O_HL, YIN_YANG_BLOCK_L_HL, YIN_YANG_BLOCK_J_HL,
                            YIN_YANG_BLOCK_T_HL, YIN_YANG_BLOCK_Z_HL,
                            YIN_YANG_BLOCK_S_HL]  # Do not change the order!
