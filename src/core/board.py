import pygame
import numpy as np
from piece import Piece

class Board:
    def __init__(self, rows: int, cols: int, cell_w: int, cell_h: int, block_surface: pygame.Surface) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_w
        self.cell_height = cell_h

        self.grid: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)
        self.block_surface = block_surface

        self.active_piece: Piece | None = None

    def spawn_piece(self, piece: Piece):
        self.active_piece = piece        
        piece.center_piece(self.cols)

    def lock_piece(self):
        if not self.active_piece:
            return
        
        for r, c in self.active_piece.get_cells():
            self.grid[r, c] = 1
        self.active_piece.state = "placed"
        self.active_piece = None

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
    
    def try_fall_piece(self) -> bool:
        if not self.active_piece:
            return False
        
        if self.try_move(1, 0):
            return True
        self.lock_piece()
        return False

    def draw(self, surface: pygame.Surface):
        for r, c in np.ndenumerate(self.grid):
            if self.grid[r][c]:
                x = c * self.cell_width
                y = r * self.cell_height
                surface.blit(self.block_surface, (x, y))
        
        if self.active_piece:
            self.active_piece.draw(surface)
        

    def is_game_over(self) -> bool:
        if not self.active_piece:
            return False
        if self.is_valid(self.active_piece):
            return False
        return True
    
    def clear_lines(self):
        pass
        # (!) falta implementar la logica, sin esto no se eliminan las lineas y haria game over mas rapido

    def try_rotate(self):
        if not self.active_piece:
            return False
        # (!) falta implementar logica porque quiero intentar los wall kicks, pero para eso necesito ir probando que funcione
