import pygame
import sys
from board import *
from nextblock import *
from blocks import *
from screen import *
from stats import *
from powers import *

# INITIALIZE
pygame.init()
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Tetris")


# GENERAL FUNCTIONS
def closeProgram():
    closeStatsDB()
    pygame.quit()
    sys.exit()


# GAME
def startNewGame():
    # Game states
    game_is_running = True  # unpaused or not
    game_is_over = False
    power_is_active = False

    # Countdown
    countdown_is_active = False  # If game_running goes from False to true, then show countdown
    countdown = 3

    # UI
    activate_power_button = (ACTIVATE_POWER_BTN_X, ACTIVATE_POWER_BTN_Y)
    cancel_power_button = (CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
    pause_button = (PAUSE_BTN_X, PAUSE_BTN_Y)
    end_button = (END_BTN_X, END_BTN_Y)  # End game
    new_game_button = (NEW_GAME_BTN_X, NEW_GAME_BTN_Y)  # If game is over, this button will be shown

    # Initialize game
    board = createBoard()
    next_block_area = createNextBlockArea()

    batch = BlocksBatch()
    current_block = Block(batch.getBlock(), board)
    shadow_block = ShadowBlock(current_block, board)
    next_block = getNextBlock(batch.getBlock(), next_block_area)

    solved_rows = 0
    current_score = 0
    score_counter = Score(current_score)
    high_score = getHighScore()

    power = Power()

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
        # UI control
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            # Close program
            if event.type == pygame.QUIT:
                closeProgram()

            # If game is over
            if event.type == GAME_OVER:
                game_is_running = False
                game_is_over = True
                saveHighScore(current_score, high_score)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_is_over and not countdown_is_active and not power_is_active:
                        if game_is_running:  # Pause game
                            game_is_running = False
                        else:  # Unpause
                            countdown_is_active = True

                if event.key == pygame.K_p:
                    if power.is_available and game_is_running:
                        power_is_active = True
                        game_is_running = False
                    elif power_is_active:
                        power_is_active = False
                        countdown_is_active = True

            # Buttons clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not power_is_active and not countdown_is_active:
                    if checkButtonPress(mouse_pos, end_button):
                        # End game and go to the main menu
                        run = False  # Stop game process
                        main_menu()

                if game_is_over:
                    if checkButtonPress(mouse_pos, new_game_button):
                        # Run following code only if game is over
                        # new_game_button is shown when game is over
                        # new_game_button is at the same place, where pause/unpause button (click areas overlap)

                        # Start new game
                        run = False  # End current game process
                        startNewGame()
                elif game_is_running:
                    if checkButtonPress(mouse_pos, pause_button):
                        game_is_running = False
                    if checkButtonPress(mouse_pos, activate_power_button):
                        if power.is_available:
                            power_is_active = True
                            game_is_running = False
                elif not game_is_running and not power_is_active:
                    if checkButtonPress(mouse_pos, pause_button):
                        # Unpause the game
                        countdown_is_active = True

                if power_is_active:
                    if checkButtonPress(mouse_pos, cancel_power_button):
                        power_is_active = False
                        countdown_is_active = True

        # Powers
        if power_is_active and not power.is_running:
            power.start(board_params=(board, current_block, shadow_block))

            if power.game_should_run == True:
                game_is_running = True

        if power.is_running:
            if power.name == "Laser":
                power.run(UI_control=(mouse_pos, events))
            elif power.name == "Wishlist":
                power.run(UI_control=(mouse_pos, events))
            elif power.name == "Timeless":
                power.run(current_block=current_block)

            # If power.run() stopped the process
            if not power.is_running:
                power_is_active = False
                countdown_is_active = True

                if power.game_should_run == True:
                    down_pressed = False
                    game_is_running = False

        # Player has turned off power, but power process is still runnning
        if power.is_running and not power_is_active:
            power.stop()

            if power.game_should_run == True:
                down_pressed = False
                game_is_running = False

        # Block movement control
        if game_is_running:
            shadow_block = ShadowBlock(current_block, board)  # Update

            # For holding down keys
            key_timer += 1

            # Block automatic falling
            if not power.autofall_is_off:
                fall_timer += 1
                if fall_timer / FPS > fall_speed:
                    fall_timer = 0
                    if not down_pressed:
                        current_block.move(board, y_step=1, autofall=True)

            # Check if user wants to move a block
            for event in events:
                if event.type == pygame.KEYDOWN:  # If a key is pressed down
                    key_timer = 0
                    if event.key == pygame.K_UP:
                        shadow_block.clearShadow(board)
                        current_block.rotate(board)
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = True
                    elif event.key == pygame.K_LEFT:
                        left_pressed = True
                    elif event.key == pygame.K_SPACE:  # Pressing space instantly drops current block
                        while not current_block.is_placed:
                            current_score = score_counter.drop()
                            current_block.move(board, y_step=1, autofall=True)
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
                current_block.move(board, y_step=1)
                # Give points for faster drops
                current_score = score_counter.drop()
            elif right_pressed and key_timer % 10 == 0:
                shadow_block.clearShadow(board)  # Player movement = Delete shadow block on last position
                current_block.move(board, x_step=1)
            elif left_pressed and key_timer % 10 == 0:
                shadow_block.clearShadow(board)
                current_block.move(board, x_step=-1)

            # Is current block placed?
            if current_block.is_placed:
                shadow_block.clearShadow(board)  # Clear previous shadow block
                full_rows = clearFullRows(board)

                current_block = Block(next_block, board)
                next_block = getNextBlock(batch.getBlock(), next_block_area)

                # Is row cleared?
                if full_rows > 0:
                    # Give points for cleared rows
                    current_score = score_counter.fullRow(stage, full_rows)

                    # Check current stage
                    solved_rows += full_rows
                    if solved_rows >= stage * 5:
                        stage += 1
                        fall_speed *= 0.9

                    # Sound effect if at least one row is cleared
                    ROW_CLEARED_SOUND.play()

        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)

        showBoard(board)
        showNextBlockArea(next_block_area)
        showScore(current_score, high_score, stage)
        showPowersSelection(power)
        showGameButtons()

        if game_is_over:
            showGameOverScreen()
        elif power_is_active:
            if power.name == "Laser":
                showLaserScreen(power.row)
            elif power.name == "Wishlist":
                showWishlistScreen(power.block_under_cursor)
            elif power.name == "Timeless":
                showTimelessScreen(power.num_of_blocks_left)
                showNextBlockArea(next_block_area)

            drawButton(CANCEL_POWER_BTN, CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
        elif countdown_is_active:
            showCountdown(countdown)
            countdown, countdown_is_active, game_is_running = runCountdown(countdown)
        elif not game_is_running:
            showPauseMenu()

        pygame.display.update()


def runCountdown(countdown):
    countdown -= 1

    if countdown < 1:
        RESUME_SOUND.play()
        countdown_is_active = False
        game_is_running = True
        countdown = 3  # Reset countdown
    else:
        countdown_is_active = True
        game_is_running = False

    return (countdown, countdown_is_active, game_is_running)


# MAIN MENU
def main_menu():
    # Button positions
    start_button = (START_BTN_X, START_BTN_Y)  # New game
    quit_button = (QUIT_BTN_X, QUIT_BTN_Y)  # Quit program

    run = True
    while run:
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        showMainMenu()
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
                        run = False  # Stop main menu proccess
                        startNewGame()
                    elif checkButtonPress(mouse_pos, quit_button):
                        closeProgram()


main_menu()  # Launch main menu when program is opened
