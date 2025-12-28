import pygame
import numpy as np
from .piece import Piece
from ..constants.tetris_values import ROWS, COLS, BLOCK_H, BLOCK_W

class Board:
    def __init__(self, grid_surface: pygame.Surface, block_surface: pygame.Surface) -> None:
        self.rows = ROWS
        self.cols = COLS

        self.grid: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)
        self.grid_surface = grid_surface

        self.width = self.grid_surface.get_width()
        self.height = self.grid_surface.get_height()
        self.x = 0
        self.y = 0

        self.cell_width: int = BLOCK_W
        self.cell_height: int = BLOCK_H
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
        surface.blit(self.grid_surface, (0, 0))

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0:
                    x: int = c * self.cell_width
                    y: int = r * self.cell_height
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
