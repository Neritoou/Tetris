import pygame
from typing import TYPE_CHECKING
from src.states.game_state import GameState
from src.states.types import StateID, OverlayType
from src.constants import SCREEN_CENTER_W
from src.ui import UIManager, UIMenu, UILabel

if TYPE_CHECKING:
    from src.core.game import Game

class GameOverState(GameState):
    """Estado de Game Over que se superpone al perder la partida."""
    def __init__(self, game: "Game", final_score: int):
        super().__init__(game)

        font_title = self.game.resources.get_font("Estandar", 100)
        font_score = self.game.resources.get_font("Estandar", 48)
        font_menu = self.game.resources.get_font("Estandar", 48)

        options = [
            ("REINTENTAR", self._on_retry),
            ("VOLVER AL MENU", self._on_menu),
            ("SALIR", self._on_exit)
        ]

        self.title = UILabel("game_title", SCREEN_CENTER_W, 200, "GAME OVER", font_title, (255, 0, 0))
        self.score_text = UILabel("final_score", SCREEN_CENTER_W, 290, f"Puntuacion final: {final_score}", font_score)
        
        self.menu = UIMenu("game_over_menu", SCREEN_CENTER_W, 410,
                           options, font_menu, spacing=70, center_text=True)
        
        self.ui: UIManager = UIManager()
        self.ui.add_element(self.title)
        self.ui.add_element(self.score_text)
        self.ui.add_element(self.menu)
    
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        pass
    
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if self.game.input.is_action_pressed("ui", "up"):
            self.menu.move_up()
        elif self.game.input.is_action_pressed("ui", "down"):
            self.menu.move_down()
        elif self.game.input.is_action_pressed("ui", "select"):
            self.menu.execute_selected()
    
    def update(self, dt: float) -> None:
        self.ui.update(dt)
    
    def render(self, surface: pygame.Surface) -> None:
        # Fondo semitransparente
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        self.ui.render(surface)
    

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.SEMITRANSPARENT
    
    @property
    def is_transient(self) -> bool:
        return False
    


    # --- Callbacks ---
    def _on_retry(self):
        """Comienza una nueva partida."""
        config = self.game.gameplay_config.data
        ruleset = config["rulesets"]["custom"]
        self.game.state.change(StateID.PLAY, session_data=config, ruleset=ruleset)
    
    def _on_menu(self):
        """Vuelve al menú principal."""
        self.game.state.change(StateID.MENU)
    
    def _on_exit(self):
        """Detiene y cierra la ventana del juego."""
        self.game.stop()