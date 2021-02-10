import pygame
import os
pygame.init()

# Cells
CELL_SIZE = (20, 20)
# COLORS
CELL_OUTLINE = (100, 100, 100) # Grey
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# White outline for big box
BIG_BACKGROUND = pygame.Surface((200, 400), pygame.SRCALPHA) 
pygame.draw.rect(BIG_BACKGROUND,(WHITE), (0, 0, 200, 400), 3)

# White outline for small box
SMALL_BACKGROUND = pygame.Surface((80, 220), pygame.SRCALPHA)
pygame.draw.rect(SMALL_BACKGROUND,(WHITE), (0, 0, 80, 220), 3)

# EMPTY CELL
EMPTY_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(EMPTY_CELL, (10, 10, 10), (0, 0, 20, 20)) # Very light grey in empty cells
pygame.draw.rect(EMPTY_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# GREEN_CELL
GREEN_CELL = pygame.Surface(CELL_SIZE) # GIVE SURFACE SIZE OF CELL_SIZE
pygame.draw.rect(GREEN_CELL, (0, 255, 0), (0, 0, 20, 20)) # FILL SURFACE WITH RGB VALUE OF (0, 255, 0)
pygame.draw.rect(GREEN_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1) # DRAW 1 PIXEL OUTLINE OF COLOR "CELL_OUTLINE"

# INDIGO_CELL
INDIGO_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(INDIGO_CELL, (136, 77, 255), (0, 0, 20, 20))
pygame.draw.rect(INDIGO_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# ORANGE_CELL
ORANGE_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(ORANGE_CELL, (255, 100, 0), (0, 0, 20, 20))
pygame.draw.rect(ORANGE_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# PINK_CELL
PINK_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(PINK_CELL, (255, 128, 234), (0, 0, 20, 20))
pygame.draw.rect(PINK_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# YELLOW_CELL
YELLOW_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(YELLOW_CELL, (255, 255, 0), (0, 0, 20, 20))
pygame.draw.rect(YELLOW_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# RED_CELL
RED_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(RED_CELL, RED, (0, 0, 20, 20))
pygame.draw.rect(RED_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# BLUE_CELL
BLUE_CELL = pygame.Surface(CELL_SIZE)
pygame.draw.rect(BLUE_CELL, (0, 0, 255), (0, 0, 20, 20))
pygame.draw.rect(BLUE_CELL, CELL_OUTLINE, (0, 0, 20, 20), 1)

# Fonts
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont('arial', 45)

# Functions
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)