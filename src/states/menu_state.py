import pygame
from typing import TYPE_CHECKING

from .state_id import StateID
from .game_state import GameState

from ..core import OverlayType
from ..ui import UIManager

if TYPE_CHECKING:
    from src.core.game import Game

class MenuState(GameState):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.ui: UIManager = UIManager()

        self.font = self.game.resources.get_font("Estandar", 48)

        self.text_play = self.font.render("JUGAR", True, (255, 255, 255))
        self.text_play_rect = self.text_play.get_rect()
        self.text_play_rect.topleft = (500, 100)

        self.text_credits = self.font.render("CREDITOS", True, (255, 255, 255))
        self.text_credits_rect = self.text_credits.get_rect()
        self.text_credits_rect.topleft = (500, 175)

        self.text_exit = self.font.render("SALIR", True, (255, 255, 255))
        self.text_exit_rect = self.text_exit.get_rect()
        self.text_exit_rect.topleft = (500, 250)

        self.text_option = self.font.render(">", True, (255, 255, 255))

        self.option = 0
        
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        return

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.text_play, self.text_play_rect)
        surface.blit(self.text_credits, self.text_credits_rect)
        surface.blit(self.text_exit, self.text_exit_rect)

        surface.blit(self.text_option, (360, 100 + self.option % 3 * 75))
    
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        for element in self.ui.elements:
            if element.enabled:
                return


        if self.game.input.is_action_pressed("ui", "down"):
            self.option += 1
            if self.option >= 3:
                self.option = 0
        if self.game.input.is_action_pressed("ui", "up"):
            self.option -= 1
        if self.game.input.is_action_pressed("ui", "select"):
            if self.option % 3 == 0:
                config = self.game.gameplay_config.data
                ruleset = config["rulesets"]["custom"]
                self.game.state.change(StateID.PLAY, session_data = config, ruleset = ruleset)
            elif self.option % 3 == 1:
                print("ESCENA DE CREDITOS")
            elif self.option % 3 == 2:
                self.game.stop()
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False