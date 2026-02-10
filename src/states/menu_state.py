import pygame
from typing import TYPE_CHECKING

from .state_id import StateID
from .game_state import GameState

from ..constants import SCREEN_CENTER_W
from ..core import OverlayType
from ..ui import UIManager, UIMenu, UILabel

if TYPE_CHECKING:
    from src.core.game import Game

class MenuState(GameState):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        options_list =[
            ("JUGAR", self._on_play),
            ("OPCIONES", self._on_config),
            ("CREDITOS", self._on_credits),
            ("SALIR", self._on_exit)
        ]

        self.font1 = self.game.resources.get_font("Estandar", 150)
        self.font2 = self.game.resources.get_font("Estandar", 48)

        self.title = UILabel("game_title", SCREEN_CENTER_W, 120, "TETRIS", self.font1, (50, 205, 50))
        self.title.center_at(SCREEN_CENTER_W)

        self.menu = UIMenu(
            "main_menu", SCREEN_CENTER_W, 360, options_list,
            self.font2, spacing=80, center_text=True
            )
        
        self.ui: UIManager = UIManager()
        self.ui.add_element(self.title)
        self.ui.add_element(self.menu)
        
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        return

    def update(self, dt: float) -> None:
        self.ui.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        self.ui.render(surface)

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if not self.menu.enabled:
            return

        if self.game.input.is_action_pressed("ui", "up"):
            self.menu.move_up()
        if self.game.input.is_action_pressed("ui", "down"):
            self.menu.move_down()
        if self.game.input.is_action_pressed("ui", "select"):
            self.menu.execute_selected()
            
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False
    


    # Callbacks
    def _on_play(self):
        config = self.game.gameplay_config.data
        ruleset = config["rulesets"]["custom"]

        self.game.state.change(StateID.PLAY, session_data = config, ruleset = ruleset)
    
    def _on_config(self):
        print("ESCENA DE CONFIGURACIONES")

    def _on_credits(self):
        print("ESCENA DE CREDITOS")
    
    def _on_exit(self):
        self.game.stop()