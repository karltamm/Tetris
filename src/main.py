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
                    power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down = resumeGameAfterPower()

                # If player has turned off power
                if not power_is_active:
                    power.stop()
                    power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down = resumeGameAfterPower()

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
                if (pygame.time.get_ticks() - current_block.time_since_rotation) > 100:  # Give time to rotate
                    fall_timer += 1
                    if fall_timer / FPS > fall_speed:
                        fall_timer = 0
                        if not down_pressed:
                            current_block.move(board, y_step=1, autofall=True)

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
                            shadow_block.clearShadow(board)
                            current_block.rotate(board)

                elif event.type == pygame.KEYDOWN:  # If a key is pressed down
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
                current_score = score_counter.drop(1)  # Give points for faster drops
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
                        fall_speed *= 0.97

                    # Sound effect if at least one row is cleared
                    playSound(ROW_CLEARED_SOUND)

                current_block = Block(next_block, board)
                blocks_created += 1
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

    return (countdown, countdown_is_active, game_is_running)


def resumeGameAfterPower():
    power_is_active = False
    game_is_running = False  # Some powers need game to run
    down_pressed = False  # If game ran, then this variable may cause glitch
    countdown_is_active = True
    mouse_btn_is_held_down = False  # Causes UI glitch if not reset

    return (power_is_active, game_is_running, down_pressed, countdown_is_active, mouse_btn_is_held_down)


# MAIN MENU
def launchMainMenu():
    # UI
    start_button = (START_BTN_X, START_BTN_Y)  # New game
    continue_button = (CONTINUE_BTN_X, CONTINUE_BTN_Y)  # Load previously saved game
    options_button = (OPTIONS_BTN_X, OPTIONS_BTN_Y)
    stats_button = (STATS_BTN_X, STATS_BTN_Y)
    trophies_button = (TROPHIES_BTN_X, TROPHIES_BTN_Y)
    themes_button = (THEMES_BTN_X, THEMES_BTN_Y)
    quit_button = (QUIT_BTN_X, QUIT_BTN_Y)

    tetris_rain = TetrisRain()  # Animation
    game_is_saved = checkIfGameIsSaved()

    # Navigation
    MENU_BUTTONS = (
        start_button, continue_button, options_button, stats_button, trophies_button, themes_button, quit_button)
    BUTTON_ACTIONS = (runGame, runGame, options, stats, trophies, themes, closeProgram)
    selected_index = 0
    selected_button = MENU_BUTTONS[selected_index]
    mouse_btn_is_held_down = False

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        tetris_rain.makeItRain()
        showMainMenu(game_is_saved)

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
                for button in MENU_BUTTONS:
                    if clickBox(button):
                        mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(start_button):
                    run = False  # Stop main menu process
                    runGame()
                elif clickBox(continue_button) and game_is_saved:
                    run = False  # Stop main menu process
                    runGame(game_is_saved)
                elif clickBox(options_button):
                    run = False  # Stop main menu process
                    options()
                elif clickBox(stats_button):
                    run = False  # Stop main menu proccess
                    stats()
                elif clickBox(trophies_button):
                    run = False  # Stop main menu process
                    trophies()
                elif clickBox(themes_button):
                    run = False  # Stop main menu process
                    themes()
                elif clickBox(quit_button):
                    closeProgram()

            # Mouse navigation
            if event.type == pygame.MOUSEMOTION:
                if clickBox(start_button):
                    selected_index = 0
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(continue_button) and game_is_saved:
                    selected_index = 1
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(options_button):
                    selected_index = 2
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(stats_button):
                    selected_index = 3
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(trophies_button):
                    selected_index = 4
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(themes_button):
                    selected_index = 5
                    selected_button = MENU_BUTTONS[selected_index]
                elif clickBox(quit_button):
                    selected_index = 6
                    selected_button = MENU_BUTTONS[selected_index]

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
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    run = False
                    if (selected_index == 1):
                        BUTTON_ACTIONS[selected_index](game_is_saved)
                    else:
                        BUTTON_ACTIONS[selected_index]()


# Options menu
def options():
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    music_slider = (MUSIC_SLIDER_BG_X, MUSIC_SLIDER_BG_Y)
    sound_slider = (SOUND_SLIDER_BG_X, SOUND_SLIDER_BG_Y)
    stages_switch = (STAGES_SWITCH_X, STAGES_SWITCH_Y)
    block_shadows_switch = (BLOCK_SHADOW_SWITCH_X, BLOCK_SHADOW_SWITCH_Y)
    powers_switch = (POWERS_SWITCH_X, POWERS_SWITCH_Y)

    selected_button = None
    mouse_btn_is_held_down = False

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        showOptionsMenu()

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEMOTION:
                if clickBox(back_button):
                    selected_button = back_button
                else:
                    selected_button = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True
                if clickBox(music_slider, element=2, slider_value="music"):  # Slider
                    regulateSlider("music", MUSIC_DRAGGER_X)
                    musicControl(change_volume=True)
                if clickBox(sound_slider, element=2, slider_value="sound"):  # Slider
                    regulateSlider("sound", SOUND_DRAGGER_X)
                    playSound(MOVE3_SOUND)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False
                    launchMainMenu()
                elif clickBox(stages_switch, element=1):
                    optionsValues("stages", invert=True)
                elif clickBox(block_shadows_switch, element=1):
                    optionsValues("block_shadows", invert=True)
                elif clickBox(powers_switch, element=1):
                    optionsValues("powers", invert=True)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu()


def regulateSlider(slider, dragger_x):
    value = optionsValues(slider)
    x_dif = pygame.mouse.get_pos()[0] - (
            dragger_x + (SLIDING_DISTANCE * value))  # distance between mouse_x and dragger_x

    while pygame.mouse.get_pressed(3)[0]:  # Updates slider until button released
        fps_controller.keepFrameDurationCorrect()
        SCREEN.fill(DARK_GREY)
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


# Stats menu
def stats(page=1):
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    previous_button = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    next_button = (NEXT_BTN_X, NEXT_BTN_Y)

    selected_button = None
    mouse_btn_is_held_down = False

    STATS_VALUES = updateStats()

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        showStatsMenu(page)

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        # On which button is the cursor?
        if clickBox(back_button):
            selected_button = back_button
        elif clickBox(previous_button) and page != 1:
            selected_button = previous_button
        elif clickBox(next_button) and page != len(STATS_VALUES):
            selected_button = next_button
        else:
            selected_button = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False  # Stop main menu proccess
                    launchMainMenu()
                elif clickBox(previous_button) and page != 1:
                    page -= 1
                elif clickBox(next_button) and page != len(STATS_VALUES):
                    # Cant go higher than last page
                    page += 1

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu()
                elif event.key == pygame.K_RIGHT and page != len(STATS_VALUES):
                    page += 1
                elif event.key == pygame.K_LEFT and page != 1:
                    page -= 1


def trophies():
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    previous_button = (PREVIOUS_BTN_X, PREVIOUS_BTN_Y)
    next_button = (NEXT_BTN_X, NEXT_BTN_Y)

    selected_button = None
    mouse_btn_is_held_down = False

    page = 1

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        showTrophiesScreen(page)

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        # On which button is the cursor?
        if clickBox(back_button):
            selected_button = back_button
        elif clickBox(previous_button) and page != 1:
            selected_button = previous_button
        elif clickBox(next_button) and page != len(TROPHIES):
            selected_button = next_button
        else:
            selected_button = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                if clickBox(back_button):
                    run = False
                    launchMainMenu()
                if clickBox(previous_button) and page != 1:
                    page -= 1
                if clickBox(next_button) and page != len(TROPHIES):
                    page += 1

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu()
                elif event.key == pygame.K_RIGHT and page != len(TROPHIES):
                    page += 1
                elif event.key == pygame.K_LEFT and page != 1:
                    page -= 1


# Themes menu
def themes():
    # UI
    back_button = (BACK_BTN_X, BACK_BTN_Y)
    classic_button = themeButtonPos(0)
    yin_yang_button = themeButtonPos(1)
    xp_button = themeButtonPos(2)
    THEME_BUTTONS = (classic_button, yin_yang_button, xp_button)

    selected_index = 0
    selected_button = None
    mouse_btn_is_held_down = False

    themes_info = getThemesInfo()

    # Determine which button is auto-selected on menu launch
    for i, button in enumerate(THEME_BUTTONS):
        if not themes_info[i]["active"]:
            selected_index = i
            selected_button = THEME_BUTTONS[selected_index]
            break

    run = True
    while run:
        # Update screen
        fps_controller.keepFrameDurationCorrect()

        SCREEN.fill(DARK_GREY)
        showThemesScreen(themes_info)

        if mouse_btn_is_held_down:
            activateButtonClickState(selected_button)
        else:
            activateButtonHoverState(selected_button)

        pygame.display.update()

        # UI control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeProgram()

            # Using a mouse
            if event.type == pygame.MOUSEMOTION:
                if clickBox(classic_button) and not themes_info[0]["active"]:
                    selected_index = 0
                    selected_button = THEME_BUTTONS[selected_index]
                elif clickBox(yin_yang_button) and not themes_info[1]["active"]:
                    selected_index = 1
                    selected_button = THEME_BUTTONS[selected_index]
                elif clickBox(xp_button) and not themes_info[2]["active"]:
                    selected_index = 2
                    selected_button = THEME_BUTTONS[selected_index]
                elif clickBox(back_button):
                    selected_button = back_button

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_btn_is_held_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_btn_is_held_down = False
                selected_button = None
                if clickBox(back_button):
                    run = False
                    launchMainMenu()
                elif clickBox(classic_button) and not themes_info[0]["active"]:
                    optionsValues("theme", new_value=0)
                elif clickBox(yin_yang_button) and not themes_info[1]["active"]:
                    optionsValues("theme", new_value=1)
                elif clickBox(xp_button) and not themes_info[2]["active"]:
                    optionsValues("theme", new_value=2)
                themes_info = getThemesInfo()

            # Using keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    start_index = copy.copy(
                        selected_index)  # If no suitable button to select, go back to original index
                    no_button_changed = True

                    while selected_index < len(THEME_BUTTONS) - 1:
                        selected_index += 1
                        if not themes_info[selected_index]["active"]:
                            selected_button = THEME_BUTTONS[selected_index]
                            no_button_changed = False
                            break

                    if no_button_changed:
                        selected_index = start_index
                elif event.key == pygame.K_UP:
                    start_index = copy.copy(
                        selected_index)  # If no suitable button to select, go back to original index
                    no_button_changed = True

                    while selected_index > 0:
                        selected_index -= 1
                        if not themes_info[selected_index]["active"]:
                            selected_button = THEME_BUTTONS[selected_index]
                            no_button_changed = False
                            break

                    if no_button_changed:
                        selected_index = start_index
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    optionsValues("theme", new_value=selected_index)
                    themes_info = getThemesInfo()
                    selected_index = (selected_index + 1) % 3
                    selected_button = THEME_BUTTONS[selected_index]
                elif event.key == pygame.K_ESCAPE:
                    run = False
                    launchMainMenu()


if __name__ == "__main__":
    musicControl()
    launchMainMenu()
