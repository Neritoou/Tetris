import numpy as np

# (?) VALORES DE SCREEN TEMPORALES
SCREEN_W = 1024
SCREEN_H = 768
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
SCREEN_CENTER_W = (1024 // 2)
SCREEN_CENTER_H = (768 // 2)
SCREEN_CENTER = (SCREEN_CENTER_W, SCREEN_CENTER_H)

# Block size
BLOCK_W = 27
BLOCK_H = 30
BLOCK_SIZE = (BLOCK_W, BLOCK_H)

# Board
ROWS = 20
COLS = 10
BOARD_W = BLOCK_W * COLS
BOARD_H = BLOCK_H * ROWS
BOARD_SIZE = (BOARD_W, BOARD_H)
BOARD_X = (SCREEN_W - BOARD_W) // 2
BOARD_Y = (SCREEN_H - BOARD_H) // 2
BOARD_POS = (BOARD_X, BOARD_Y)

# Block padding
BLOCK_PADDING = (4,4)
BLOCK_PW = 4
BLOCK_PH = 4

# Piece definitions
PIECE_DEFINITIONS = {
    "O": {
        "matrix": np.array([[7,7],
                            [7,7]]),
        "spritesheet_col": 7
    },
    "S": {
        "matrix": np.array([[0,2,2],
                            [2,2,0],
                            [0,0,0]]),
        "spritesheet_col": 2
    },
    "T": {
        "matrix": np.array([[4,4,4],
                            [0,4,0],
                            [0,0,0]]),
        "spritesheet_col": 4
    },
    "I": {
        "matrix": np.array([[6,6,6,6],
                            [0,0,0,0],
                            [0,0,0,0],
                            [0,0,0,0]]),
        "spritesheet_col": 6
    },
    "Z": {
        "matrix": np.array([[5,5,0],
                            [0,5,5],
                            [0,0,0]]),
        "spritesheet_col": 5
    },
    "L": {
        "matrix": np.array([[0,3,0],
                            [0,3,0],
                            [0,3,3]]),
        "spritesheet_col": 3
    },
    "J": {
        "matrix": np.array([[0,0,1],
                            [0,0,1],
                            [0,1,1]]),
        "spritesheet_col": 1
    },
}

# Diccionario de mapeo de números a las piezas
NUM_TO_PIECE = {
    1: "J",
    2: "S",
    3: "L",
    4: "T",
    5: "Z",
    6: "I",
    7: "O",
}