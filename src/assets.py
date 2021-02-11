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

# Colors
LIGHT_GREY = (209, 209, 209)
DARK_GREY = (43, 43, 43)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (18, 71, 219)
NEON_BLUE = (78, 250, 252)

# Fonts
CHATHURA_RG = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-regular.ttf"))

# Buttons
START_BTN = pygame.image.load(os.path.join("assets/buttons", "Start.png"))
OPTIONS_BTN = pygame.image.load(os.path.join("assets/buttons", "Options.png"))
STATS_BTN = pygame.image.load(os.path.join("assets/buttons", "Stats.png"))
QUIT_BTN = pygame.image.load(os.path.join("assets/buttons", "Quit.png"))

RESUME_BTN = pygame.image.load(os.path.join("assets/buttons", "Resume.png"))
PAUSE_BTN = pygame.image.load(os.path.join("assets/buttons", "Pause.png"))
END_BTN = pygame.image.load(os.path.join("assets/buttons", "End.png"))

# Images
LOGO = pygame.image.load(os.path.join("assets", "logo.png"))
INSTRUCTION_IMAGE = pygame.image.load(os.path.join("assets", "instruction.png"))
