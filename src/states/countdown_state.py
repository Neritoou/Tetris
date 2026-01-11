import pygame
import time
from typing import List, TYPE_CHECKING
from ..core import OverlayType

from .game_state import GameState

if TYPE_CHECKING:
    from src.core.game import Game
    from .play_state import PlayState

class CountdownState(GameState):
    """
    Estado de cuenta regresiva antes de que el juego comience.
    Muestra una cuenta regresiva y permite al jugador prepararse.
    """
    def __init__(self, game: "Game", playstate: "PlayState"):
        super().__init__(game)
        self.playstate = playstate
        self.time_left = 3 
        
        # (?) cambiar las fonts en dado caso por imagenes o por fonts del resource xyz
        self.font = pygame.font.SysFont("Consolas", 50)
    
    def on_exit(self) -> None:
        self.playstate._start_game()
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        pass

    def update(self, dt: float) -> None:
        """Actualiza la cuenta regresiva."""
        if self.time_left <= -0.5:
            self.game.state.exit_current()
            return
        
        self.time_left -= dt

    def render(self, surface: pygame.Surface) -> None:
        """Dibuja la cuenta regresiva en la pantalla."""
        if self.time_left > 0:
                countdown_text = self.font.render(f"Starting in {str(max(1, int(self.time_left) + 1))}", True, (255, 255, 255))
        else:
            countdown_text = self.font.render(f"¡GO!", True, (255, 255, 255))
        surface.blit(countdown_text, (surface.get_width() // 2 - countdown_text.get_width() // 2, surface.get_height() // 2 - countdown_text.get_height() // 2))

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.SEMITRANSPARENT

    @property
    def is_transient(self) -> bool:
        return False