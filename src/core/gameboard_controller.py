from typing import Tuple, Dict, TYPE_CHECKING
from .board import Board
from .piece import Piece
from .piece_spawner import PieceSpawner
from pygame import Surface

if TYPE_CHECKING:
    from .types import PieceData

class GameBoardController:
    def __init__(self, board: Board, spawner: PieceSpawner):
        self.board = board
        self.spawner = spawner
        self.piece: Piece | None = None

    def spawn_piece(self) -> None:
        """Genera y coloca una nueva pieza en el tablero."""
        self.piece = self.spawner.new_piece()
        self.piece.center(self.board.cols)

    def draw(self, surface: Surface, pieces: "Dict[str, PieceData]") -> None:
        # Dibujar la Board
        self.board.draw(surface, pieces) 
        
        # Dibuja la Pieza activa actualmente
        if not self.piece: return

        pos_normal = self.board.get_pixels_of_cell(self.piece.row, self.piece.col)
        r, c = self.get_ghost_position(self.piece)
        pos_ghost = self.board.get_pixels_of_cell(r,c)

        self.piece.draw_normal(surface, pos_normal)
        self.piece.draw_ghost(surface, pos_ghost)

    def try_move_to(self, dr: int, dc: int) -> bool:
        """
        Intenta desplazar la pieza activa si el movimiento es válido.

        Args:
            dr: Cantidad de filas que se intenta mover la pieza.
            dc: Cantidad de columnas que se intenta mover la pieza.
                0 para no cambiar esa posicion, 1 para mover hacia la derecha o abajo, -1 para la izquierda.

        Returns:
            bool: True si el movimiento es posible, False si no.
        """
        if not self.piece:
            return False
        
        new_row = self.piece.row + dr
        new_col = self.piece.col + dc

        if self.board.is_valid(self.piece, new_row, new_col):
            self.piece.move(dr, dc)
            return True
        return False
    
    def try_fall(self) -> bool:
        """
        Permite que la pieza caiga por gravedad de ser posible.

        Returns:
            bool: True mientras se pueda mover, False cuando no.
        """
        return self.try_move_to(1, 0)  # Intentar mover hacia abajo (dr=1, dc=0)

    def try_rotate(self, direction: int = 1) -> bool:
        """
        Intenta rotar la pieza activa y valida el resultado.

        Args:
            direction: Sentido del giro (1 para horario, -1 para antihorario).

        Returns:
            bool: True si la rotación fue exitosa y se mantuvo; 
                  False si fue ilegal y se tuvo que revertir.
        """
        if not self.piece:
            return False
        
        old_rot = self.piece.rot
        self.piece.rotate(direction)
        if self.board.is_valid(self.piece):
            return True
        
        # Si la rotación no es es válida, se revierte
        self.piece.rot = old_rot
        return False
    
        # (!) Intentar implementar los wall kicks
    
    def get_ghost_position(self, piece: "Piece") -> Tuple[int, int]:
        """
        Calcula la fila en la que la pieza debe caer (posición fantasma).
        
        Esta función calcula la posición fantasma utilizando el movimiento vertical hasta que no sea posible.

        Args:
            piece: La pieza activa para la cual calcular la posición fantasma.
        
        Returns:
            Tuple[int, int]: La fila y columna de la posición fantasma.
        """ 
        row = piece.row
        col = piece.col

        # Mueve la pieza hacia abajo hasta que no pueda caer más
        while self.board.is_valid(piece, row + 1, col):
            row += 1

        return row, col