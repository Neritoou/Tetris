import pygame
import numpy as np
from src.constants import BLOCK_W, BLOCK_H, WALL_KICKS
from src.core.types import PieceData

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
        self.ghost_row = -1
        self.ghost_col = -1
        self.ghost_rot = -1
        self.active = True
    
    @property
    def type(self) -> int:
        return self._data["type"]
    
    @property
    def matrix(self) -> np.ndarray:
        """Devuelve la matriz correspondiente a la rotación actual de la pieza."""
        return self._data["matrices"][self.rot]
    
    def is_locked(self) -> bool:
        """Retorna verdadero si la pieza ya está bloqueada en el tablero"""
        return not self.active
    
    def set_locked(self) -> None:
        """Cambia el estado de la pieza a bloqueada"""
        self.active = False

    def set_actived(self) -> None:
        """Cambia el estado de la pieza a activada"""
        self.active = True
    
    def draw_normal(self, surface: pygame.Surface, position_in_board: tuple[int, int]) -> None:
        """Dibuja la pieza normal usando su surface de bloque normal."""
        self._draw_blocks(surface, position_in_board, self._data["block"]["normal"])

    def draw_ghost(self, surface: pygame.Surface, position_in_board: tuple[int, int]) -> None:
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

    def center(self, board_cols: int, spawn_offset: int = 0):
        """
        Centra horizontalmente la pieza en el tablero y aplica un spawn_offset
        vertical para generarla fuera de la pantalla si spawn_offset < 0.
        """
        matrix_width = self.matrix.shape[1]
        self.col = (board_cols - matrix_width) // 2
        self.row = spawn_offset
    
    def get_cells(self, row: int | None = None, col: int | None = None) -> list[tuple[int, int]]:
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

        cells: list[tuple[int, int]] = []
        for (r,c), block in np.ndenumerate(self.matrix):
            if block: 
                cells.append((baserow + r, basecol + c))
        return cells
    
    def get_wall_kicks(self, old_rot: int, new_rot: int):
        """
        Obtiene los Wall Kicks necesarios para una rotación de pieza, basándose en el tipo de pieza 
        y las rotaciones previas y actuales.

        Los Wall Kicks son desplazamientos que se aplican a una pieza cuando no puede rotar debido 
        a una colisión, pero puede moverse 
        ligeramente para que la rotación sea válida.

        Args:
            old_rot (int): La rotación previa de la pieza (en grados: 0, 90, 180, 270).
            new_rot (int): La nueva rotación de la pieza (en grados: 0, 90, 180, 270).
            piece_type (str): El tipo de pieza que se está rotando (por ejemplo, "I", "T", "J", "L", "S", "Z", "O").

        Returns:
            List[Tuple[int, int]]: Una lista de desplazamientos (dx, dy) que representan los posibles wall kicks para realizar la rotación.
            Si no se encuentran desplazamientos, devuelve [(0, 0)], lo que indica que no hay necesidad de aplicar un wall kick.
        """
        if self.name == "I":
            table = WALL_KICKS["I"]
        elif self.name != "O":
            table = WALL_KICKS["OTHERS"]
        else:
            return [(0, 0)]

        return table.get((old_rot % 4, new_rot % 4), [(0, 0)])

    
    # --- HELPERS ---
    def _draw_blocks(self, surface: pygame.Surface, position_in_board: tuple[int, int], block_surface: pygame.Surface) -> None:
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