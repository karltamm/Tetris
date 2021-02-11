import pygame
from board import *
from nextblock import *
from blocks import *
from screen import *

# Important initializing
pygame.init()
CLOCK = pygame.time.Clock()

# IN GAME
def game():
    # Is game running (unpaused)?
    game_running = True

    # Create button click areas
    pause_button = buttonClickBox(PAUSE_BTN_X, PAUSE_BTN_Y)
    end_button = buttonClickBox(END_BTN_X, END_BTN_Y) # End game

    # Initialize first game
    board = createBoard()
    next_block_area = createNextBlockArea()
    current_block = generateActiveBlock(board)
    next_block = generateNextBlock(next_block_area)
    score = 0

    # Block movement control
    down_pressed = False
    left_pressed = False
    right_pressed = False
    key_timer = 0

    # Block automatic falling
    fall_timer = 0
    FALL_SPEED = 25  # Lower value -> Faster drop speed

    run = True
    while run:
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        updateBoard(board)
        updateNextBlockArea(next_block_area)
        updateScore(score)
        updateGameButtons()

        if not game_running:
            updatePauseMenu()

        pygame.display.update()

        # UI control
        mouse_pos = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Pause or unpause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = not game_running

            # Buttons clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_button.collidepoint(mouse_pos):
                        # Pause or unpause game
                        game_running = not game_running
                    elif end_button.collidepoint(mouse_pos):
                        # End game
                        run = False

        # Block movement control
        if game_running:
            # For holding down keys
            key_timer += 1

            # Block automatic falling
            fall_timer += 1
            if fall_timer > FALL_SPEED:
                fall_timer = 0
                current_block.move(board, 0, 1)

                # Give points for faster drops
                if down_pressed:
                    score += 1

            # Check if user wants to move a block
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

            # Move blocks
            if down_pressed:
                fall_timer += 8
            if right_pressed and key_timer % 10 == 0:
                current_block.move(board, 1, 0)
            if left_pressed and key_timer % 10 == 0:
                current_block.move(board, -1, 0)

            # Is current block placed?
            if current_block.is_placed:
                full_rows = clearFullRows(board)
                current_block = generateActiveBlock(board, next_block)
                next_block = generateNextBlock(next_block_area)

                # Give points for cleared rows
                if full_rows > 0:
                    score += 100 + (full_rows - 1) * 200

# MENU WINDOW
def main_menu():
    # Create button click areas
    start_button = buttonClickBox(START_BTN_X, START_BTN_Y)  # New game
    quit_button = buttonClickBox(QUIT_BTN_X, QUIT_BTN_Y)  # Quit program
    run = True
    while run:
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        updateMainMenu()
        pygame.display.update()
        
        # UI control
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Buttons clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(mouse_pos):
                        # Start new game
                        game()
                    elif quit_button.collidepoint(mouse_pos):
                        # Quit program
                        run = False
                        pygame.quit()
    
main_menu()
