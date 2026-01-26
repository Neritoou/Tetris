from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..board import Board
    from ..piece import Piece
    from ..score import Score

class MovementManager:
    def __init__(self,board: Board, piece: Piece, score: Score):
        self.board = board
        self.piece = piece
        self.score = score

    def can_piece_move(self, dr: int, dc: int) -> bool:
        """Indica si la pieza puede desplazarse por el offset dado sin colisionar.
        Args:
            dr: Desplazamiento vertical (filas).
            dc: Desplazamiento horizontal (columnas).
        """
        return self.board.is_valid_move(self.piece, self.piece.row + dr, self.piece.col + dc)

    def try_move_piece_to(self, dr: int, dc: int) -> bool:
        """
        Intenta mover la pieza activa aplicando un desplazamiento relativo.

        Args:
            dr: Cantidad de filas a desplazar (positivo hacia abajo).
            dc: Cantidad de columnas a desplazar (positivo hacia la derecha).

        Returns:
            bool: True si el movimiento fue válido y aplicado.
        """
        if self.piece.is_locked():
            return False
        
        if self.can_piece_move(dr, dc):
            self.piece.move(dr, dc)
            return True
        return False
    
    def try_fall_piece(self):
        """ Permite que la pieza caiga por gravedad de ser posible."""
        if self.piece.is_locked():
            return
        
        if self.can_piece_move(1, 0):
            self.piece.move(1, 0)

    def try_soft_drop_piece(self) -> bool:
        """ 
        Intenta realizar un soft drop (la pieza baja una celda).
        Otorga puntos por cada celda descendida.
        """
        if self.try_move_piece_to(1, 0):
            self.score.soft_drop += 1
            return True
        return False

    def try_hard_drop_piece(self):
        """Realiza un hard drop (la pieza cae de golpe)."""
        self.score.hard_drop = max(0,self.piece.ghost_row - max(self.piece.row,0))
        self.piece.row = self.piece.ghost_row
        self.piece.col = self.piece.ghost_col

    def try_rotate_piece(self, direction: int = 1) -> bool:
        """
        Intenta rotar la pieza activa y valida el resultado.

        Args:
            direction: Sentido del giro (1 para horario, -1 para antihorario).

        Returns:
            bool: True si la rotación fue exitosa y se mantuvo; 
                  False si fue ilegal y se tuvo que revertir.
        """
        if self.piece.is_locked():
            return False

        # La O no necesita rotación real
        if self.piece.name == "O":
            return True
 
        old_rot = self.piece.rot
        old_row = self.piece.row
        old_col = self.piece.col

        # Aplica la rotación
        self.piece.rotate(direction)

        # Intentar wall kicks
        wall_kicks = self.piece.get_wall_kicks(old_rot, self.piece.rot)

        for dr, dc in wall_kicks:
            if self.board.is_valid_move(self.piece, old_row + dr, old_col + dc):
                self.piece.move(dr, dc)
                return True

        # Revertir si todo falla
        self.piece.rot = old_rot
        self.piece.row = old_row
        self.piece.col = old_col
        return False