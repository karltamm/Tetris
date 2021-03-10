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


# ASSETS
# Cells
EMPTY_CELL = loadImage("cells", "empty.png")
SHADOW_CELL = loadImage("cells", "shadow.png")
GREEN_CELL = loadImage("cells", "green.png")
BRONZE_CELL = loadImage("cells", "bronze.png")
PURPLE_CELL = loadImage("cells", "purple.png")
PINK_CELL = loadImage("cells", "pink.png")
RED_CELL = loadImage("cells", "red.png")
YELLOW_CELL = loadImage("cells", "yellow.png")
BLUE_CELL = loadImage("cells", "blue.png")
CELLS_IMAGES = [GREEN_CELL, BRONZE_CELL, PURPLE_CELL, PINK_CELL, RED_CELL, YELLOW_CELL, BLUE_CELL]  # For animation

# Colors
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

# Fonts
CHATHURA_LIGHT = loadFont("chathura", "chathura-light.ttf")
CHATHURA_RG = loadFont("chathura", "chathura-regular.ttf")
CHATHURA_XBOLD = loadFont("chathura", "chathura-extrabold.ttf")
CHATHURA_BOLD = loadFont("chathura", "chathura-bold.ttf")

# Buttons
CLICK_MASK = loadImage("buttons", "click_mask.png")
HOVER_MASK = loadImage("buttons", "hover_mask.png")

# Main Menu
START_BTN = loadImage("buttons", "Start.png")
CONTINUE_BTN = loadImage("buttons", "Continue.png")
CONTINUE_BTN_BW = loadImage("buttons", "ContinueBW.png")
OPTIONS_BTN = loadImage("buttons", "Options.png")
STATS_BTN = loadImage("buttons", "Stats.png")
TROPHIES_BTN = loadImage("buttons", "Trophies.png")
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

# Switches
ON_SWITCH = loadImage("switches", "On.png")
OFF_SWITCH = loadImage("switches", "Off.png")

# Sliders
SLIDER_BG = loadImage("sliders", "SliderBackground.png")
DRAGGER = loadImage("sliders", "Dragger.png")

# Misc
INSTRUCTION_IMAGE = loadImage("", "instruction.png")

# Keys
ESC_KEY_IMG = loadImage("keys", "esc_key.png")
C_KEY_IMG = loadImage("keys", "C_key.png")
E_KEY_IMG = loadImage("keys", "E_key.png")
N_KEY_IMG = loadImage("keys", "N_key.png")
O_KEY_IMG = loadImage("keys", "O_key.png")
P_KEY_IMG = loadImage("keys", "P_key.png")
S_KEY_IMG = loadImage("keys", "S_key.png")
T_KEY_IMG = loadImage("keys", "T_key.png")

# Sounds
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

# Music
MUSIC1 = getMusicFilePath("music1.mp3")
MUSIC2 = getMusicFilePath("music2.mp3")
MUSIC3 = getMusicFilePath("music3.mp3")
MUSIC4 = getMusicFilePath("music4.mp3")
MUSIC5 = getMusicFilePath("music5.mp3")

# Blocks
BLOCK_I = loadImage("blocks", "I_block.png")
BLOCK_O = loadImage("blocks", "O_block.png")
BLOCK_L = loadImage("blocks", "L_block.png")
BLOCK_J = loadImage("blocks", "J_block.png")
BLOCK_T = loadImage("blocks", "T_block.png")
BLOCK_Z = loadImage("blocks", "Z_block.png")
BLOCK_S = loadImage("blocks", "S_block.png")
BLOCK_IMAGES = [BLOCK_I, BLOCK_O, BLOCK_L, BLOCK_J, BLOCK_T, BLOCK_Z, BLOCK_S]  # Do not change the order!

BLOCK_I_HL = loadImage("blocks", "I_block_HL.png")
BLOCK_O_HL = loadImage("blocks", "O_block_HL.png")
BLOCK_L_HL = loadImage("blocks", "L_block_HL.png")
BLOCK_J_HL = loadImage("blocks", "J_block_HL.png")
BLOCK_T_HL = loadImage("blocks", "T_block_HL.png")
BLOCK_Z_HL = loadImage("blocks", "Z_block_HL.png")
BLOCK_S_HL = loadImage("blocks", "S_block_HL.png")
BLOCK_IMAGES_HL = [BLOCK_I_HL, BLOCK_O_HL, BLOCK_L_HL, BLOCK_J_HL, BLOCK_T_HL, BLOCK_Z_HL,
                   BLOCK_S_HL]  # Do not change the order!
