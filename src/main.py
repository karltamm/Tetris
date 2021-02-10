import pygame
from board import *
from smallboard import *
from blocks import *
from screen import *
from assets import *


# MAIN
pygame.init()
CLOCK = pygame.time.Clock()

def game():
    SCREEN.fill(BLACK)
    board = createBoard()  # 2D array, where "0" represents empty cell
    small_board = createSmallBoard()

    current_block = activeBlock(0, board)
    next_block = randomBlock(small_board, 0, 1)
    third_block = randomBlock(small_board, 0, 6)

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
                pygame.quit()
                exit()

            # Move block
            if event.type == pygame.KEYDOWN:  # If a key is pressed down
                key_timer = 0
                if event.key == pygame.K_ESCAPE:
                    run = False
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
            current_block = activeBlock(next_block, board)
            next_block = third_block
            NextBlocks(next_block, small_board, 0, 1)
            third_block = randomBlock(small_board, 0, 6)


        # Screen
        updateSmallBoard(small_board)
        updateMainBoard(board)


def options():
    run = True
    while run:
        SCREEN.fill((BLACK))
        
        draw_text('OPTIONS', font1, WHITE, SCREEN, 210, 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pygame.display.update()
        CLOCK.tick(FPS)


def main_menu():
    while True:
        SCREEN.fill((0,0,0))

        mouse_x, mouse_y = pygame.mouse.get_pos() # Get mouse location
        click = False
 
        button_1 = pygame.Rect(150, 200, 200, 50)
        button_2 = pygame.Rect(150, 300, 200, 50)

        pygame.draw.rect(SCREEN, RED, button_1)
        pygame.draw.rect(SCREEN, RED, button_2)
        draw_text('TETRIS', font2, (100, 255, 255), SCREEN, 190, 45)
        draw_text('MAIN MENU', font1, WHITE, SCREEN, 200, 115)
        draw_text('NEW GAME', font1, WHITE, SCREEN, 205, 215)
        draw_text('OPTIONS', font1, WHITE, SCREEN, 205, 315)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                game()
        if button_2.collidepoint((mouse_x, mouse_y)):
            if click:
                options()
 
        pygame.display.update()
        CLOCK.tick(FPS)

main_menu()
