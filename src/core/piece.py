import pygame
import numpy as np

from typing import List, Tuple

from .types import PieceData
from ..constants import BLOCK_H, BLOCK_W, ROWS, COLS

class Piece:
    """
    Representa un tetromino individual en el juego.

    Esta clase gestiona el estado dinámico de una pieza, incluyendo su posición 
    en la cuadrícula, su rotación actual y su representación visual.
    """
    def __init__(self, name: str, data: PieceData, row: int = 0, col: int = 0, rot: int = 0, state: str = "normal") -> None:
        """
        Inicializa una pieza activa del juego.

        Args:
            name: Identificador de la pieza ('O', 'T', 'J'...).
            data: Datos estáticos de la pieza (matrices y superficies).
            row: Fila inicial de la pieza en el tablero.
            col: Columna inicial de la pieza en el tablero.
            rot: Indice de la rotación actual.
            state: Estado visual de la pieza (normal, placed, ghost).
        """
        self.name = name
        self.data = data
        self.row = row
        self.col = col
        self.rot = rot
        self.state = state

    @property
    def matrix(self) -> np.ndarray:
        """Devuelve la matriz correspondiente a la rotación actual de la pieza."""
        return self.data["matrices"][self.rot]
    
    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja la pieza en la ventana bloque por bloque."""
        pos_x, pos_y = self._get_coords_of_piece_in_board(self.row, self.col)

        for (r, c), block in np.ndenumerate(self.matrix):
            if not block: continue
            dx = pos_x + c * BLOCK_W
            dy = pos_y + r * BLOCK_H
            surface.blit(self.data["block"][self.state], (dx, dy))

    def move(self, dr: int, dc: int):
        """
        Modifica la posición de la pieza desplazandola en filas y columnas.

        Args:
            dr: Desplazamiento vertical (filas).
            dc: Desplazamiento horizontal (columnas).
        """
        self.row += dr
        self.col += dc

    def rotate(self, direction: int = 1): 
        """
        Cicla entre las posibles rotaciones de la pieza.
        
        Args:
            direction: Sentido de giro. 1 para horario, -1 para antihorario.
        """
        # Mide la cantidad de rotaciones que tiene la pieza.
        total = len(self.data["matrices"])
        # Se le suma una rotación a la actual y se aplica el % para controlar el índice de rotación
        self.rot = (self.rot + direction) % total

    def center_piece(self, board_cols: int):
        """Centra las piezas en la board."""
        matrix_width = self.matrix.shape[1]
        self.col = (board_cols - matrix_width) // 2
    
    def get_cells(self, row: int | None = None, col: int | None = None) -> List[Tuple[int, int]]:
        """
        Calcula la lista de celdas absolutas (y, x) ocupadas por la pieza en el tablero.

        Args:
            row: Fila opcional para emular la posición en la board.
            col: Columna opcional para emular la posición en la board.

        Returns:
            List[Tuple[int, int]]: Lista de tuplas representando (fila, columna) absolutas.
        """
        base_row = self.row if row is None else row
        base_col = self.col if col is None else col

        cells = []
        matrix = self.matrix

        for r in range(len(matrix)): # itera con respecto a las filas
            for c in range(len(matrix[r])): # itera con respecto a las columnas que tenga la fila actual
                if matrix[r][c]:
                    cells.append((base_row + r, base_col + c))
        return cells

    def _get_coords_of_piece_in_board(self, row: int, col: int) -> Tuple[int, int]:
        """
        Calcula el desplazamiento (offset) en píxeles para el centrado del tablero.

        Args:
            row: Índice de fila en el tablero.
            col: Índice de columna en el tablero.

        Returns:
            Tuple[int, int]: Coordenadas (x, y) de la pieza en píxeles.
        """
        board_w = BLOCK_W * COLS
        board_h = BLOCK_H * ROWS

        board_x = (1024 - board_w) // 2
        board_y = (768 - board_h) // 2
        
        return ((board_x + col * BLOCK_W), (board_y + row * BLOCK_H))