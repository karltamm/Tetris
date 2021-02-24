import pygame
import pygame.freetype
import os

# INITIALIZE
pygame.init()

# Initialize screen for image loading (to use convert())
SCREEN_WIDTH = 600  # px
SCREEN_HEIGHT = 790  # px
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# FUNCTIONS
def loadImage(folder, file_name, transparent=True):
    return pygame.image.load(os.path.join(folder, file_name)).convert_alpha()


# ASSETS
# Cells
EMPTY_CELL = loadImage("assets/cells", "empty.png")
SHADOW_CELL = loadImage("assets/cells", "shadow.png")
GREEN_CELL = loadImage("assets/cells", "green.png")
BRONZE_CELL = loadImage("assets/cells", "bronze.png")
PURPLE_CELL = loadImage("assets/cells", "purple.png")
PINK_CELL = loadImage("assets/cells", "pink.png")
RED_CELL = loadImage("assets/cells", "red.png")
YELLOW_CELL = loadImage("assets/cells", "yellow.png")
BLUE_CELL = loadImage("assets/cells", "blue.png")
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
CHATHURA_LIGHT = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-light.ttf"))
CHATHURA_RG = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-regular.ttf"))
CHATHURA_XBOLD = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-extrabold.ttf"))
CHATHURA_BOLD = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-bold.ttf"))

# Buttons
# Main Menu
START_BTN = loadImage("assets/buttons", "Start.png")
OPTIONS_BTN = loadImage("assets/buttons", "Options.png")
STATS_BTN = loadImage("assets/buttons", "Stats.png")
TROPHIES_BTN = loadImage("assets/buttons", "Trophies.png")
QUIT_BTN = loadImage("assets/buttons", "Quit.png")

# Game
RESUME_BTN = loadImage("assets/buttons", "Resume.png")
PAUSE_BTN = loadImage("assets/buttons", "Pause.png")
END_BTN = loadImage("assets/buttons", "End.png")
NEW_GAME_BTN = loadImage("assets/buttons", "NewGame.png")

# Powers
LASER_BTN = loadImage("assets/buttons", "Laser.png")
WISHLIST_BTN = loadImage("assets/buttons", "Wishlist.png")
TIMELESS_BTN = loadImage("assets/buttons", "Timeless.png")
CANCEL_POWER_BTN = loadImage("assets/buttons", "Cancel.png")

# Navigation
BACK_BTN = loadImage("assets/buttons", "Back.png")
PREVIOUS_BTN = loadImage("assets/buttons", "Previous.png")
NEXT_BTN = loadImage("assets/buttons", "Next.png")
PREVIOUS_BTN_BW = loadImage("assets/buttons", "PreviousBW.png")
NEXT_BTN_BW = loadImage("assets/buttons", "NextBW.png")

# Switches
ON_SWITCH = loadImage("assets/switches", "On.png")
OFF_SWITCH = loadImage("assets/switches", "Off.png")

# Misc
INSTRUCTION_IMAGE = loadImage("assets", "instruction.png")

# Sounds
MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "move.mp3"))
MOVE2_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "move2.mp3"))
MOVE3_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "move3.mp3"))
ROTATE_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "rotate.mp3"))
ROW_CLEARED_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "rowcleared.mp3"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "gameover.mp3"))
RESUME_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "resume.mp3"))
TICK_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "tick.mp3"))
LASER_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "laser.mp3"))
LASER2_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "laser2.mp3"))
LASER3_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "laser3.mp3"))
APPEAR_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "appear.mp3"))
TIMEUP_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "timeup.mp3"))
TIMEUP2_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "timeup2.mp3"))
REWIND_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "rewind.mp3"))
TAKEOFF_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "takeoff.mp3"))

# Blocks
BLOCK_I = loadImage("assets/blocks", "I_block.png")
BLOCK_O = loadImage("assets/blocks", "O_block.png")
BLOCK_L = loadImage("assets/blocks", "L_block.png")
BLOCK_J = loadImage("assets/blocks", "J_block.png")
BLOCK_T = loadImage("assets/blocks", "T_block.png")
BLOCK_Z = loadImage("assets/blocks", "Z_block.png")
BLOCK_S = loadImage("assets/blocks", "S_block.png")
BLOCK_IMAGES = [BLOCK_I, BLOCK_O, BLOCK_L, BLOCK_J, BLOCK_T, BLOCK_Z, BLOCK_S]  # Do not change the order!

BLOCK_I_HL = loadImage("assets/blocks", "I_block_HL.png")
BLOCK_O_HL = loadImage("assets/blocks", "O_block_HL.png")
BLOCK_L_HL = loadImage("assets/blocks", "L_block_HL.png")
BLOCK_J_HL = loadImage("assets/blocks", "J_block_HL.png")
BLOCK_T_HL = loadImage("assets/blocks", "T_block_HL.png")
BLOCK_Z_HL = loadImage("assets/blocks", "Z_block_HL.png")
BLOCK_S_HL = loadImage("assets/blocks", "S_block_HL.png")
BLOCK_IMAGES_HL = [BLOCK_I_HL, BLOCK_O_HL, BLOCK_L_HL, BLOCK_J_HL, BLOCK_T_HL, BLOCK_Z_HL,
                   BLOCK_S_HL]  # Do not change the order!
