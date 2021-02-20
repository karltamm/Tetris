import pygame
import sys
from board import *
from nextblock import *
from blocks import *
from screen import *
from database import *
from powers import *

# Initialize pygame
pygame.init()
CLOCK = pygame.time.Clock()


# FUNCTIONS
# Close program
def closeProgram():
    closeDB()
    pygame.quit()
    sys.exit()


# Playing the game
def startNewGame():
    # Game states
    game_running = True  # unpaused or not
    game_over = False
    power_is_active = False

    # Countdown
    show_countdown = False  # If game_running goes from False to true, then show countdown
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
                game_running = False
                game_over = True
                saveHighScore(current_score, high_score)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_over and not show_countdown and not power_is_active:
                        if game_running:  # Pause game
                            game_running = False
                        else:  # Unpause
                            show_countdown = True

                if event.key == pygame.K_p:
                    if power.is_available and game_running:
                        power_is_active = True
                        game_running = False
                    elif power_is_active:
                        power_is_active = False
                        show_countdown = True

            # Buttons clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not power_is_active and not show_countdown:
                    if clickBox(mouse_pos, end_button, BTN_CORNER_RAD):

                        # End game and go to the main menu
                        run = False  # Stop game process
                        main_menu()

                if game_over:
                    if clickBox(mouse_pos, new_game_button, BTN_CORNER_RAD):
                        # Run following code only if game is over
                        # new_game_button is shown when game is over
                        # new_game_button is at the same place, where pause/unpause button (click areas overlap)

                        # Start new game
                        run = False  # End current game process
                        startNewGame()
                elif game_running:
                    if clickBox(mouse_pos, pause_button, BTN_CORNER_RAD):
                        game_running = False
                    if clickBox(mouse_pos, activate_power_button, BTN_CORNER_RAD):
                        if power.is_available:
                            power_is_active = True
                            game_running = False
                elif not game_running and not power_is_active:
                    if clickBox(mouse_pos, pause_button, BTN_CORNER_RAD):
                        # Unpause the game
                        show_countdown = True
                elif power_is_active:
                    if clickBox(mouse_pos, cancel_power_button, BTN_CORNER_RAD):
                        power_is_active = False
                        show_countdown = True

        # Powers
        if power_is_active:
            # Start the power
            if not power.is_running:
                if power.name == "Laser":
                    power.start(board_params=(board, current_block, shadow_block))
                elif power.name == "Wishlist":
                    power.start(board_params=(board, current_block, shadow_block))

            # Keep the power running
            if power.is_running:
                if power.name == "Laser":
                    power.run(UI_control=(mouse_pos, events))
                elif power.name == "Wishlist":
                    power.run(UI_control=(mouse_pos, events))

                if not power.is_running:  # If power.run() stopped the process
                    power_is_active = False
                    show_countdown = True

        if power.is_running and not power_is_active:
            # Player has turned off power, but power process is still runnning
            power.stop()

        # Block movement control
        if game_running:
            shadow_block = ShadowBlock(current_block, board)  # Update

            # For holding down keys
            key_timer += 1

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
                            current_block.move(board, 0, 1, autofall=True)
                        current_block.playSound(MOVE_SOUND)

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
                current_score = score_counter.drop()
            elif right_pressed and key_timer % 10 == 0:
                shadow_block.clearShadow(board)  # Player movement = Delete shadow block on last position
                current_block.move(board, 1, 0)
            elif left_pressed and key_timer % 10 == 0:
                shadow_block.clearShadow(board)
                current_block.move(board, -1, 0)

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
                    if solved_rows >= stage * 5 and optionsValues("stages"):
                        stage += 1
                        fall_speed *= 0.9

                    # Sound effect if at least one row is cleared
                    current_block.playSound(ROW_CLEARED_SOUND)

        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)

        updateBoard(board)
        updateNextBlockArea(next_block_area)
        updateScore(current_score, high_score, stage)
        updatePowersSelection(power)
        updateGameButtons()

        if game_over:
            updateGameOverScreen()
        elif power_is_active:
            if power.name == "Laser":
                laserScreen(power.row)
            elif power.name == "Wishlist":
                wishlistScreen(power.block_under_cursor)

            drawObject(CANCEL_POWER_BTN, CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
        elif show_countdown:
            TICK_SOUND.play()
            showCountdownToResumeGame(countdown)
            countdown -= 1

            if countdown < 1:
                RESUME_SOUND.play()
                show_countdown = False
                game_running = True
                countdown = 3  # Reset countdown
        elif not game_running:
            updatePauseMenu()

        pygame.display.update()


# Main menu
def main_menu():
    # Button positions
    start_button = (START_BTN_X, START_BTN_Y)  # New game
    options_button = (OPTIONS_BTN_X, OPTIONS_BTN_Y)  # Options
    quit_button = (QUIT_BTN_X, QUIT_BTN_Y)  # Quit program


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
                    if clickBox(mouse_pos, start_button, BTN_CORNER_RAD):
                        run = False  # Stop main menu process
                        startNewGame()
                    elif clickBox(mouse_pos, options_button, BTN_CORNER_RAD):
                        run = False  # Stop main menu process
                        options()
                    elif clickBox(mouse_pos, quit_button, BTN_CORNER_RAD):
                        closeProgram()

# Options menu
def options():
    # Buttons and switches positions
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    sound_switch = (SOUND_SWITCH_X, SOUND_SWITCH_Y)
    stages_switch = (STAGES_SWITCH_X, STAGES_SWITCH_Y)
    block_shadows_switch = (BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    power_ups_switch = (POWER_UPS_SWITCH_X, POWER_UPS_SWITCH_Y)

    run = True
    while run:
        # UI control
        mouse_pos = pygame.mouse.get_pos()

        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        updateOptionsMenu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clickBox(mouse_pos, back_button, BTN_CORNER_RAD):
                        run = False
                        main_menu()
                    elif clickBox(mouse_pos, sound_switch, SWITCH_CORNER_RAD):
                        optionsValues("sound", True)  # Second parameter changes value
                    elif clickBox(mouse_pos, stages_switch, SWITCH_CORNER_RAD):
                        optionsValues("stages", True)
                    elif clickBox(mouse_pos, block_shadows_switch, SWITCH_CORNER_RAD):
                        optionsValues("block_shadows", True)
                    elif clickBox(mouse_pos, power_ups_switch, SWITCH_CORNER_RAD):
                        optionsValues("power_ups", True)

main_menu()  # Launch main menu when program is opened
