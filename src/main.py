import pygame

from shapes import *
from blockClass import *
from functions import *

# MAIN
def main():
    board = createBoard() # 2D array, where "0" represents empty cell
    currentBlock = randomShape(board) # Generates random shape into currentBlock
    nextBlock = randomShape(board)
    run = True
    changeBlock = False
    fall_time = 0
    fall_speed = 25 # Lower value -> Faster drop speed
    while run:
        CLOCK.tick(FPS)
        # Block automatic dropping
        fall_time += 1
        if fall_time > fall_speed:
            fall_time = 0
            currentBlock.move(board, 0, 1)
        # Input
        for event in pygame.event.get():
            # Close game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Move block
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    currentBlock.rotate(board)
                if event.key == pygame.K_DOWN:
                    currentBlock.move(board, 0, 1)
                elif event.key == pygame.K_RIGHT:
                    currentBlock.move(board, 1, 0)
                elif event.key == pygame.K_LEFT:
                    currentBlock.move(board, -1, 0)
            ''' TODO
            if changeBlock:
                lockedBlocks[p] = currentBlock
                currentBlock = nextBlock
                nextBlock = randomShape(board)
                changeBlock = False
            '''
        # UI
        updateScreen(board)
main()
