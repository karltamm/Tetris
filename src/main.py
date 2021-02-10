import pygame
from board import *
from nextblock import *
from blocks import *
from screen import *


# MAIN
def main():
    # Initialize
    pygame.init()
    CLOCK = pygame.time.Clock()
    board = createBoard()  # 2D array, where "0" represents empty cell
    next_block_area = createNextBlockArea()

    # Blocks
    current_block = activeBlock(0, board)
    next_block = randomBlock(next_block_area, 0, 1)
    third_block = randomBlock(next_block_area, 0, 6)

    # For holding down keys
    down_pressed = False
    left_pressed = False
    right_pressed = False
    key_timer = 0

    # Block automatic falling
    fall_timer = 0
    FALL_SPEED = 25  # Lower value -> Faster drop speed

    run = True
    while run:
        # Screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)  # Background color
        updateBoard(board)
        updateNextBlockArea(next_block_area)
        pygame.display.update()

        # For holding down keys
        key_timer += 1

        # Block automatic falling
        fall_timer += 1
        if fall_timer > FALL_SPEED:
            fall_timer = 0
            current_block.move(board, 0, 1)

        # Input
        for event in pygame.event.get():
            # Close game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Move block
            if event.type == pygame.KEYDOWN:  # If a key is pressed down
                key_timer = 0
                if event.key == pygame.K_UP:
                    current_block.rotate(board)
                elif event.key == pygame.K_DOWN:
                    down_pressed = True
                elif event.key == pygame.K_RIGHT:
                    right_pressed = True
                elif event.key == pygame.K_LEFT:
                    left_pressed = True

            elif event.type == pygame.KEYUP:  # If a key is released
                if event.key == pygame.K_DOWN:
                    down_pressed = False
                elif event.key == pygame.K_RIGHT:
                    right_pressed = False
                elif event.key == pygame.K_LEFT:
                    left_pressed = False

        if down_pressed:
            fall_timer += 8
        if right_pressed and key_timer % 10 == 0:
            current_block.move(board, 1, 0)
        if left_pressed and key_timer % 10 == 0:
            current_block.move(board, -1, 0)

        # Is current block placed?
        if current_block.is_placed == True:
            clearFullRows(board)
            current_block = activeBlock(next_block, board)
            next_block = third_block
            NextBlock(next_block, next_block_area, 0, 1)
            third_block = randomBlock(next_block_area, 0, 6)


main()
