import pygame
import numpy as np
from constants import tetris_values
from piece import Piece

FALL_INTERVAL = 0.3
fall_timer = 0

class Board:
    def __init__(self, rows: int, cols: int, cell_w: int, cell_h: int) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_w
        self.cell_height = cell_h

        self.grid: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)
        
        self.active_piece: Piece | None = None
        self.next_piece: Piece | None = None
        self.hold_piece: Piece | None = None

    def spawn_piece(self, piece: Piece):
        self.active_piece = piece

    def try_rotate(self):
        pass

    def lock_piece(self):
        if not self.active_piece:
            return
        
        for r, c in self.active_piece.get_cells():
            self.grid[r, c] = 1
        self.active_piece.state = "placed"
        self.active_piece = self.next_piece

    def is_valid(self, piece: Piece, row: int | None = None, col: int | None = None) -> bool:
        for r, c in piece.get_cells(row, col):
            if r < 0 or r >= self.rows:
                return False
            if c < 0 or c >= self.cols: 
                return False
            if self.grid[r, c]: 
                return False
        return True
    
    def try_move(self, dr: int, dc: int) -> bool:
        if not self.active_piece:
            return False
        
        new_row = self.active_piece.row + dr
        new_col = self.active_piece.col + dc

        if self.is_valid(self.active_piece, new_row, new_col):
            self.active_piece.move(dr, dc)
            return True
        return False
    
    def clear_lines(self):
        pass

    def draw(self, surface: pygame.Surface):
        pass
    
    """
    def try_fall_piece(rect: pygame.Rect, h, dt):
        global fall_timer
        global row_piece
        fall_timer += dt
        if fall_timer >= FALL_INTERVAL:
            fall_timer = 0
            return True
        return False

    def try_move(dx, dy):
        global col_piece, row_piece
        new_col = col_piece + dx
        new_row = row_piece + dy

        if valid_move(PIECES["S"], GRID_MATRIZ, new_row, new_col):
            col_piece = new_col
            row_piece = new_row

    def get_coords_of_piece_in_grid(piece, row, col):
        return ((GRID_X + col * CELL_W), GRID_Y + row * CELL_H)

    
    def get_piece_matrix(self, name: str, rotation: int = 0) -> np.ndarray:
        if not self.piece_manager:
            raise RuntimeError("PieceManager no cargado")
        return self.piece_manager.get_matrix(name, rotation)

    def get_piece_surface(self, name: str, rotation: int = 0) -> pygame.Surface:
        if not self.piece_manager:
            raise RuntimeError("PieceManager no cargado")
        return self.piece_manager.get_surface(name, rotation)
    """