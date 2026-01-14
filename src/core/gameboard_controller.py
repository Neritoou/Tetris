from pygame import Surface
from typing import Tuple, Any, Dict, TYPE_CHECKING
from ..constants import PIECE_DEFINITIONS, ROWS, COLS, BLOCK_W, BLOCK_H
from .piece_bag import PieceBag
from .board import Board
from .piece import Piece
from .score import Score
from .pieces_preview import PiecesPreview

if TYPE_CHECKING:
    from .types import BoardType, PiecesPreviewType, PieceDataType
    from ..config import GameplayConfigType

class GameBoardController:
    def __init__(self, 
                session_config: "GameplayConfigType", 
                pieces: "PieceDataType", 
                board: "BoardType",
                preview: "PiecesPreviewType") -> None:
        
        self.data = pieces
        self.score = Score(session_config)
        self.bag = PieceBag(PIECE_DEFINITIONS, session_config["general"]["bag_size"])
        self.pieces_preview = PiecesPreview(
            data = pieces,
            bag = self.bag,
            preview = preview
        )
        self.board = Board(ROWS, COLS, board["surface"], BLOCK_W, BLOCK_H, board["pos_x"], board["pos_y"])
        self.piece: Piece
        self.ghost_position: Tuple[int, int]

        self.soft_drop: int = 0
        self.hard_drop: int = 0

    def set_preview_count(self, count: int) -> None:
        """
        Actualiza dinámicamente la cantidad de piezas que se muestran en la vista previa.
        Args:
            count (int): Número positivo de piezas a mostrar en la preview.
        """
        self.pieces_preview.count = count

    def spawn_piece(self) -> None:
        """Genera y coloca una nueva pieza en el tablero."""
        piece_name = self.bag.get_next_piece()
        piece_data = self.data[piece_name]
        self.piece = Piece(piece_name, piece_data)
        self.piece.center(self.board.cols, spawn_offset = -2)
        self.pieces_preview.generate()

    def draw(self, surface: Surface, pieces: "PieceDataType") -> None:
        """
        Dibuja todos los elementos visuales asociados a este tablero de juego.

        El orden de dibujo es el siguiente:
        1. El tablero (Board).
        2. La vista previa de las próximas piezas (PiecesPreview).
        3. La pieza activa y su pieza fantasma (ghost), si existe y no está bloqueada.

        Args:
            surface (Surface): Superficie principal donde se renderiza el juego.
            pieces (PieceDataType): Diccionario con los datos gráficos y lógicos
                de todas las piezas (matrices, surfaces y bloques).
        """
        # Dibujar la Board
        self.board.draw(surface, pieces) 
        
        # Dibujar la preview de las próximas piezas
        for surf, x, y in self.pieces_preview.get():
            surface.blit(surf, (x, y))

        # Dibujar la Pieza y su Ghost si es posible
        if not hasattr(self, "piece") or self.piece.is_locked():
            return

        pos_normal = self.board.get_pixels_of_cell(self.piece.row, self.piece.col)
        r, c = self.get_ghost_position()
        pos_ghost = self.board.get_pixels_of_cell(r,c)

        self.piece.draw_normal(surface, pos_normal)
        self.piece.draw_ghost(surface, pos_ghost)

    def resolve_piece_lock(self):
        """Bloquea la pieza en el tablero, elimina las líneas completas, y verifica si el tablero está vacío."""
        self.board.lock_piece(self.piece)
        self.piece.set_locked()
        lines = self.board.clear_lines()
        perfect_clear = self.board.is_empty()
        dict: Dict[str, Any] = { "type": "normal",
            "lines_cleared": lines, "perfect_clear": perfect_clear,
            "soft_drop": self.soft_drop, "hard_drop": self.hard_drop }
        
        # Reincia las variables de los Drops
        self.soft_drop = 0
        self.hard_drop = 0
        return dict
    
    def can_piece_move(self, dr: int, dc: int) -> bool:
        """Indica si la pieza puede desplazarse por el offset dado sin colisionar.
        Args:
            dr: Desplazamiento vertical (filas).
            dc: Desplazamiento horizontal (columnas).
        """
        return self.board.is_valid(self.piece, self.piece.row + dr, self.piece.col + dc)

    def try_move_piece_to(self, dr: int, dc: int) -> bool:
        """
        Intenta mover la pieza activa aplicando un desplazamiento relativo.

        Args:
            dr: Cantidad de filas a desplazar (positivo hacia abajo).
            dc: Cantidad de columnas a desplazar (positivo hacia la derecha).

        Returns:
            bool: True si el movimiento fue válido y aplicado.
        """
        if not hasattr(self, "piece") or self.piece.is_locked():
            return False
        
        if self.can_piece_move(dr, dc):
            self.piece.move(dr, dc)
            return True
        return False
    
    def try_fall_piece(self):
        """ Permite que la pieza caiga por gravedad de ser posible."""
        if not hasattr(self, "piece") or self.piece.is_locked():
            return
        
        if self.can_piece_move(1, 0):
            self.piece.move(1, 0)

    def try_soft_drop_piece(self) -> bool:
        """ 
        Intenta realizar un soft drop (la pieza baja una celda).
        Otorga puntos por cada celda descendida.
        """
        if self.try_move_piece_to(1, 0):
            self.soft_drop += 1
            return True
        return False

    def try_hard_drop_piece(self):
        """Realiza un hard drop (la pieza cae de golpe)."""
        distance = 0
        while self.try_move_piece_to(1, 0):
            distance += 1
        # el hard drop es contado por las filas que la pieza descendió
        self.hard_drop = distance 
    
    def try_rotate_piece(self, direction: int = 1) -> bool:
        """
        Intenta rotar la pieza activa y valida el resultado.

        Args:
            direction: Sentido del giro (1 para horario, -1 para antihorario).

        Returns:
            bool: True si la rotación fue exitosa y se mantuvo; 
                  False si fue ilegal y se tuvo que revertir.
        """
        if not hasattr(self, "piece") or self.piece.is_locked():
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
            if self.board.is_valid(self.piece, old_row + dr, old_col + dc):
                self.piece.move(dr, dc)
                return True

        # Revertir si todo falla
        self.piece.rot = old_rot
        self.piece.row = old_row
        self.piece.col = old_col
        return False

    def get_ghost_position(self) -> Tuple[int,int]:
        """
        Calcula la fila en la que la pieza debe caer (posición fantasma).
        
        Esta función calcula la posición fantasma utilizando el movimiento vertical hasta que no sea posible.
        
        Returns:
            Tuple[int, int]: La fila y columna de la posición fantasma.
        """ 
        row = self.piece.row
        col = self.piece.col
        distance = 0
        # Mueve la pieza hacia abajo hasta que no pueda caer más
        while self.board.is_valid(self.piece, row + 1, col):
            distance += 1
            row += 1

        return (row, col)
    