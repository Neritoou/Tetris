import pygame
import numpy as np

from .piece import Piece
from ..constants import ROWS, COLS, BLOCK_H, BLOCK_W

class Board:
    """
    Gestiona la lógica y el estado del tablero de juego.

    Es responsable de mantener la matriz de bloques fijos, controlar 
    el movimiento y rotación de la pieza activa mediante validaciones de 
    colisión y procesar la eliminación de líneas completas.
    """
    def __init__(self, board_surface: pygame.Surface, block_surface: pygame.Surface) -> None:
        """
        Inicializa el tablero del juego.

        Args:
            board_surface: Imagen del tablero.
            block_surface: Bloque individual de cada pieza.
        """
        self.rows = ROWS
        self.cols = COLS

        self.board: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)
        self.board_surface = board_surface

        self.width = self.board_surface.get_width()
        self.height = self.board_surface.get_height()
        self._rect = self.board_surface.get_rect()

        self.x = (1024 - self.width) // 2
        self.y = (768 - self.height) // 2
        self._rect.topleft = (self.x, self.y)

        self.cell_width: int = BLOCK_W
        self.cell_height: int = BLOCK_H
        self.block_surface = block_surface
        self.active_piece: Piece | None = None

    def draw(self, surface: pygame.Surface):
        """Dibuja el fondo del tablero, los bloques estáticos y la pieza activa."""
        surface.blit(self.board_surface, self._rect)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] > 0:
                    bx = self.x + c * self.cell_width
                    by = self.y + r * self.cell_height
                    surface.blit(self.block_surface, (bx, by))
        
        if self.active_piece:
            self.active_piece.draw(surface)

    def spawn_piece(self, piece: Piece) -> None:
        """
        Genera y centra la pieza en el tablero.
        
        Args:
            piece (Piece): Nombre de la pieza.
        """  
        self.active_piece = piece        
        piece.center_piece(self.cols)

    def lock_piece(self):
        """Bloquea la pieza en el tablero y elimina la pieza activa marcandola como 'placed'."""
        if not self.active_piece:
            return
        
        for r, c in self.active_piece.get_cells():
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.board[r, c] = 1
        self.active_piece.state = "placed"
        self.active_piece = None

    def clear_lines(self):
        """
        Escanea el tablero para eliminar filas llenas y desplazar las filas
        superiores hacia abajo.

        Returns:
            int: Cantidad de líneas eliminadas.
        """
        lines_cleared = 0
        for r in range(self.rows):
            zeros = 0
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    zeros += 1
            if zeros == 0:
                lines_cleared += 1
                for rl in range(r, 1, -1):
                    for c in range (self.cols):
                        self.board[rl][c] = self.board[rl - 1][c]
        return lines_cleared
    
    def try_move(self, dr: int, dc: int) -> bool:
        """
        Intenta desplazar la pieza activa si el movimiento es válido.

        Args:
            dr: Cantidad de filas que se intenta mover la pieza.
            dc: Cantidad de columnas que se intenta mover la pieza.
                0 para no cambiar esa posicion, 1 para mover hacia la derecha o abajo, -1 para la izquierda.

        Returns:
            bool: True si el movimiento es posible, False si no.
        """
        if not self.active_piece:
            return False
        
        new_row = self.active_piece.row + dr
        new_col = self.active_piece.col + dc

        if self.is_valid(self.active_piece, new_row, new_col):
            self.active_piece.move(dr, dc)
            return True
        return False
    
    def try_fall_piece(self) -> bool:
        """
        Permite que la pieza caiga por gravedad de ser posible.

        Returns:
            bool: True mientras se pueda mover, False cuando no.
        """
        if not self.active_piece:
            return False
        
        if self.try_move(1, 0):
            return True
        return False

    def try_rotate(self, direction: int = 1) -> bool:
        """
        Intenta rotar la pieza activa y valida el resultado.

        Args:
            direction: Sentido del giro (1 para horario, -1 para antihorario).

        Returns:
            bool: True si la rotación fue exitosa y se mantuvo; 
                  False si fue ilegal y se tuvo que revertir.
        """
        if not self.active_piece:
            return False
        
        piece = self.active_piece
        old_rot = piece.rot
        
        piece.rotate(direction)

        if self.is_valid(piece):
            return True
        
        # Si la rotación no es es válida, se revierte
        piece.rot = old_rot
        return False
    
        # (!) Intentar implementar los wall kicks

    # --- MÉTODOS PARA VALIDAR ---
    def is_game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""

        if not self.active_piece:
            return False
        if self.is_valid(self.active_piece):
            return False
        return True
    
    def is_valid(self, piece: Piece, row: int | None = None, col: int | None = None) -> bool:
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
            if r >= self.rows:
                return False
            if c < 0 or c >= self.cols: 
                return False
            if r >= 0 and self.board[r, c]: 
                return False
        return True