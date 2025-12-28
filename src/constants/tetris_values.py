import numpy as np

# Board
ROWS = 20
COLS = 10

# Block size
BLOCK_SIZE = (27,30)
BLOCK_W = 27
BLOCK_H = 30

# Block padding
BLOCK_PADDING = (4,4)
BLOCK_PW = 4
BLOCK_PH = 4

# Piece definitions
PIECE_DEFINITIONS = {
    "O": {
        "matrix": np.array([[1,1],
                            [1,1]]),
        "spritesheet_col": 7
    },
    "S": {
        "matrix": np.array([[0,1,1],
                            [1,1,0],
                            [0,0,0]]),
        "spritesheet_col": 2
    },
    "T": {
        "matrix": np.array([[1,1,1],
                            [0,1,0],
                            [0,0,0]]),
        "spritesheet_col": 4
    },
    "I": {
        "matrix": np.array([[1,1,1,1],
                            [0,0,0,0],
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
    "L": {
        "matrix": np.array([[0,1,0],
                            [0,1,0],
                            [0,1,1]]),
        "spritesheet_col": 3
    },
    "J": {
        "matrix": np.array([[0,0,1],
                            [0,0,1],
                            [0,1,1]]),
        "spritesheet_col": 1
    },
}