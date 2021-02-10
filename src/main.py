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
    score = 0

    # Which UI window is shown? (main menu, game UI, in-game menu etc)
    game_window_open = True
    pause_menu_open = False

    # Blocks
    current_block = generateActiveBlock(board)
    next_block = generateNextBlock(next_block_area)

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
        SCREEN.fill(DARK_GREY)

        if game_window_open == True:
            updateBoard(board)
            updateNextBlockArea(next_block_area)
            updateScore(score)
            updateGameButtons()

            if pause_menu_open == True:
                updatePauseMenu()

        pygame.display.update()

        # UI control
        events = pygame.event.get()
        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
<<<<<<< HEAD
<<<<<<< HEAD
            # MOUSE CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # If left click
                    click = True
            # KEY PRESS
            if event.type == pygame.KEYDOWN:
                key_timer = 0
                if event.key == pygame.K_UP:
                    current_block.rotate(board)
                elif event.key == pygame.K_DOWN:
                    down_pressed = True
                elif event.key == pygame.K_RIGHT:
                    right_pressed = True
                elif event.key == pygame.K_LEFT:
                    left_pressed = True
                elif event.key == pygame.K_p:  # ONLY FOR TESTING!
                    pause_menu_open = not pause_menu_open  # Invert the boolean value
            # KEY RELEASE
            elif event.type == pygame.KEYUP:
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
            current_block = generateActiveBlock(board, next_block)
            next_block = generateNextBlock(next_block_area)
=======

            # Pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # ONLY FOR TESTING!
                    pause_menu_open = not pause_menu_open  # Invert the boolean value
=======

            # Pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # ONLY FOR TESTING!
                    pause_menu_open = not pause_menu_open  # Invert the boolean value
            
            if event.type == pygame.MOUSEBUTTONDOWN: # If mouse click
                if event.button == 1: # If left click
                    click = True
                    
        if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                pause_menu_open = not pause_menu_open
>>>>>>> parent of 098ab1a (Fixed formatting)

        # Block movement
        if game_window_open == True and pause_menu_open == False:
            # For holding down keys
            key_timer += 1

            # Block automatic falling
            fall_timer += 1
            if fall_timer > FALL_SPEED:
                fall_timer = 0
                current_block.move(board, 0, 1)

            # User input
            for event in events:
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
                current_block = generateActiveBlock(board, next_block)
                next_block = generateNextBlock(next_block_area)
<<<<<<< HEAD
>>>>>>> parent of c959aae (Clickable pause button)
=======
>>>>>>> parent of 098ab1a (Fixed formatting)


main()
