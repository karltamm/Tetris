import pygame
import random

from shapes import *
from blockClass import *
from functions import *

""" FUNCTIONS """
# board
def createBoard():
    return [[0] * BOARD_WIDTH for row in range(BOARD_HEIGHT)] # 2D array, where "0" represents empty cell

def printBoard(board):
    for row in range(BOARD_HEIGHT):
        print()
        for col in range(BOARD_WIDTH):
            print(board[row][col], end = " ")
    print()
    
def copyBoard(src, dest = 0):
    if dest == 0:
        dest = createBoard()
        
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            dest[row][col] = src[row][col]

    return dest

# UI
def updateScreen(board):
    # Update board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                SCREEN.blit(EMPTY_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 1:
                SCREEN.blit(GREEN_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 2:
                SCREEN.blit(INDIGO_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 3:
                SCREEN.blit(ORANGE_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 4:
                SCREEN.blit(PINK_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 5:
                SCREEN.blit(RED_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 6:
                SCREEN.blit(YELLOW_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))
            elif board[row][col] == 7:
                SCREEN.blit(BLUE_CELL, (BOARD_X + col * BOARD_CELL, BOARD_Y + row * BOARD_CELL))

    pygame.display.update()
