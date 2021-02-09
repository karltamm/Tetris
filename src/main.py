import pygame
import os

from shapes import *
from blockClass import *
from functions import *

# MAIN
def main():
    board = createBoard() # 2D array, where "0" represents empty cell
    block = Block(SHAPE_J, board)
    block2 = Block(SHAPE_O, board)
    block2.move(board, 3, 6)
    run = True
    while run:
        CLOCK.tick(FPS)
        # Input
        for event in pygame.event.get():
            # Close game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Move block
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    block.rotate(board)
                if event.key == pygame.K_DOWN:
                    block.move(board, 0, 1)
                elif event.key == pygame.K_RIGHT:
                    block.move(board, 1, 0)
                elif event.key == pygame.K_LEFT:
                    block.move(board, -1, 0)
        # UI
        updateScreen(board)
main()
