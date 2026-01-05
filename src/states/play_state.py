import pygame
from typing import Tuple, List, TYPE_CHECKING

from .game_state import GameState
from ..core import OverlayType, Piece, Board, PieceBag
from ..constants import PIECE_DEFINITIONS, ROWS, COLS, BLOCK_W, BLOCK_H, BOARD_X, BOARD_Y

if TYPE_CHECKING:
    from src.core.game import Game

class PlayState(GameState):
    """
    Estado principal del juego donde ocurren todas las acciones del Tetris.

    Coordina la interacción entre el tablero (Board), el generador de piezas
    (PieceBag) y la entrada del usuario.
    """
    def __init__(self, game: "Game"):
        super().__init__(game)

        self.fall_timer = 0.0
        self.fall_delay = 0.3

        self.lock_delay = 0.05
        self.lock_timer = 0.0

        self.bag: PieceBag
        self.board: Board
        self.current_piece: Piece | None
        self.next_pieces = [] # (!) Ver que se hará con esto

    def on_enter(self) -> None:
        self.bag = PieceBag(PIECE_DEFINITIONS, 3)

        board_surface = self.game.resources.get_image("Board")
        self.board = Board(ROWS, COLS, board_surface, BLOCK_W, BLOCK_H, BOARD_X, BOARD_Y)
        
        self.spawn_new_piece()

    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        if self.game.input.is_key_pressed("play", "move_left"):
            if self.try_move_to(0, -1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "move_right"):
            if self.try_move_to(0, 1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "move_down"):
            if self.try_move_to(1, 0):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "rotate_piece_right"):
            if self.try_rotate(1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "lock_piece"):
            while self.try_fall_piece():
                pass 
            self.board.lock_piece(self.current_piece)
            self.current_piece = None
            lines_cleared = self.board.clear_lines()
            self.lock_timer = 0.0

        return 
    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))
        self.board.draw(surface, self.game.resources.get_pieces()) 
        
        # Dibuja la Pieza activa actualmente
        if self.current_piece:
            
            pos = self.board.get_pixels_of_cell(self.current_piece.row, self.current_piece.col)
            r, c = self.get_ghost_position(self.current_piece)
            pos_ghost = self.board.get_pixels_of_cell(r,c)

            self.current_piece.draw_normal(surface, pos)
            self.current_piece.draw_ghost(surface, pos_ghost)
    
    def update(self, dt: float) -> None:
        # --- Genera una nueva pieza ---
        if not self.current_piece and self.bag is not None:
            self.spawn_new_piece()

            if self.is_game_over():
                print("Game Over.")
            return

        # --- Caída por gravedad ---
        self.fall_timer += dt
        if self.fall_timer >= self.fall_delay:
            self.fall_timer = 0.0
            
            if self.try_fall_piece():
                self.lock_timer = 0.0
                return
            self.lock_timer += dt
                
            if self.lock_timer >= self.lock_delay:
                self.board.lock_piece(self.current_piece)
                self.current_piece = None
                lines_cleared = self.board.clear_lines()
                self.lock_timer = 0.0

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False
    

    def spawn_new_piece(self) -> None:
        """Genera una nueva pieza de la bolsa y la coloca en la parte superior del tablero."""
        piece_name = self.bag.get_next_piece()
        piece_data = self.game.resources.get_piece(piece_name)
        self.current_piece = Piece(piece_name, piece_data)
        self.current_piece.center(self.board.cols)

     



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
        if not self.current_piece:
            return False
        
        new_row = self.current_piece.row + dr
        new_col = self.current_piece.col + dc

        if self.board.is_valid(self.current_piece, new_row, new_col):
            self.current_piece.move(dr, dc)
            return True
        return False
    
    def try_fall_piece(self) -> bool:
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
        if not self.current_piece:
            return False
        
        old_rot = self.current_piece.rot
        self.current_piece.rotate(direction)
        if self.board.is_valid(self.current_piece):
            return True
        
        # Si la rotación no es es válida, se revierte
        self.current_piece.rot = old_rot
        return False
    
        # (!) Intentar implementar los wall kicks

    def is_game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""
        if not self.current_piece:
            return False
        if self.board.is_valid(self.current_piece):
            return False
        return True
    
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
