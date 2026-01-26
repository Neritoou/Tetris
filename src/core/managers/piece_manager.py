from typing import TYPE_CHECKING
from ..piece import Piece
if TYPE_CHECKING:
    from ..board import Board
    from ..pieces_preview import PiecesPreview
    from ..piece_bag import PieceBag
    from pygame import Surface
    from ..types import PieceDataType
    from ..score import Score
    
class PieceManager:
    def __init__(self, piece: Piece, piece_bag: "PieceBag", board: "Board", preview: "PiecesPreview", pieces_data: "PieceDataType", score: Score):
        self.bag = piece_bag
        self.data = pieces_data
        self.preview = preview
        self.board = board
        self.current = piece
        self.score = score


    def spawn(self) -> None:
        """Genera y coloca una nueva pieza en el tablero."""
        piece_name = self.bag.get_next_piece()
        piece_data = self.data[piece_name]
        self.current = Piece(piece_name, piece_data)
        self.current.center(self.board.cols, spawn_offset = -2)
        self.preview.generate()
        self.calculate_ghost_position()


    def lock(self) -> None:
        """Bloquea la pieza en el tablero, elimina las líneas completas, y verifica si el tablero está vacío."""
        self.board.lock_piece(self.current)
        self.current.set_locked()
        lines = self.board.clear_lines()
        perfect_clear = self.board.is_empty() # VER SI SE USARÁ
            
        self.score.update(lines,"normal")

        self.lock.timer = 0.0
        self.soft_drop = 0
        self.hard_drop = 0

    def draw(self, surface: Surface) -> None:

        # Dibujar la preview de las próximas piezas
        for surf, x, y in self.preview.get():
            surface.blit(surf, (x, y))

        # Dibujar la Pieza y su Ghost si es posible
        if not hasattr(self, "piece") or self.current.is_locked():
            return

        pos_normal = self.board.get_pixels_of_cell(self.current.row, self.current.col)
        pos_ghost = self.board.get_pixels_of_cell(self.current.ghost_row ,self.current.ghost_col)

        self.current.draw_normal(surface, pos_normal)
        self.current.draw_ghost(surface, pos_ghost)

    def set_preview_count(self, count: int) -> None:
        """
        Actualiza dinámicamente la cantidad de piezas que se muestran en la vista previa.
        Args:
            count (int): Número entero positivo de piezas a mostrar en la preview.
        """
        if count < 0:
            raise ValueError(f"Gameboard Controller: No es posible asignar un número menor a 0 a preview count")
        
        self.preview.count = count

    def calculate_ghost_position(self) -> None:
        """
        Calcula la posición fantasma utilizando el movimiento vertical hasta que no sea posible.
        
        Returns:
            Tuple[int,int]: La fila y columna de la posición fantasma.
        """ 

        if self.current.col == self.current.ghost_col and self.current.rot == self.current.ghost_rot:
            return
        
        row = self.current.row

        # Mueve la pieza hacia abajo hasta que no pueda caer más
        while self.board.is_valid_move(self.current, row + 1, self.current.col):
            row += 1

        self.current.ghost_row = row
        self.current.ghost_col = self.current.col
        self.current.ghost_rot = self.current.rot
"""

1. fall_delay
    Clase relacionada: GravityStrategy
    Método relacionado: get_fall_delay(self.score.level)
    Calcula el retraso de la caída de la pieza según el nivel del jugador.

    
(!) 2. set_preview_count(self, count: int)
    Clase relacionada: PiecesPreview
    Actualiza la cantidad de piezas a mostrar en la vista previa.

(!) 3. spawn_piece(self)
    Clases relacionadas: PieceBag, Piece, PiecesPreview
    Genera y coloca una nueva pieza en el tablero, también actualiza la vista previa.

(?) FUERA PIECE
4. draw(self, surface: Surface, pieces: "PieceDataType")
    Clases relacionadas: Board, PiecesPreview, Piece
    Dibuja el tablero, las piezas activas y la vista previa.

    
5. resolve_piece_lock(self)
    Clases relacionadas: Board, Score
    Bloquea la pieza en el tablero, elimina líneas y actualiza el puntaje.

(!) 6. can_piece_move(self, dr: int, dc: int)
    Clase relacionada: Board
    Verifica si la pieza puede moverse a una nueva posición sin colisionar.

(!) 7. try_move_piece_to(self, dr: int, dc: int)
    Clase relacionada: Board, Piece
    Intenta mover la pieza activa por un desplazamiento dado.

(!) 8. try_fall_piece(self)
    Clase relacionada: Board, Piece
    Deja caer la pieza por un espacio si es posible (gravedad).

(!) 9. try_soft_drop_piece(self)
    Clase relacionada: Board, Piece
    Realiza un "soft drop" (deja caer la pieza una celda) y otorga puntos.

(!) 10. try_hard_drop_piece(self)
    Clase relacionada: Board, Piece
    Realiza un "hard drop" (deja caer la pieza inmediatamente al fondo del tablero).

(!) 11. try_rotate_piece(self, direction: int = 1)
    Clases relacionadas: Board, Piece
    Intenta rotar la pieza activa y valida el resultado.


(!) 12. set_ghost_position(self)
    Clase relacionada: Board, Piece
    Calcula la posición fantasma (donde la pieza caerá sin colisiones).

13. update(self, dt: float)
    Clases relacionadas: Board, Piece, LockStrategy, GravityStrategy
    Actualiza el estado del juego, controlando la caída de la pieza y la colisión con el fondo.

14. is_game_over(self)
    Clase relacionada: Piece, Board
    Verifica si el juego ha terminado (si la pieza recién generada colisiona).
"""