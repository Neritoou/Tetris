import pygame
import numpy as np
from typing import TYPE_CHECKING
from src.constants import NUM_TO_PIECE

if TYPE_CHECKING:
    from piece import Piece
    from src.core.types import PieceDataType

class Board:
    """
    Gestiona la lógica y el estado del tablero de juego.

    Es responsable de mantener la matriz de bloques fijos, controlar 
    el movimiento y rotación de la pieza activa mediante validaciones de 
    colisión y procesar la eliminación de líneas completas.
    """
    def __init__(self, rows: int, cols: int, surface: pygame.Surface, 
                 cell_width: int, cell_height: int,
                 pos_x: int, pos_y: int) -> None:
        """
        Inicializa el tablero del juego.

        Args:
            surface: Imagen del tablero.
            block_surface: Bloque individual de cada pieza.
        """
        self.rows = rows
        self.cols = cols
        self.matrix: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)

        self._surface = surface
        self._width: int = self._surface.get_width()
        self._height: int = self._surface.get_height()
        self._rect: pygame.Rect = self._surface.get_rect()
        self._rect.topleft = (pos_x, pos_y)

        self.cell_width = cell_width
        self.cell_height = cell_height

    def draw(self, surface: pygame.Surface, pieces: "PieceDataType") -> None:
        """Dibuja el fondo del tablero, los bloques estáticos y la pieza activa."""
        # Dibuja la Board
        surface.blit(self._surface, self._rect)

        for (row,col), block in np.ndenumerate(self.matrix):
            if block:
                bx = self._rect.x + col * self.cell_width
                by = self._rect.y + row * self.cell_height
                block_surface = pieces[NUM_TO_PIECE[block]]["block"]["placed"]

                surface.blit(block_surface, (bx, by))

    def lock_piece(self, piece: "Piece") -> None:
        """
        Bloquea la pieza actual en el tablero, marcando las celdas que ocupa como ocupadas 
        (con valor 1) en la matriz. Después de bloquearla, la pieza activa se elimina.
        """
        for r, c in piece.get_cells():
            # Verifica que la celda esté dentro del tablero
            if 0 <= r < self.rows and 0 <= c < self.cols: 
                self.matrix[r, c] = piece.type

    def clear_lines(self) -> int:
        """
        Escanea el tablero para eliminar filas llenas y desplazar las filas
        superiores hacia abajo.

        Returns:
            int: Cantidad de líneas eliminadas.
        """
        lines_cleared = 0

        # Detecta las filas llenas
        fullrows = self.__find_fullrows()

        if len(fullrows) > 0:
            lines_cleared = len(fullrows)
            # EN CASO DE HACER ANIMACIONES, AQUI DEBERIAN DE IR

            # Elimina las filas completas y las desplaza
            self.__remove_filled_lines(fullrows)

        return lines_cleared
    
    def is_valid_move(self, piece: "Piece", row: int | None = None, col: int | None = None) -> bool:
        """
        Verifica si la pieza colisiona con los bordes o bloques existentes.

        Args:
            piece: Instancia de la pieza a validar.
            row: Posición de la pieza en las filas del tablero.
            col: Posición de la pieza en las columnas del tablero.

        Returns:
            bool: True si la posición está libre, False si no está ocupada o fuera de límites.

        """
        for r, c in piece.get_cells(row, col):
            if r >= self.rows or (c < 0 or c >= self.cols) or (r >= 0  and self.matrix[r, c]):
                return False
        return True
    
    def is_empty(self, check_rows: int = 3) -> bool:
        """Verifica si las últimas `check_rows` filas del tablero están vacías.

        Con tan solo comprobar las últimas filas es posible conocer si la Board está vacía"""
        return not np.any(self.matrix[-check_rows:, :])



    # --- HELPERS ---
    def get_pixels_of_cell(self, row: int, col: int) -> tuple[int, int]:
        """
        Convierte una posición de celda del tablero (row, col) en coordenadas
        absolutas en píxeles para dibujar la pieza en pantalla.

        La conversión toma como origen la esquina superior izquierda del tablero
        y aplica el tamaño de cada celda.

        Args:
            row: Fila de la celda dentro del tablero.
            col: Columna de la celda dentro del tablero.

        Returns:
            Tuple[int, int]: Coordenadas (x, y) en píxeles dentro de la ventana.
        """
        return ((self._rect.x + col * self.cell_width), (self._rect.y + row * self.cell_height))
    
    def __find_fullrows(self) -> np.ndarray:
        """
        Encuentra las filas llenas en el tablero (todas las celdas tienen un valor diferente de 0).

        Returns:
            np.ndarray: Un arreglo con los índices de las filas completas.
        """
        # Verifica si todas las celdas en cada fila son diferentes de 0
        fullrows = np.where(np.all(self.matrix != 0, axis=1))[0]
        return fullrows
    
    def __remove_filled_lines(self, fullrows: np.ndarray) -> None:
        """
        Elimina las filas llenas de la matriz y las desplaza hacia abajo.

        Args:
            fullrows: Las filas que deben ser eliminadas.
        """
        # Elimina las filas completas de la matriz
        self.matrix = np.delete(self.matrix, fullrows, axis=0)

        # Añade filas vacías (llenas de ceros) en la parte superior del tablero
        new_emptyrows = np.zeros((len(fullrows), self.cols), dtype=int) # Crea las filas vacias
        self.matrix = np.vstack((new_emptyrows, self.matrix)) # Las anexa a la matrix
