from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .movement_manager import MovementManager
    from .piece_manager import PieceManager

class UpdateManager:
    def __init__(self, piece_manager: PieceManager, movement_manager: MovementManager):
        self.piece = piece_manager
        self.movement = movement_manager

    def update(self, dt: float) -> None:
        if self.game_over:
            return
        
        if self.piece.current.is_locked():
            self.piece.spawn()
            if not self.movement.can_piece_move(1,0):
                self.game_over = True
            return

      # --- Actualiza la caída ---
        self.fall_timer += dt
        if self.fall_timer >= self.fall_delay:
            self.fall_timer = 0.0
            self.movement.try_fall_piece()
                
        # --- Actualiza el lock ---
        is_colliding = not self.movement.can_piece_move(1,0)
        self.movement.lock.update(dt, is_colliding)

        # --- Bloquea la pieza si está colisionando ---
        if is_colliding and self.lock.is_locked():
            self.lock_piece()

    def is_game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""
        return self.game_over 
    
    def start(self) -> None:
        self.piece.spawn()


    def lock_piece(self) -> None:
            """Bloquea la pieza en el tablero, elimina las líneas completas, y verifica si el tablero está vacío."""
            self.board.lock_piece(self.piece)
            self.piece.set_locked()
            lines = self.board.clear_lines()
            perfect_clear = self.board.is_empty() # VER SI SE USARÁ
            
            self.score.update(lines,"normal")

            self.lock.timer = 0.0

        