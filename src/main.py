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
    
    # For holding down keys
    down_pressed = False
    left_pressed = False
    right_pressed = False
    key_timer = 0
    # Block automatic falling
    fall_timer = 0
    FALL_SPEED = 25 # Lower value -> Faster drop speed

    run = True
    while run:
        CLOCK.tick(FPS)
        
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
            if event.type == pygame.KEYDOWN: # If a key is pressed down
                key_timer = 0
                if event.key == pygame.K_UP:
                    current_block.rotate(board)
                elif event.key == pygame.K_DOWN:
                    down_pressed = True
                elif event.key == pygame.K_RIGHT:
                    right_pressed = True
                elif event.key == pygame.K_LEFT:
                    left_pressed = True
                    
            elif event.type == pygame.KEYUP: # If a key is released
                if event.key == pygame.K_DOWN:
                    down_pressed = False
                elif event.key == pygame.K_RIGHT:
                    right_pressed = False
                elif event.key == pygame.K_LEFT:
                    left_pressed = False
                    
        if down_pressed and key_timer % 3 == 0:
                changeBlock = current_block.move(board, 0, 1)
        if right_pressed and key_timer % 10 == 0:
                current_block.move(board, 1, 0)
        if left_pressed and key_timer % 10 == 0:
                current_block.move(board, -1, 0)

        # Is current block placed?
        if current_block.is_placed == True:
            clearFullRows(board)
            current_block = randomBlock(board)

        # Screen
        updateScreen(board)

main()
