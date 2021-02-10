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
ARIAL = pygame.font.SysFont('arial', 45)
CHATHURA_RG = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-regular.ttf"))
CHATHURA_LIGHT = pygame.freetype.Font(os.path.join("assets/fonts/chathura", "chathura-light.ttf"))

# Buttons
RESUME_BTN = pygame.image.load(os.path.join("assets/buttons", "Resume.png"))
PAUSE_BTN = pygame.image.load(os.path.join("assets/buttons", "Pause.png"))
END_BTN = pygame.image.load(os.path.join("assets/buttons", "End.png"))
