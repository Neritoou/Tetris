import pygame
from typing import TYPE_CHECKING
from src.states.game_state import GameState
from src.states.types import StateID, OverlayType
from src.constants import SCREEN_CENTER_W
from src.ui import UIMenu, UILabel, UIManager

if TYPE_CHECKING:
    from src.core.game import Game
    from src.database import RulesetName

class PauseState(GameState):
    """Estado de pausa que se superpone al juego."""
    def __init__(self, game: "Game", ruleset_name: "RulesetName"):
        super().__init__(game)
        self.ruleset_name = ruleset_name

        self.font_title = self.game.resources.get_font("Estandar", 100)
        self.font_menu  = self.game.resources.get_font("Estandar", 48)
        
        self.title = UILabel("pause_title", SCREEN_CENTER_W, 200,
            "PAUSA", self.font_title, (130, 59, 188))

        options = [
            ("CONTINUAR",      self._on_resume),
            ("REINICIAR",      self._on_restart),
            ("VOLVER AL MENU", self._on_menu),
            ("OPCIONES",       self._on_options)
        ]
        
        self.menu = UIMenu("pause_menu", SCREEN_CENTER_W, 350,
            options, self.font_menu, spacing=80, center_text=True)

        self.ui: UIManager = UIManager()
        self.ui.add_element(self.title)
        self.ui.add_element(self.menu)
    
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        pass
    
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if self.game.input.is_action_pressed("ui", "pause"):
            self._on_resume()
            return
        if self.game.input.is_action_pressed("ui", "up"):
            self.menu.move_up()
        elif self.game.input.is_action_pressed("ui", "down"):
            self.menu.move_down()
        elif self.game.input.is_action_pressed("ui", "select"):
            self.menu.execute_selected()
    
    def update(self, dt: float) -> None:
        self.ui.update(dt)
    
    def render(self, surface: pygame.Surface) -> None:
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
    def _on_resume(self):
        self.game.state.exit_current()
    
    def _on_restart(self):
        config = self.game.gameplay_config.data
        ruleset = config["rulesets"][self.ruleset_name.value]
        self.game.state.clear()
        self.game.state.change(StateID.PLAY,
            session_data = config,
            ruleset      = ruleset,
            ruleset_name = self.ruleset_name,
        )
    
    def _on_options(self):
        print("Menú de opciones aún no implementado")
    
    def _on_menu(self):
        self.game.state.clear()
        self.game.state.change(StateID.MENU)