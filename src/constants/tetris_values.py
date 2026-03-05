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

PIECE_SPAWN_OFFSET = -2

# Board
ROWS = 20
COLS = 10
BOARD_W = BLOCK_W * COLS
BOARD_H = BLOCK_H * ROWS
BOARD_SIZE = (BOARD_W, BOARD_H)
BOARD_X = (SCREEN_W - 595) // 2
BOARD_Y = (SCREEN_H - BOARD_H) // 2
BOARD_POS = (BOARD_X, BOARD_Y)

HOLD_X = BOARD_X + 77
HOLD_Y = BOARD_Y + 105

MAX_RECORDS = 8

# Block padding
BLOCK_PADDING = (4,4)
BLOCK_PW = 4
BLOCK_PH = 4

# Piece definitions
PIECE_DEFINITIONS = {
    "O": {
        "matrix": np.array([[0,1,1],
                            [0,1,1],
                            [0,0,0]]),
        "spritesheet_col": 7
    },
    "S": {
        "matrix": np.array([[0,1,1],
                            [1,1,0],
                            [0,0,0]]),
        "spritesheet_col": 2
    },
    "T": {
        "matrix": np.array([[0,1,0],
                            [1,1,1],
                            [0,0,0]]),
        "spritesheet_col": 4
    },
    "I": {
        "matrix": np.array([[0,0,0,0],
                            [1,1,1,1],
                            [0,0,0,0],
                            [0,0,0,0]]),
        "spritesheet_col": 6
    },
    "Z": {
        "matrix": np.array([[1,1,0],
                            [0,1,1],
                            [0,0,0]]),
        "spritesheet_col": 5
    },
    "J": {
        "matrix": np.array([[1,0,0],
                            [1,1,1],
                            [0,0,0]]),
        "spritesheet_col": 1
    },
    "L": {
        "matrix": np.array([[0,0,1],
                            [1,1,1],
                            [0,0,0]]),
        "spritesheet_col": 3
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

# Wall Kicks para J, L, S, T, Z (3x3)
WALL_KICKS_OTHERS = {
    (0, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],  # 0->R
    (1, 0): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],  # R->0
    (1, 2): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],  # R->2
    (2, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],  # 2->R
    (2, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],  # 2->L
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],  # L->2
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],  # L->0
    (0, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],  # 0->L
}

# Wall Kicks para la pieza I (4x4)
WALL_KICKS_I = {
    (0, 1): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],  # 0->R
    (1, 0): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],  # R->0
    (1, 2): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],  # R->2
    (2, 1): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],  # 2->R
    (2, 3): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],  # 2->L
    (3, 2): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],  # L->2
    (3, 0): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],  # L->0
    (0, 3): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],  # 0->L
}

WALL_KICKS = {
    "I": WALL_KICKS_I,
    "OTHERS": WALL_KICKS_OTHERS
}