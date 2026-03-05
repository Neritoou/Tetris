import pygame
from typing import TYPE_CHECKING
from src.states.game_state import GameState
from src.core import GameBoardController
from src.constants import BOARD_X, BOARD_Y
from src.states.types import StateID, OverlayType
from src.util import ScreenShake, ShakeDirection

if TYPE_CHECKING:
    from src.core.game import Game
    from src.core.types import PieceDataType, BoardType, PiecesPreviewType
    from src.config.gameplay import GameplayConfigType, GameplayRulesetType
    from src.database import RulesetName


class PlayState(GameState):
    def __init__(self, game: "Game", session_data: "GameplayConfigType",
                 ruleset: "GameplayRulesetType", ruleset_name: "RulesetName"):
        super().__init__(game)
        self._started = False
        self._game_over_triggered = False
        self.session_config = session_data
        self.ruleset = ruleset
        self.ruleset_name = ruleset_name
        self.pieces: "PieceDataType"
        self.session: GameBoardController
        self._shake = ScreenShake(intensity=4, duration=0.2)
        self._temp_surface = pygame.Surface(game.surface.get_size())

    def on_enter(self) -> None:
        self.pieces       = self.game.resources.get_pieces()
        self._board     = self.game.resources.get_image("Board")

        board_surface = pygame.Surface((270, 600), pygame.SRCALPHA)

        board_config: "BoardType" = {
            "surface": board_surface,
            "pos_x":   BOARD_X + 163,
            "pos_y":   BOARD_Y,
        }
        preview_config: "PiecesPreviewType" = {
            "pos_x":         BOARD_X + 480,
            "pos_y":         BOARD_Y + 90,
            "max_width":     80,
            "margin":        8,
            "preview_count": self.session_config["general"]["preview_count"],
        }

        self.session = GameBoardController(
            self.session_config, self.ruleset,
            self.pieces, board_config, preview_config
        )
        self.game.state.change(StateID.COUNTDOWN, playstate=self)

    def on_exit(self) -> None:
        pass

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if not self._started or self.session.is_game_over():
            return

        if self.game.input.is_action_pressed("ui", "pause"):
            self.game.state.change(StateID.PAUSE, ruleset_name=self.ruleset_name)
            return

        if self.game.input.is_action_pressed("play", "move_left"):
            self.game.audio.play_sfx("MovePiece")
            self.session.move_left()
        if self.game.input.is_action_pressed("play", "move_right"):
            self.game.audio.play_sfx("MovePiece")
            self.session.move_right()
        if self.game.input.is_action_pressed("play", "move_down"):
            self.game.audio.play_sfx("MovePiece")
            self.session.soft_drop()
        if self.game.input.is_action_pressed("play", "rotate_right"):
            self.game.audio.play_sfx("RotatePiece")
            self.session.rotate_right()
        if self.game.input.is_action_pressed("play", "rotate_left"):
            self.game.audio.play_sfx("RotatePiece")
            self.session.rotate_left()
        if self.game.input.is_action_pressed("play", "hard_drop"):
            self.game.audio.play_sfx("LockPiece")
            self.session.hard_drop()
        if self.game.input.is_action_pressed("play", "hold"):
            self.game.audio.play_sfx("RotatePiece")
            self.session.hold()

    def update(self, dt: float) -> None:
        if not self._started:
            return

        self.session.update(dt)
        if self.session.consume_lock_event():
            self._shake.trigger(ShakeDirection.VERTICAL)

        self._shake.update(dt)

        if self.session.is_game_over() and not self._game_over_triggered:
            self.game.audio.stop_music()
            self._game_over_triggered = True
            self.game.state.change(
                StateID.GAME_OVER,
                ruleset_name = self.ruleset_name,
                stats        = self.session.final_stats,
            )

    def render(self, surface: pygame.Surface) -> None:
        target = self._temp_surface if self._shake.is_active else surface

        target.blit(self.game.background, (0, 0))
        target.blit(self._board, (BOARD_X, BOARD_Y))

        self.session.draw(target, self.pieces)

        if self._shake.is_active:
            surface.fill((0, 0, 0))
            surface.blit(target, self._shake.offset)

    def _start_game(self) -> None:
        path = self.game.resources.get_music_path("GameplayMusic")
        self.game.audio.play_music(path)

        self._started = True
        self.session.start()

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False