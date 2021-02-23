# CONSTANTS
BOARD_WIDTH = 10  # Number of board cells in a row
BOARD_HEIGHT = 20  # Number of board cells in a column
BLOCK_WIDTH = BLOCK_HEIGHT = 4  # Block is made of 4x4 board cells


# FUNCTIONS
def createBoard():
    return [[0] * BOARD_WIDTH for row in range(BOARD_HEIGHT)]  # 2D array, where "0" represents empty cell


def printBoard(board):
    for row in range(BOARD_HEIGHT):
        print()
        for col in range(BOARD_WIDTH):
            print(board[row][col], end=" ")

    print()


def copyBoard(src, dest=0):
    if dest == 0:
        dest = createBoard()

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            dest[row][col] = src[row][col]

    return dest


def clearFullRows(board):
    full_rows = 0
    # Go trough every board row and check if row is full
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                break  # Row isn't full

            if col == BOARD_WIDTH - 1:  # Last column has been checked and row is full
                full_rows += 1  # Number of full rows
                board.pop(row)
                board.insert(0, [0] * BOARD_WIDTH)

    return full_rows

def perfectClear(board):
    perfect_clear = True
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] != 0:
                perfect_clear = False
                break
    return perfect_clear
