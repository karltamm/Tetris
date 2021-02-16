import pygame
import sys
from board import *
from nextblock import *
from blocks import *
from screen import *
from stats import *

# Initialize pygame
pygame.init()
CLOCK = pygame.time.Clock()


# FUNCTIONS
# Close program
def closeProgram():
    closeStatsDB()
    pygame.quit()
    sys.exit()


# Playing the game
def startNewGame():
    # Game states
    game_running = True  # unpaused or not
    game_over = False

    # Buttons position
    pause_button = (PAUSE_BTN_X, PAUSE_BTN_Y)
    end_button = (END_BTN_X, END_BTN_Y)  # End game
    new_game_button = (NEW_GAME_BTN_X, NEW_GAME_BTN_Y)  # If game is over, this button will be shown

    # Initialize game
    board = createBoard()
    next_block_area = createNextBlockArea()

    batch = BlocksBatch()
    current_block = Block(batch.getBlock(), board)
    next_block = getNextBlock(batch.getBlock(), next_block_area)

    current_score = 0
    high_score = getHighScore()

    # Block movement control
    down_pressed = False
    left_pressed = False
    right_pressed = False
    key_timer = 0

    # Block automatic falling
    fall_timer = 0
    fall_speed = 0.4  # Every X second trigger block autofall
    
    # Game stage
    stage = 1
    

    run = True
    while run:
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)

        updateBoard(board)
        updateNextBlockArea(next_block_area)
        updateScore(current_score, high_score, stage)
        updateGameButtons()

        if game_over:
            updateGameOverScreen()
        elif not game_running:
            updatePauseMenu()

        pygame.display.update()

        # UI control
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                closeProgram()

            # If game is over
            if event.type == GAME_OVER:
                game_running = False
                game_over = True
                saveHighScore(current_score, high_score)

            # Pause or unpause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not game_over:
                    game_running = not game_running

            # Buttons clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if checkButtonPress(mouse_pos, new_game_button) and game_over:
                        # Run following code only if game is over
                        # new_game_button is shown when game is over
                        # new_game_button is at the same place, where pause/unpause button (click areas overlap)

                        # Start new game
                        run = False  # End current game process
                        startNewGame()
                    elif checkButtonPress(mouse_pos, pause_button):
                        # Pause or unpause game
                        game_running = not game_running
                    elif checkButtonPress(mouse_pos, end_button):
                        # End game and go to the main menu
                        run = False # Stop game process
                        main_menu()

        # Block movement control
        if game_running:
            # For holding down keys
            key_timer += 1

            # For stage (higher stage -> faster block autofall)
            if current_score >= (1000 * stage):  # Next stage every 1000 score
                stage += 1
                fall_speed *= 0.9

            # Block automatic falling
            fall_timer += 1
            if (fall_timer / FPS) > fall_speed:
                fall_timer = 0
                if not down_pressed:
                    current_block.move(board, 0, 1, autofall=True)

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
                    elif event.key == pygame.K_SPACE:  # Pressing space instantly drops current block
                        while not current_block.is_placed:
                            current_score = increaseScore(current_score, FAST_DROP_POINTS)
                            current_block.move(board, 0, 1, autofall=True)
                        MOVE_SOUND.play()

                elif event.type == pygame.KEYUP:  # If a key is released
                    if event.key == pygame.K_DOWN:
                        down_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = False
                    elif event.key == pygame.K_LEFT:
                        left_pressed = False

            # Move blocks
            if down_pressed and key_timer % 4 == 0:
                current_block.move(board, 0, 1)
                # Give points for faster drops
                current_score = increaseScore(current_score, FAST_DROP_POINTS)
            elif right_pressed and key_timer % 10 == 0:
                current_block.move(board, 1, 0)
            elif left_pressed and key_timer % 10 == 0:
                current_block.move(board, -1, 0)

            # Is current block placed?
            if current_block.is_placed:
                full_rows = clearFullRows(board)

                current_block = Block(next_block, board)
                next_block = getNextBlock(batch.getBlock(), next_block_area)

                # Give points for cleared rows
                if full_rows > 0:
                    current_score = increaseScore(current_score, FULL_ROW_POINTS, full_rows)
                    
                    # Sound effect if at least one row is cleared
                    ROW_CLEARED_SOUND.play()


# Main menu
def main_menu():
    # Button positions
    start_button = [START_BTN_X, START_BTN_Y]  # New game
    quit_button = [QUIT_BTN_X, QUIT_BTN_Y]  # Quit program

    run = True
    while run:
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        updateMainMenu()
        pygame.display.update()

        # UI control
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Buttons clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if checkButtonPress(mouse_pos, start_button):
                        run = False # Stop main menu proccess
                        startNewGame()
                    elif checkButtonPress(mouse_pos, quit_button):
                        closeProgram()


main_menu()  # Launch main menu when program is opened
