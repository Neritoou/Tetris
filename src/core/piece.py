import pygame
import numpy as np
from typing import List, Tuple
from ..constants import BLOCK_W, BLOCK_H

from .types import PieceData

class Piece:
    """
    Representa un tetromino individual en el juego.

    Esta clase gestiona el estado dinámico de una pieza, incluyendo su posición 
    en la cuadrícula, su rotación actual y su representación visual.
    """
    def __init__(self, name: str, data: "PieceData", row: int = 0, col: int = 0, rot: int = 0) -> None:
        """
        Inicializa una pieza activa del juego.
        Args:
            name: Identificador de la pieza ('O', 'T', 'J'...).
            data: Datos estáticos de la pieza (matrices y superficies).
            row: Fila inicial de la pieza en el tablero.
            col: Columna inicial de la pieza en el tablero.
            rot: Indice de la rotación actual.
        """
        self.name = name
        self._data = data
        self.row = row
        self.col = col
        self.rot = rot
    
    
    @property
    def type(self) -> int:
        return self._data["type"]
    
    @property
    def matrix(self) -> np.ndarray:
        """Devuelve la matriz correspondiente a la rotación actual de la pieza."""
        return self._data["matrices"][self.rot]
    
    def draw_normal(self, surface: pygame.Surface, position_in_board: Tuple[int, int]) -> None:
        """Dibuja la pieza normal usando su surface de bloque normal."""
        self._draw_blocks(surface, position_in_board, self._data["block"]["normal"])

    def draw_ghost(self, surface: pygame.Surface, position_in_board: Tuple[int, int]) -> None:
        """Dibuja la pieza fantasma usando su surface de bloque ghost."""
        self._draw_blocks(surface, position_in_board, self._data["block"]["ghost"])

    def move(self, dr: int, dc: int):
        """
        Modifica la posición de la pieza desplazandola en filas y columnas.

        Args:
            dr (int): Desplazamiento vertical (filas).
            dc (int): Desplazamiento horizontal (columnas).
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
        total = len(self._data["matrices"])
        # Se le suma una rotación a la actual y se aplica el % para controlar el índice de rotación
        self.rot = (self.rot + direction) % total

    def center(self, board_cols: int):
        """Centra las piezas en la board."""
        matrix_width = self.matrix.shape[1]
        self.col = (board_cols - matrix_width) // 2
    
    def get_cells(self, row: int | None = None, col: int | None = None) -> List[Tuple[int, int]]:
        """
        Calcula la lista de celdas absolutas (row, col) ocupadas por la pieza en el tablero.

        Args:
            row: Fila opcional para emular la posición en la board.
            col: Columna opcional para emular la posición en la board.

        Returns:
            List[Tuple[int, int]]: Lista de tuplas representando (fila, columna) absolutas.
        """
        baserow = self.row if row is None else row
        basecol = self.col if col is None else col

        cells = []
        for (r,c), block in np.ndenumerate(self.matrix):
            if block: 
                cells.append((baserow + r, basecol + c))
        return cells
    
    # --- HELPERS ---
    def _draw_blocks(self, surface: pygame.Surface, position_in_board: Tuple[int, int], block_surface: pygame.Surface) -> None:
        """
        Método interno que dibuja los bloques de la pieza usando la surface indicada.
        """
        pos_x, pos_y = position_in_board
        for (r, c), block in np.ndenumerate(self.matrix):
            if not block:
                continue
            dx = pos_x + c * BLOCK_W
            dy = pos_y + r * BLOCK_H
            surface.blit(block_surface, (dx, dy))