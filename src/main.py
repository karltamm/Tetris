import pygame
from board import *
from blocks import *
from screen import *

# MAIN
def main():
    pygame.init()
    CLOCK = pygame.time.Clock()

    board = createBoard() # 2D array, where "0" represents empty cell
    current_block = randomBlock(board)

    # Block automatic falling
    fall_time = 0
    FALL_SPEED = 25 # Lower value -> Faster drop speed

    run = True
    while run:
        CLOCK.tick(FPS)

        # Block automatic falling
        fall_time += 1

        if fall_time > FALL_SPEED:
            fall_time = 0
            current_block.move(board, 0, 1)

        # Input
        for event in pygame.event.get():
            # Close game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            # Move block
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_block.rotate(board)
                if event.key == pygame.K_DOWN:
                    current_block.move(board, 0, 1)
                elif event.key == pygame.K_RIGHT:
                    current_block.move(board, 1, 0)
                elif event.key == pygame.K_LEFT:
                    current_block.move(board, -1, 0)

        # Is current block placed?
        if current_block.is_placed == True:
            clearFullRows(board)
            current_block = randomBlock(board)

        # Screen
        updateScreen(board)

main()