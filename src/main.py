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

    # Which UI window is shown?
    game_paused = False

    # Buttons
    pause_button = buttonClickBox(GAME_BTNS_AREA_X, GAME_BTNS_AREA_Y)
    end_button = buttonClickBox(GAME_BTNS_AREA_X, GAME_BTNS_AREA_Y + BTN_HEIGHT + NEAR)

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

        updateBoard(board)
        updateNextBlockArea(next_block_area)
        updateScore(score)
        updateGameButtons()

        if game_paused:
            updatePauseMenu()

        pygame.display.update()
        
        # Mouse
        mouse_pos = pygame.mouse.get_pos()

        # UI control
        events = pygame.event.get()
        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused  # Invert the boolean value
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_button.collidepoint(mouse_pos):
                        game_paused = not game_paused  # Invert the boolean value
                    elif end_button.collidepoint(mouse_pos):
                        run = False
                        pygame.quit()

        # Block movement
        if game_paused == False:
            # For holding down keys
            key_timer += 1

            # Block automatic falling
            fall_timer += 1
            if fall_timer > FALL_SPEED:
                fall_timer = 0
                current_block.move(board, 0, 1)
                if down_pressed:
                    score += 1

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
                full_rows = clearFullRows(board)
                if full_rows > 0:
                    score += 100 + (full_rows-1)*200
                current_block = generateActiveBlock(board, next_block)
                next_block = generateNextBlock(next_block_area)


main()

