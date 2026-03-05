import pygame
from typing import TYPE_CHECKING
from src.states.types import OverlayType
from src.constants.tetris_values import SCREEN_SIZE

from src.states.game_state import GameState

if TYPE_CHECKING:
    from src.core.game import Game
    from src.states.play_state import PlayState

COUNTDOWN_STEPS = ["3", "2", "1", "GO!"]
STEP_DURATION   = 1.0

class CountdownState(GameState):
    """
    Estado de cuenta regresiva antes de que el juego comience.
    Muestra 3 → 2 → 1 → GO!
    """

    def __init__(self, game: "Game", playstate: "PlayState"):
        super().__init__(game)
        self.play_state = playstate

        self._step_index = 0
        self._timer = 0.0

        self._overlay = pygame.Surface(SCREEN_SIZE)
        self._overlay.set_alpha(150)
        self._overlay.fill((0, 0, 0))

        self.font = self.game.resources.get_font("Estandar", 100)

    def on_enter(self) -> None:
        self.game.audio.stop_music()
        self.game.audio.play_sfx("Countdown")


    def on_exit(self) -> None:
        self.play_state._start_game()

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, dt: float) -> None:
        self._timer += dt

        if self._timer >= STEP_DURATION:
            self._timer = 0.0
            self._step_index += 1

            if self._step_index >= len(COUNTDOWN_STEPS):
                self.game.state.exit_current()

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._overlay, (0, 0))

        text = COUNTDOWN_STEPS[min(self._step_index, len(COUNTDOWN_STEPS) - 1)]
        text_surf = self.font.render(text, True, (255, 255, 255))

        rect = text_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text_surf, rect)

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.SEMITRANSPARENT

    @property
    def is_transient(self) -> bool:
        return False