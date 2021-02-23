import pygame
import sys
from board import *
from nextblock import *
from blocks import *
from screen import *
from database import *
from powers import *

# INITIALIZE
pygame.init()
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Tetris")


# GENERAL FUNCTIONS
def closeProgram():
    closeDB()
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
    if (optionsValues("power_ups")):
        high_score = getStat("high_score_powers")
    else:
        high_score = getStat("high_score")

    power = Power()

    # Variables for stats
    blocks_created = 0
    timer = 0
    seconds_in_game = 0

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
                # STATS
                if (optionsValues("power_ups")):
                    saveStat("high_score_powers", current_score, compare=1)
                else:
                    saveStat("high_score", current_score, compare=1)

                saveStat("highest_stage", stage, compare=1)
                saveStat("rows", solved_rows)
                saveStat("blocks_created", blocks_created)
                saveStat("time_ingame", seconds_in_game)
                saveStat("games_played", 1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_is_over and not countdown_is_active and not power_is_active:
                        if game_is_running:  # Pause game
                            game_is_running = False
                        else:  # Unpause
                            countdown_is_active = True

                if event.key == pygame.K_p:
                    if power.is_running:
                        power_is_active = False
                        countdown_is_active = True
                    elif power.is_available and game_is_running:
                        power_is_active = True
                        game_is_running = False

            # Buttons clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not power_is_active and not countdown_is_active:
                    if clickBox(mouse_pos, end_button):
                        # End game and go to the main menu
                        run = False  # Stop game process
                        main_menu()

                if power_is_active:
                    if clickBox(mouse_pos, cancel_power_button):
                        power_is_active = False
                        countdown_is_active = True

                if game_is_over:
                    if clickBox(mouse_pos, new_game_button):
                        # Run following code only if game is over
                        # new_game_button is shown when game is over
                        # new_game_button is at the same place, where pause/unpause button (click areas overlap)

                        # Start new game
                        run = False  # End current game process
                        startNewGame()
                elif game_is_running:
                    if clickBox(mouse_pos, pause_button):
                        game_is_running = False
                    if clickBox(mouse_pos, activate_power_button):
                        if power.is_available:
                            power_is_active = True
                            game_is_running = False
                elif not game_is_running and not power_is_active:
                    if clickBox(mouse_pos, pause_button):
                        # Unpause the game
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

            # Measure time spent in game (for stats)
            timer += 1
            if (timer / FPS) == 1:
                timer = 0
                seconds_in_game += 1

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
                            current_score = score_counter.drop(2)
                            current_block.move(board, y_step=1, autofall=True)
                        playSound(MOVE_SOUND)
                        saveStat("hard_drops", 1)

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
                current_score = score_counter.drop(1)
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

                # Is row cleared?
                if full_rows:
                    # Give points for cleared rows
                    if perfectClear(board):
                        current_score = score_counter.perfectClear(stage, full_rows)
                    else:
                        current_score = score_counter.fullRow(stage, full_rows)

                    # Check current stage
                    solved_rows += full_rows
                    if solved_rows >= stage * 5 and optionsValues("stages"):
                        stage += 1
                        fall_speed *= 0.9

                    # Sound effect if at least one row is cleared
                    playSound(ROW_CLEARED_SOUND)
                    
                current_block = Block(next_block, board)
                blocks_created += 1
                next_block = getNextBlock(batch.getBlock(), next_block_area)

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

            drawObject(CANCEL_POWER_BTN, CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
        elif countdown_is_active:
            showCountdown(countdown)
            countdown, countdown_is_active, game_is_running = runCountdown(countdown)
        elif not game_is_running:
            showPauseMenu()

        pygame.display.update()


def runCountdown(countdown):
    countdown -= 1

    if countdown < 1:
        playSound(RESUME_SOUND)
        countdown_is_active = False
        game_is_running = True
        countdown = 3  # Reset countdown
    else:
        playSound(TICK_SOUND)
        countdown_is_active = True
        game_is_running = False

    return (countdown, countdown_is_active, game_is_running)


# MAIN MENU
def main_menu():
    # Button positions
    start_button = (START_BTN_X, START_BTN_Y)  # New game
    options_button = (OPTIONS_BTN_X, OPTIONS_BTN_Y)  # Options
    stats_button = (STATS_BTN_X, STATS_BTN_Y)  # Stats
    trophies_button = (TROPHIES_BTN_X, TROPHIES_BTN_Y)
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
                    if clickBox(mouse_pos, start_button):
                        run = False  # Stop main menu process
                        startNewGame()
                    elif clickBox(mouse_pos, options_button):
                        run = False  # Stop main menu process
                        options()
                    elif clickBox(mouse_pos, stats_button):
                        run = False  # Stop main menu proccess
                        stats()
                    elif clickBox(mouse_pos, trophies_button):
                        run = False  # Stop main menu process
                        trophies()
                    elif clickBox(mouse_pos, quit_button):
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
        showOptionsMenu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clickBox(mouse_pos, back_button):
                        run = False
                        main_menu()
                    elif clickBox(mouse_pos, sound_switch, switch=True):
                        optionsValues("sound", True)  # Second parameter changes value
                    elif clickBox(mouse_pos, stages_switch, switch=True):
                        optionsValues("stages", True)
                    elif clickBox(mouse_pos, block_shadows_switch, switch=True):
                        optionsValues("block_shadows", True)
                    elif clickBox(mouse_pos, power_ups_switch, switch=True):
                        optionsValues("power_ups", True)


# Stats menu
def stats(page=1):
    # Buttons and switches positions
    back_button = [BACK_BTN_X, BACK_BTN_Y]
    previous_button = [PREVIOUS_BTN_X, PREVIOUS_BTN_Y]
    next_button = [NEXT_BTN_X, NEXT_BTN_Y]

    STATS_VALUES = updateStats()

    run = True
    while run:
        # UI control
        mouse_pos = pygame.mouse.get_pos()
        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        showStatsMenu(page)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clickBox(mouse_pos, back_button):
                        run = False  # Stop main menu proccess
                        main_menu()
                    elif clickBox(mouse_pos, previous_button) and page != 1:
                        page -= 1
                    elif clickBox(mouse_pos, next_button) and page != len(STATS_VALUES):
                        # Cant go higher than last page
                        page += 1


def trophies():
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    previous_button = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    next_button = (NEXT_BTN_X, NEXT_BTN_Y)
    page = 1
    run = True
    while run:
        # UI control
        mouse_pos = pygame.mouse.get_pos()

        # Update screen
        CLOCK.tick(FPS)
        SCREEN.fill(DARK_GREY)
        showTrophiesScreen(page)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clickBox(mouse_pos, back_button):
                        run = False
                        main_menu()
                    if clickBox(mouse_pos, previous_button) and page != 1:
                        page -= 1
                    if clickBox(mouse_pos, next_button) and page != len(TROPHIES):
                        page += 1


main_menu()  # Launch main menu when program is opened
