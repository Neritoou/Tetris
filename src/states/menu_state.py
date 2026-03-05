import pygame
from typing import TYPE_CHECKING

from src.states.types import StateID, OverlayType
from src.states.game_state import GameState

from src.constants import SCREEN_CENTER_W
from src.ui import UIManager, UIMenu, UILabel

if TYPE_CHECKING:
    from src.core.game import Game

class MenuState(GameState):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        self._title = pygame.transform.scale_by(self.game.resources.get_image("Title"), 2.6)

        self._build_ui()
        
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        return

    def update(self, dt: float) -> None:
        self.ui.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.game.background, (0, 0))

        surface.blit(self._title, self._title.get_rect(centerx=SCREEN_CENTER_W, y=100))
        self.ui.render(surface)

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if self.game.input.is_action_pressed("ui", "up"):
            self.menu.move_up()
        elif self.game.input.is_action_pressed("ui", "down"):
            self.menu.move_down()
        elif self.game.input.is_action_pressed("ui", "select"):
            self.menu.execute_selected()
            
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False
    
    def _build_ui(self) -> None:
        font_menu = self.game.resources.get_font("Estandar", 48)

        options_list =[
            ("JUGAR", self._on_play),
            ("OPCIONES", self._on_config),
            ("SALIR", self._on_exit)
        ]

        self.menu = UIMenu(
            "main_menu", SCREEN_CENTER_W, 450, options_list,
            font_menu, spacing=20, center_text=True
            )
        
        self.ui: UIManager = UIManager()
        self.ui.add_element(self.menu)



    # --- Callbacks ---
    def _on_play(self):
        self.game.state.change(StateID.RULESET_SELECT)
    
    def _on_config(self):
        self.game.state.change(StateID.OPTIONS)
    
    def _on_exit(self):
        """Detiene y cierra la ventana del juego."""
        self.game.stop()