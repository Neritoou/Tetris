import pygame
from typing import TYPE_CHECKING
from src.states.game_state import GameState
from src.core import GameBoardController
from src.constants import BOARD_X, BOARD_Y, SCREEN_H, SCREEN_W
from src.states.types import StateID, OverlayType
from src.util import ScreenShake, ShakeDirection, get_hint_key
from src.ui import UIFloatingLabel, UILabel, UIManager, UIHintBar

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

        self._build_ui()

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

        center_x = board_config["pos_x"] + 135
        center_y = board_config["pos_y"] + 300
        
        font = self.game.resources.get_font("Estandar", 40) # O la fuente que prefieras
        
        self._floating_score = UIFloatingLabel(
            "score_popup", center_x, center_y, font,
            float_speed=60.0, fade_duration=1.2, spawn_offset=20.0
        )
        self.ui.add_element(self._floating_score)

        self.game.state.change(StateID.COUNTDOWN, playstate=self)

    def on_exit(self) -> None:
        pass

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if not self._started or self.session.is_game_over():
            return

        if self.game.input.is_action_pressed("ui", "pause") or self.game.input.is_action_pressed("ui","back"):
            self.game.state.change(StateID.PAUSE, ruleset_name=self.ruleset_name)
            return

        if self.game.input.is_action_pressed("play", "move_left"):
            if self.session.move_left():
                self.game.audio.play_sfx("MovePiece")

        if self.game.input.is_action_pressed("play", "move_right"):
            if self.session.move_right():
                self.game.audio.play_sfx("MovePiece")

        if self.game.input.is_action_pressed("play", "move_down"):
            if self.session.soft_drop():
                self.game.audio.play_sfx("MovePiece")

        if self.game.input.is_action_pressed("play", "rotate_right"):
            if self.session.rotate_right():
                self.game.audio.play_sfx("RotatePiece")

        if self.game.input.is_action_pressed("play", "rotate_left"):
            if self.session.rotate_left():
                self.game.audio.play_sfx("RotatePiece")

        if self.game.input.is_action_pressed("play", "hard_drop"):
            self.session.hard_drop()
            #self.game.audio.play_sfx("LockPiece")

        if self.game.input.is_action_pressed("play", "hold") and self.ruleset_name == "guideline":
            if self.session.hold():
                self.game.audio.play_sfx("RotatePiece")

    def update(self, dt: float) -> None:
        if not self._started:
            return

        self.session.update(dt)
        self._floating_score.update(dt)

        self.val_score.set_text(str(self.session.current_score))
        self.val_level.set_text(str(self.session.current_level))
        self.val_lines.set_text(str(self.session.total_lines_cleared))

        if self.session.consume_lock_event():
            self.game.audio.play_sfx("LockPiece")
            self._shake.trigger(ShakeDirection.VERTICAL)

            points = self.session.last_score_gained
            lines = self.session.last_lines_cleared

            if lines > 0:
                if lines >= 4:
                    self.game.audio.play_sfx("FourRows")
                    color = (255, 215, 0)
                else:
                    self.game.audio.play_sfx("DeleteRow")
                    color = (255, 255, 255)

                self._floating_score.show(f"+{points}", color)

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

        self.ui.render(target)

        if self._shake.is_active:
            surface.fill((0, 0, 0))
            surface.blit(target, self._shake.offset)

    def _start_game(self) -> None:
        path = self.game.resources.get_music_path("GameplayMusic")
        self.game.audio.play_music(path)

        self._started = True
        self.session.start()

    def _build_ui(self) -> None:
        self.ui = UIManager()
        
        font_title = self.game.resources.get_font("Estandar", 30)
        font_value = self.game.resources.get_font("Estandar", 30)
        font_hint = self.game.resources.get_font("Estandar", 25)

        stats_x = BOARD_X + 10  
        base_y = BOARD_Y + 340
        spacing = 90 # Espacio vertical entre cada bloque de texto

        # SCORE
        self.ui.add_element(UILabel("lbl_score_txt", stats_x, base_y, "SCORE", font_title, (180, 180, 180), center=False))
        self.val_score = UILabel("val_score", stats_x, base_y + 30, "0", font_value, (255, 255, 255), center=False)
        self.ui.add_element(self.val_score)

        # LEVEL
        self.ui.add_element(UILabel("lbl_lvl_txt", stats_x, base_y + spacing, "LEVEL", font_title, (180, 180, 180), center=False))
        self.val_level = UILabel("val_lvl", stats_x, base_y + spacing + 30, "1", font_value, (255, 255, 255), center=False)
        self.ui.add_element(self.val_level)

        # LINES
        self.ui.add_element(UILabel("lbl_lines_txt", stats_x, base_y + spacing * 2, "LINES", font_title, (180, 180, 180), center=False))
        self.val_lines = UILabel("val_lines", stats_x, base_y + spacing * 2 + 30, "0", font_value, (255, 255, 255), center=False)
        self.ui.add_element(self.val_lines)


        ctrl = self.game.controls_config
        self.ui.add_element(
            UIHintBar(
                "play_hints",
                font_hint,
                [
                    (f"{get_hint_key(ctrl, "pause")} / {get_hint_key(ctrl, "back")}", "Pausa"),
                ],
                midbottom=(SCREEN_W // 2, SCREEN_H - 5),
            )
        )
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False