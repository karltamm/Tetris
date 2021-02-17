import pygame
import pygame.freetype
import os

pygame.init()

# Cells
EMPTY_CELL = pygame.image.load(os.path.join("assets/cells", "empty.png"))
GREEN_CELL = pygame.image.load(os.path.join("assets/cells", "green.png"))
BRONZE_CELL = pygame.image.load(os.path.join("assets/cells", "bronze.png"))
PURPLE_CELL = pygame.image.load(os.path.join("assets/cells", "purple.png"))
PINK_CELL = pygame.image.load(os.path.join("assets/cells", "pink.png"))
RED_CELL = pygame.image.load(os.path.join("assets/cells", "red.png"))
YELLOW_CELL = pygame.image.load(os.path.join("assets/cells", "yellow.png"))
BLUE_CELL = pygame.image.load(os.path.join("assets/cells", "blue.png"))
SHADOW_CELL = pygame.image.load(os.path.join("assets/cells", "shadow.png"))

# Colors
LIGHT_GREY = (209, 209, 209)
DARK_GREY = (43, 43, 43)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (18, 71, 219)
NEON_BLUE = (78, 250, 252)
LIGHT_ORANGE = (252, 144, 78)
LAVENDER = (230, 230, 250)
NEON_GREEN = (66, 245, 114)

# Fonts
CHATHURA_LIGHT = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-light.ttf"))
CHATHURA_RG = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-regular.ttf"))
CHATHURA_XBOLD = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-extrabold.ttf"))
CHATHURA_BOLD = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-bold.ttf"))

# Buttons
START_BTN = pygame.image.load(os.path.join("assets/buttons", "Start.png"))
OPTIONS_BTN = pygame.image.load(os.path.join("assets/buttons", "Options.png"))
STATS_BTN = pygame.image.load(os.path.join("assets/buttons", "Stats.png"))
TROPHIES_BTN = pygame.image.load(os.path.join("assets/buttons", "Trophies.png"))
QUIT_BTN = pygame.image.load(os.path.join("assets/buttons", "Quit.png"))

RESUME_BTN = pygame.image.load(os.path.join("assets/buttons", "Resume.png"))
PAUSE_BTN = pygame.image.load(os.path.join("assets/buttons", "Pause.png"))
END_BTN = pygame.image.load(os.path.join("assets/buttons", "End.png"))
NEW_GAME_BTN = pygame.image.load(os.path.join("assets/buttons", "NewGame.png"))

BACK_BTN = pygame.image.load(os.path.join("assets/buttons", "Back.png"))
PREVIOUS_BTN = pygame.image.load(os.path.join("assets/buttons", "Previous.png"))
NEXT_BTN = pygame.image.load(os.path.join("assets/buttons", "Next.png"))

# Switches
ON_SWITCH = pygame.image.load(os.path.join("assets/switches", "On.png"))
OFF_SWITCH = pygame.image.load(os.path.join("assets/switches", "Off.png"))

# Images
LOGO = pygame.image.load(os.path.join("assets", "logo.png"))
INSTRUCTION_IMAGE = pygame.image.load(os.path.join("assets", "instruction.png"))

# Sounds
MOVE_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "move.mp3"))
MOVE2_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "move2.mp3"))
ROTATE_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "rotate.mp3"))
ROW_CLEARED_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "rowcleared.mp3"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets/sounds", "gameover.mp3"))
