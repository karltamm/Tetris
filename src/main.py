import pygame
import sys
from board import *
from nextblock import *
from blocks import *
from screen import *
from database import *
from powers import *
from animations import TetrisRain
from themes import *

# INITIALIZE
pygame.init()
pygame.display.set_caption("Tetris")
pygame.display.set_icon(CLASSIC_BLUE_CELL)
fps_controller = FPSController()


# GENERAL FUNCTIONS
def closeProgram():
    closeDB()
    pygame.quit()
    sys.exit()


# GAME
def runGame(load_game=False):
    # Game states
    game_is_running = True
    game_is_paused = False
    game_is_over = False
    power_is_active = False
    game_is_being_saved = False
    resume_game_if_saved = False

    # Countdown
    countdown_is_active = False
    countdown = 3

    # UI
    activate_power_button = (ACTIVATE_POWER_BTN_X, ACTIVATE_POWER_BTN_Y)
    cancel_power_button = (CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
    pause_button = (PAUSE_BTN_X, PAUSE_BTN_Y)
    save_button = (SAVE_BTN_X, SAVE_BTN_Y)
    end_button = (END_BTN_X, END_BTN_Y)  # End game
    new_game_button = (NEW_GAME_BTN_X, NEW_GAME_BTN_Y)  # If game is over, this button will be shown

    GAME_RUNNING_BTNS = (activate_power_button, pause_button, save_button, end_button)
    PAUSE_MENU_BTNS = (pause_button, save_button, end_button)
    GAME_IS_OVER_BTNS = (new_game_button, end_button)

    selected_button = None
    mouse_btn_is_held_down = False

    theme = Theme(optionsValues("theme"))

    # Get game ready
    powers_are_enabled = optionsValues("powers")
    next_block_area = createNextBlockArea()

    if load_game:
        board = SAVED_GAME_DB["board"]
        blocks_batch = SAVED_GAME_DB["blocks_batch"]
        current_block = SAVED_GAME_DB["current_block"]
        rewindCurrentBlock(current_block, board)
        next_block = SAVED_GAME_DB["next_block"]
        NextBlock(next_block, next_block_area)

        current_score = SAVED_GAME_DB["current_score"]
        solved_rows = SAVED_GAME_DB["solved_rows"]
        stage = SAVED_GAME_DB["stage"]

        power = SAVED_GAME_DB["power"]
        powers_batch = SAVED_GAME_DB["powers_batch"]
    else:
        # Initialize new game
        board = createBoard()
        blocks_batch = BlocksBatch()
        current_block = Block(blocks_batch.getBlock(), board)
        next_block = getNextBlock(blocks_batch.getBlock(), next_block_area)

        stage = 1
        solved_rows = 0
        current_score = 0

        powers_batch = PowersBatch()
        power = powers_batch.getPower()
        power.is_available = False  # Player has to clear rows to earn power

    score_counter = Score(current_score)
    if optionsValues("powers"):
        high_score = getStat("high_score_powers")
    else:
        high_score = getStat("high_score")

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
    fall_speed = 0.6  # Every X second trigger block autofall
    autofall_failed = 0  # Nr of failed autofall attempts

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
                # Play game over sound
                if theme.name == "XP":
                    playSound(XP_GAME_OVER_SOUND)
                elif theme.name == "Yin-Yang":
                    playSound(YIN_YANG_GAME_OVER_SOUND)
                else:
                    playSound(GAME_OVER_SOUND)

                game_is_running = False
                game_is_over = True

                SAVED_GAME_DB["save_exsists"] = False  # Previous game save can't be used as a checkpoint

                # Update stats
                if optionsValues("powers"):
                    saveStat("high_score_powers", current_score, compare=1)
                else:
                    saveStat("high_score", current_score, compare=1)

                saveStat("highest_stage", stage, compare=1)
                saveStat("rows", solved_rows)
                saveStat("blocks_created", blocks_created)
                saveStat("time_ingame", seconds_in_game)
                saveStat("games_played", 1)
                saveStat("single_game_rows", solved_rows, compare=1)
                saveStat("single_game_time_ingame", seconds_in_game, compare=1)
                unlockedTrophies()

            # Using keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_is_over and not countdown_is_active and not power_is_active:
                        if game_is_running:  # Pause game
                            game_is_running = False
                            game_is_paused = True
                        else:  # Unpause
                            game_is_paused = False
                            countdown_is_active = True

                if event.key == pygame.K_p:
                    if power_is_active:  # Deactivate power
                        power_is_active = False
                        countdown_is_active = True
                    elif powers_are_enabled and power.is_available and game_is_running:  # Activate power
                        power_is_active = True
                        game_is_running = False

                if event.key == pygame.K_s:
                    if not power_is_active and not game_is_over:
                        # Save game
                        if game_is_running:
                            game_is_being_saved = True
                            resume_game_if_saved = True
                            game_is_running = False
                        else:
                            game_is_being_saved = True

                if event.key == pygame.K_e:
                    # End game and go to the main menu
                    run = False  # Stop game process
                    launchMainMenu()

                if event.key == pygame.K_n and game_is_over:
                    # Start a new game
                    run = False  # End current game process
                    runGame()

            # Using mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if (game_is_running and not power_is_active) or game_is_over or game_is_paused:
                    if clickBox(end_button):
                        # End game and go to the main menu
                        run = False  # Stop game process
                        launchMainMenu()

                if power_is_active:
                    if clickBox(cancel_power_button):
                        power_is_active = False
                        countdown_is_active = True
                elif game_is_running:
                    if clickBox(pause_button):
                        game_is_running = False
                        game_is_paused = True
                    elif clickBox(activate_power_button):
                        if powers_are_enabled and power.is_available:
                            power_is_active = True
                            game_is_running = False
                    elif clickBox(save_button):
                        game_is_being_saved = True
                        resume_game_if_saved = True
                        game_is_running = False
                elif game_is_paused:
                    if clickBox(pause_button):
                        game_is_paused = False
                        countdown_is_active = True
                    elif clickBox(save_button):
                        game_is_being_saved = True
                        game_is_running = False
                elif game_is_over:
                    if clickBox(new_game_button):
                        run = False  # End current game process
                        runGame()

        # On which button is the cursor? (to determine button hover and clicked state)
        if game_is_running:
            for index, button in enumerate(GAME_RUNNING_BTNS):
                if clickBox(button):
                    if button == activate_power_button and not power.is_available:
                        break  # "Activate power" button is not available, so don't higlight it

                    selected_button = button
                    break  # Found the button; job done

                if index == len(GAME_RUNNING_BTNS) - 1:  # Cursor wasn't on any button
                    selected_button = None

        if game_is_paused:
            for index, button in enumerate(PAUSE_MENU_BTNS):
                if clickBox(button):
                    selected_button = button
                    break  # Found the button; job done

                if index == len(PAUSE_MENU_BTNS) - 1:  # Cursor wasn't on any button
                    selected_button = None

        if game_is_over:
            for index, button in enumerate(GAME_IS_OVER_BTNS):
                if clickBox(button):
                    selected_button = button
                    break  # Found the button; job done

                if index == len(GAME_IS_OVER_BTNS) - 1:
                    selected_button = None  # Cursor wasn't on any button

        if power_is_active:
            if clickBox(cancel_power_button):
                selected_button = cancel_power_button
            else:
                selected_button = None  # Cursor wasn't on any button

        if countdown_is_active:
            selected_button = None  # During countdown, no button is highlighted

        # Powers
        if powers_are_enabled:
            if power_is_active and not power.is_running:
                power.start(board_params=(board, current_block, shadow_block))

                if power.game_should_run:
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
                    power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down = \
                        resumeGameAfterPower()

                # If player has turned off power
                if not power_is_active:
                    power.stop()
                    power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down = \
                        resumeGameAfterPower()

            if powers_batch.itsTimeForNextPower(solved_rows):
                if not power.is_available:  # Only give new power when last one is used
                    power = powers_batch.getPower()

        # Saving a game
        if game_is_being_saved:
            SAVED_GAME_DB["save_exsists"] = True

            shadow_block.clearShadow(board)  # To avoid glitches
            SAVED_GAME_DB["board"] = board
            shadow_block = ShadowBlock(current_block, board)  # Restore the shadow

            SAVED_GAME_DB["current_block"] = current_block
            SAVED_GAME_DB["next_block"] = next_block
            SAVED_GAME_DB["blocks_batch"] = blocks_batch

            SAVED_GAME_DB["current_score"] = current_score
            SAVED_GAME_DB["solved_rows"] = solved_rows
            SAVED_GAME_DB["stage"] = stage

            SAVED_GAME_DB["power"] = power
            SAVED_GAME_DB["powers_batch"] = powers_batch

        # Block movement control
        if game_is_running:
            shadow_block = ShadowBlock(current_block, board)  # Update shadow block on the screen

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
                        if not current_block.move(board, y_step=1, autofall=True):
                            autofall_failed += 1

            # Check if user wants to move a block
            for event in events:
                if event.type == pygame.MOUSEMOTION:  # If mouse movement detected
                    if isMouseOnGameBoard(mouse_pos):  # Is mouse on game board
                        if current_block.movedToCursor(board, mouse_pos):  # Return True if block moved to cursor
                            shadow_block.clearShadow(board)
                            shadow_block = ShadowBlock(current_block, board)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if isMouseOnGameBoard(mouse_pos):  # Check if mouse clicked on game board
                        if event.button == 1:  # Left click hard drops block
                            while not current_block.is_placed:
                                current_score = score_counter.drop(2)
                                current_block.move(board, y_step=1, autofall=True)
                            playSound(MOVE_SOUND)
                            saveStat("hard_drops", 1)
                        elif event.button == 3:  # Right click rotates block
                            current_block.rotate(board)
                            if current_block.movedToCursor(board, mouse_pos):  # Move block to cursor after rotation
                                shadow_block.clearShadow(board)

                elif event.type == pygame.KEYDOWN:  # If a key is pressed down
                    key_timer = 0
                    if event.key == pygame.K_UP:
                        if current_block.shape != SHAPE_O:
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
            if down_pressed and key_timer % 4 == 0 and not current_block.is_placed:
                if current_block.move(board, y_step=1):  # if move successful
                    fall_timer = 0
                    if current_block.y >= current_block.lowest_y:
                        current_block.lowest_y = current_block.y + 1
                        current_score = score_counter.drop(1)  # Give points for faster drops

            elif right_pressed and key_timer % 10 == 0:
                if current_block.move(board, x_step=1):  # If move unsuccessful shadow won't flicker
                    shadow_block.clearShadow(board)  # Player movement = Delete shadow block on last position

            elif left_pressed and key_timer % 10 == 0:
                if current_block.move(board, x_step=-1):
                    shadow_block.clearShadow(board)

            # Is current block placed?
            if current_block.is_placed:
                # If block hasn't been moved in 300 ms or autofall has failed 8 times
                if (pygame.time.get_ticks() - current_block.time_since_movement) > 300 or autofall_failed >= 8:
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
                            fall_speed *= 0.97

                        # Sound effect if at least one row is cleared
                        playSound(ROW_CLEARED_SOUND)

                    if isMouseOnGameBoard(mouse_pos):
                        current_block = Block(next_block, board, getPosOnMouse(mouse_pos, next_block))
                    else:
                        current_block = Block(next_block, board)
                    blocks_created += 1
                    autofall_failed = 0
                    next_block = getNextBlock(blocks_batch.getBlock(), next_block_area)

        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        showBoard(board, theme)
        showNextBlockArea(next_block_area, theme)
        showScore(current_score, high_score, stage)
        showPowersSelection(powers_are_enabled, power)
        showGameButtons()

        if game_is_over:
            showGameOverScreen(theme)
        elif power_is_active:
            if power.name == "Laser":
                showLaserScreen(power.row, theme)
            elif power.name == "Wishlist":
                showWishlistScreen(power.block_under_cursor, theme)
            elif power.name == "Timeless":
                showTimelessScreen(power.num_of_blocks_left)
                showNextBlockArea(next_block_area, theme)

            drawObject(CANCEL_POWER_BTN, CANCEL_POWER_BTN_X, CANCEL_POWER_BTN_Y)
        elif countdown_is_active:
            showCountdown(countdown)
            countdown, countdown_is_active, game_is_running = runCountdown(countdown)
            game_is_being_saved = False  # If user tries to save game during countdown, ignore it
        elif game_is_being_saved:
            playSound(GAME_SAVE_SOUND)
            showSaveConfirmation(resume_game_if_saved)

            if resume_game_if_saved:
                countdown_is_active = True
                resume_game_if_saved = False

            game_is_being_saved = False
        elif game_is_paused:
            showPauseMenu()

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

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

    return countdown, countdown_is_active, game_is_running


def resumeGameAfterPower():
    power_is_active = False
    game_is_running = False  # Some powers need game to run
    down_pressed = False  # If game ran, then this variable may cause glitch
    countdown_is_active = True
    mouse_btn_is_held_down = False  # Causes UI glitch if not reset

    return power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down


# MAIN MENU
def launchMainMenu(tetris_rain=TetrisRain()):
    # UI
    start_button = (START_BTN_X, START_BTN_Y)  # New game
    continue_button = (CONTINUE_BTN_X, CONTINUE_BTN_Y)  # Load previously saved game
    shortcuts_button = (SHORTCUTS_BTN_X, SHORTCUTS_BTN_Y)
    options_button = (OPTIONS_BTN_X, OPTIONS_BTN_Y)
    stats_button = (STATS_BTN_X, STATS_BTN_Y)
    trophies_button = (TROPHIES_BTN_X, TROPHIES_BTN_Y)
    themes_button = (THEMES_BTN_X, THEMES_BTN_Y)
    quit_button = (QUIT_BTN_X, QUIT_BTN_Y)

    game_is_saved = checkIfGameIsSaved()

    # Navigation
    MENU_BUTTONS = (
        start_button, continue_button, shortcuts_button, options_button, stats_button, trophies_button, themes_button,
        quit_button)
    BUTTON_ACTIONS = (runGame, runGame, shortcuts, options, stats, trophies, themes, closeProgram)
    selected_index = 0
    mouse_btn_is_held_down = False

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showMainMenu(game_is_saved)
        selected_button = MENU_BUTTONS[selected_index]

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clickBox(selected_button):
                    mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(start_button):
                    run = False  # Stop main menu process
                    runGame()
                elif clickBox(continue_button) and game_is_saved:
                    run = False  # Stop main menu process
                    runGame(game_is_saved)
                elif clickBox(shortcuts_button):
                    run = False  # Stop main menu process
                    shortcuts(tetris_rain)
                elif clickBox(options_button):
                    run = False  # Stop main menu process
                    options(tetris_rain)
                elif clickBox(stats_button):
                    run = False  # Stop main menu proccess
                    stats(tetris_rain)
                elif clickBox(trophies_button):
                    run = False  # Stop main menu process
                    trophies(tetris_rain)
                elif clickBox(themes_button):
                    run = False  # Stop main menu process
                    themes(tetris_rain)
                elif clickBox(quit_button):
                    closeProgram()

            # Mouse navigation
            if event.type == pygame.MOUSEMOTION:
                for index, btn in enumerate(MENU_BUTTONS):
                    if clickBox(btn):
                        if index == 1 and not game_is_saved:
                            break
                        else:
                            selected_index = index

            # Keyboard navigation
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if not (selected_index == len(MENU_BUTTONS) - 1):
                        selected_index += 1

                        if selected_index == 1 and not game_is_saved:
                            selected_index += 1  # Skip "Continue" button if there is no game save

                        selected_button = MENU_BUTTONS[selected_index]
                elif event.key == pygame.K_UP:
                    if not (selected_index == 0):
                        selected_index -= 1

                        if selected_index == 1 and not game_is_saved:
                            selected_index -= 1  # Skip "Continue" button if there is no game save

                        selected_button = MENU_BUTTONS[selected_index]
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Key highlight effect on select btn hold down
                    mouse_btn_is_held_down = True

            elif event.type == pygame.KEYUP:  # Go to selection on key release
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    run = False
                    if selected_index == 1:
                        BUTTON_ACTIONS[selected_index](game_is_saved)
                    elif 1 < selected_index < 7:
                        BUTTON_ACTIONS[selected_index](tetris_rain)
                    else:
                        BUTTON_ACTIONS[selected_index]()


# Shortcuts menu
def shortcuts(tetris_rain):
    # UI
    BACK_BTN = (BACK_BTN_X, BACK_BTN_Y)
    NEXT_BTN = (NEXT_BTN_X, NEXT_BTN_Y)
    PREV_BTN = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)

    # Navigation
    ALL_BTNS = (BACK_BTN, NEXT_BTN, PREV_BTN)
    selected_index = 0
    mouse_btn_is_held_down = False
    page = 1
    MAX_PAGES = 2

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showShortcutsMenu(page, MAX_PAGES)

        selected_btn = ALL_BTNS[selected_index]
        if mouse_btn_is_held_down:
            activateButtonClickState(selected_btn)
        else:
            activateButtonHoverState(selected_btn)

        pygame.display.update()

        # UI control
        # On which button is the cursor?
        if clickBox(BACK_BTN):
            selected_index = 0
        elif clickBox(NEXT_BTN) and page < 2:
            selected_index = 1
        elif clickBox(PREV_BTN) and page > 1:
            selected_index = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clickBox(selected_btn):
                    mouse_btn_is_held_down = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False

                if clickBox(BACK_BTN):
                    run = False
                    launchMainMenu(tetris_rain)
                elif clickBox(NEXT_BTN) and page < 2:
                    page += 1
                    if page == MAX_PAGES:
                        selected_index = 2  # Select "Previous" button, because "Next" is now inactive
                elif clickBox(PREV_BTN) and page > 1:
                    page -= 1
                    if page < 2:
                        selected_index = 1  # Select "Next" button, because "Previous" is now inactive


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu(tetris_rain)

                elif event.key == pygame.K_UP:
                    selected_index = 0  # "Back" button

                elif event.key == pygame.K_DOWN:
                    if page < MAX_PAGES:
                        selected_index = 1  # "Next" button
                    else:
                        selected_index = 2  # "Previous" button

                elif event.key == pygame.K_RIGHT and page < MAX_PAGES:
                    selected_index = 1  # "Next" button

                elif event.key == pygame.K_LEFT and page > 1:
                    selected_index = 2  # "Previous" button

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = True

            elif event.type == pygame.KEYUP:
                mouse_btn_is_held_down = False

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_index == 0:  # "Back" button
                        run = False
                        launchMainMenu(tetris_rain)

                    elif selected_index == 1:  # "Next" button
                        page += 1
                        if page == MAX_PAGES:
                            selected_index = 2  # Select "Previous" button, because "Next" is now inactive

                    elif selected_index == 2:  # "Previous" button
                        page -= 1
                        if page < 2:
                            selected_index = 1  # Select "Next" button, because "Previous" is now inactive


# Options menu
def options(tetris_rain):
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    music_slider = (MUSIC_SLIDER_BG_X, MUSIC_SLIDER_BG_Y)
    sound_slider = (SOUND_SLIDER_BG_X, SOUND_SLIDER_BG_Y)
    stages_switch = (STAGES_SWITCH_X, STAGES_SWITCH_Y)
    block_shadows_switch = (BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    powers_switch = (POWERS_SWITCH_X, POWERS_SWITCH_Y)

    MENU_BUTTONS = (back_button, music_slider, sound_slider, stages_switch, block_shadows_switch, powers_switch)
    selected_index = 0
    mouse_btn_is_held_down = False
    vol_change = False

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showOptionsMenu()
        selected_button = MENU_BUTTONS[selected_index]

        if selected_index != 0:
            mouse_btn_is_held_down = False

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            if selected_index > 2:
                activateSwitchHoverState(selected_button)
            elif selected_index > 0:
                activateSliderHoverState(selected_button)
            else:
                activateButtonHoverState(selected_button)

        if vol_change:
            if selected_index == 1:
                regulateSliderKeyboard("music", vol_amount, tetris_rain)
            elif selected_index == 2:
                regulateSliderKeyboard("sound", vol_amount, tetris_rain)

        pygame.display.update()

        # UI control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEMOTION:
                for index, btn in enumerate(MENU_BUTTONS):
                    if clickBox(btn):
                        selected_index = index

                # Check if mouse in on slider dragger
                if clickBox(getMusicDraggerPos()):
                    selected_index = 1
                elif clickBox(getSoundDraggerPos()):
                    selected_index = 2

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clickBox(back_button):
                    mouse_btn_is_held_down = True
                if clickBox(music_slider, element=2, slider_value="music"):  # Slider
                    regulateSlider("music", MUSIC_DRAGGER_X, tetris_rain)
                    musicControl(change_volume=True)
                if clickBox(sound_slider, element=2, slider_value="sound"):  # Slider
                    regulateSlider("sound", SOUND_DRAGGER_X, tetris_rain)
                    playSound(MOVE3_SOUND)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False
                    launchMainMenu(tetris_rain)
                elif clickBox(stages_switch, element=1):
                    optionsValues("stages", invert=True)
                elif clickBox(block_shadows_switch, element=1):
                    optionsValues("block_shadows", invert=True)
                elif clickBox(powers_switch, element=1):
                    optionsValues("powers", invert=True)

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu(tetris_rain)
                elif event.key == pygame.K_DOWN and selected_index != len(MENU_BUTTONS) - 1:
                    selected_index += 1
                elif event.key == pygame.K_UP and selected_index != 0:
                    selected_index -= 1
                elif event.key == pygame.K_LEFT:
                    vol_change = True
                    vol_amount = -0.01
                elif event.key == pygame.K_RIGHT:
                    vol_change = True
                    vol_amount = 0.01
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        mouse_btn_is_held_down = True
                    elif selected_index == 3:
                        optionsValues("stages", invert=True)
                    elif selected_index == 4:
                        optionsValues("block_shadows", invert=True)
                    elif selected_index == 5:
                        optionsValues("powers", invert=True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    vol_change = False
                    if selected_index == 2:
                        playSound(MOVE3_SOUND)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = False
                    if selected_index == 0:
                        run = False
                        launchMainMenu(tetris_rain)


def regulateSlider(slider, dragger_x, bg_animation):
    value = optionsValues(slider)
    x_dif = pygame.mouse.get_pos()[0] - (
            dragger_x + (SLIDING_DISTANCE * value))  # distance between mouse_x and dragger_x

    while pygame.mouse.get_pressed(3)[0]:  # Updates slider until button released
        fps_controller.keepFrameDurationCorrect()
        SCREEN.fill(DARK_GREY)
        bg_animation.makeItRain()
        showOptionsMenu()
        pygame.display.update()

        event = pygame.event.poll()
        if event.type == pygame.QUIT:  # Be ready to close the programm
            closeProgram()

        dragger_pos = pygame.mouse.get_pos()[0] - x_dif  # dragger pos relative to mouse pos
        if dragger_x < dragger_pos < (dragger_x + SLIDING_DISTANCE):
            value = round((dragger_pos - dragger_x) / SLIDING_DISTANCE, 2)
        elif dragger_pos <= dragger_x:
            value = 0
        elif dragger_pos >= dragger_x + SLIDING_DISTANCE:
            value = 1
        if slider == "music":
            musicControl(change_volume=True)
        optionsValues(slider, new_value=value)


def regulateSliderKeyboard(slider, vol_change, bg_animation):
    value = optionsValues(slider)

    value += vol_change
    if value < 0:
        value = 0
    elif value > 1:
        value = 1
    if slider == "music":
        musicControl(change_volume=True)
    optionsValues(slider, new_value=value)


# Stats menu
def stats(tetris_rain, page=1):
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    previous_button = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    next_button = (NEXT_BTN_X, NEXT_BTN_Y)
    STATS_VALUES = updateStats()

    # Navigation
    MENU_BUTTONS = (back_button, previous_button, next_button)
    selected_index = 0
    mouse_btn_is_held_down = False

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showStatsMenu(page)
        selected_button = MENU_BUTTONS[selected_index]

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        # On which button is the cursor?
        if clickBox(back_button):
            selected_index = 0  # Back btn
        elif clickBox(previous_button) and page != 1:
            selected_index = 1  # Previous page
        elif clickBox(next_button) and page != len(STATS_VALUES):
            selected_index = 2  # Next page

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clickBox(selected_button):
                    mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False  # Stop main menu proccess
                    launchMainMenu(tetris_rain)
                elif clickBox(previous_button) and page != 1:
                    page -= 1
                    if page == 1:
                        selected_index = 2
                elif clickBox(next_button) and page != len(STATS_VALUES):
                    # Cant go higher than last page
                    page += 1
                    if page == len(STATS_VALUES):
                        selected_index = 1

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu(tetris_rain)
                elif event.key == pygame.K_UP:
                    selected_index = 0
                elif event.key == pygame.K_DOWN:
                    if page != 1:
                        selected_index = 1
                    else:
                        selected_index = 2
                elif event.key == pygame.K_RIGHT and page != len(STATS_VALUES):
                    selected_index = 2
                elif event.key == pygame.K_LEFT and page != 1:
                    selected_index = 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = False
                    if selected_index == 0:
                        run = False
                        launchMainMenu(tetris_rain)
                    elif selected_index == 1:
                        page -= 1
                        if page == 1:
                            selected_index += 1
                    elif selected_index == 2:
                        page += 1
                        if page == len(STATS_VALUES):
                            selected_index -= 1


def trophies(tetris_rain):
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    previous_button = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    next_button = (NEXT_BTN_X, NEXT_BTN_Y)

    # Navigation
    MENU_BUTTONS = (back_button, previous_button, next_button)
    selected_index = 0
    mouse_btn_is_held_down = False

    page = 1

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showTrophiesScreen(page)
        selected_button = MENU_BUTTONS[selected_index]

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        # On which button is the cursor?
        if clickBox(back_button):
            selected_index = 0  # Back btn
        elif clickBox(previous_button) and page != 1:
            selected_index = 1  # Previous page
        elif clickBox(next_button) and page != len(TROPHIES):
            selected_index = 2  # Next page

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clickBox(selected_button):
                    mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False
                    launchMainMenu(tetris_rain)
                if clickBox(previous_button) and page != 1:
                    page -= 1
                    if page == 1:
                        selected_index = 2
                if clickBox(next_button) and page != len(TROPHIES):
                    page += 1
                    if page == len(TROPHIES):
                        selected_index = 1

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu(tetris_rain)
                elif event.key == pygame.K_UP:
                    selected_index = 0
                elif event.key == pygame.K_DOWN:
                    if page != 1:
                        selected_index = 1
                    else:
                        selected_index = 2
                elif event.key == pygame.K_RIGHT and page != len(TROPHIES):
                    selected_index = 2
                elif event.key == pygame.K_LEFT and page != 1:
                    selected_index = 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mouse_btn_is_held_down = False
                    if selected_index == 0:
                        run = False
                        launchMainMenu(tetris_rain)
                    elif selected_index == 1:
                        page -= 1
                        if page == 1:
                            selected_index += 1
                    elif selected_index == 2:
                        page += 1
                        if page == len(TROPHIES):
                            selected_index -= 1


# Themes menu
def themes(tetris_rain):
    # UI
    BACK_BTN = (BACK_BTN_X, BACK_BTN_Y)
    CLASSIC_BTN = themeButtonPos(0)
    YIN_YANG_BTN = themeButtonPos(1)
    XP_BTN = themeButtonPos(2)
    ALL_BTNS = (CLASSIC_BTN, YIN_YANG_BTN, XP_BTN, BACK_BTN)

    default_btn_active = True
    selected_index = 3
    selected_button = BACK_BTN

    mouse_btn_is_held_down = False
    mouse_was_clicked = False
    action_key_is_held_down = False

    themes_info = getThemesInfo()

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showThemesScreen(themes_info)

        if mouse_btn_is_held_down and not default_btn_active or action_key_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                mouse_was_clicked = True
                if clickBox(BACK_BTN):
                    run = False
                    launchMainMenu(tetris_rain)
                elif clickBox(CLASSIC_BTN):
                    if themes_info[0]["unlocked"] and not themes_info[0]["active"]:
                        optionsValues("theme", new_value=0)
                elif clickBox(YIN_YANG_BTN):
                    if themes_info[1]["unlocked"] and not themes_info[1]["active"]:
                        optionsValues("theme", new_value=1)
                elif clickBox(XP_BTN):
                    if themes_info[2]["unlocked"] and not themes_info[2]["active"]:
                        optionsValues("theme", new_value=2)
                themes_info = getThemesInfo()

            # Which button is selected/active? On which button is cursor?
            if event.type == pygame.MOUSEMOTION or mouse_was_clicked:
                mouse_was_clicked = False

                # Default active button
                selected_button = BACK_BTN
                selected_index = 3
                default_btn_active = True

                # On which button is cursor?
                for i, btn in enumerate(ALL_BTNS):
                    if clickBox(btn):
                        if i < 3:  # 3 theme buttons: index 0-2
                            if themes_info[i]["unlocked"] and not themes_info[i]["active"]:
                                selected_index = i
                                selected_button = ALL_BTNS[i]
                                default_btn_active = False
                                break
                        else:  # Back button
                            selected_index = i
                            selected_button = ALL_BTNS[i]
                            default_btn_active = False

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    theme_btn_selected = False
                    selected_index = (selected_index + 1) % 4

                    while selected_index < 3:
                        if themes_info[selected_index]["unlocked"] and not themes_info[selected_index]["active"]:
                            selected_button = ALL_BTNS[selected_index]
                            theme_btn_selected = True
                            break
                        selected_index += 1  # Increment to find suitable button

                    if not theme_btn_selected:
                        selected_button = BACK_BTN
                        selected_index = 3

                elif event.key == pygame.K_UP:
                    theme_btn_selected = False
                    selected_index -= 1

                    while selected_index > 0:
                        if themes_info[selected_index]["unlocked"] and not themes_info[selected_index]["active"]:
                            selected_button = ALL_BTNS[selected_index]
                            theme_btn_selected = True
                            break
                        selected_index -= 1  # Decrement to find suitable button

                    if not theme_btn_selected:
                        selected_button = BACK_BTN
                        selected_index = 3

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    action_key_is_held_down = True

            elif event.type == pygame.KEYUP:
                action_key_is_held_down = False

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_index < 3:
                        optionsValues("theme", new_value=selected_index)
                        themes_info = getThemesInfo()

                        # Default active button
                        selected_button = BACK_BTN
                        selected_index = 3
                    else:
                        run = False
                        launchMainMenu(tetris_rain)
                elif event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu(tetris_rain)


if __name__ == "__main__":
    musicControl()
    launchMainMenu()
