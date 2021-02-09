import pygame
import os

# Screen
SCREEN_WIDTH = 300  # px
SCREEN_HEIGHT = 500  # px
FPS = 60

# INITIALIZE
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Tetris")

# Board
BOARD_WIDTH = 10  # Number of cells in a row
BOARD_HEIGHT = 20  # Number of cells in a column
BOARD_CELL = 20  # 20 px square
BOARD_X = 50 # Number of px from left edge of the screen
BOARD_Y = 50 # Number of px from top of the screen
BLOCK_WIDTH = BLOCK_HEIGHT = 4  # Block is made of 4x4 board cells

""" ASSETS """
# Cells
EMPTY_CELL = pygame.image.load(os.path.join("assets/cells", "empty.png"))
GREEN_CELL = pygame.image.load(os.path.join("assets/cells", "green.png"))
INDIGO_CELL = pygame.image.load(os.path.join("assets/cells", "indigo.png"))
ORANGE_CELL = pygame.image.load(os.path.join("assets/cells", "orange.png"))
PINK_CELL = pygame.image.load(os.path.join("assets/cells", "pink.png"))
RED_CELL = pygame.image.load(os.path.join("assets/cells", "red.png"))
YELLOW_CELL = pygame.image.load(os.path.join("assets/cells", "yellow.png"))
BLUE_CELL = pygame.image.load(os.path.join("assets/cells", "blue.png"))

# Shapes
# ? ilmselt oma failis m6tekam sest p2ris mahukas..
