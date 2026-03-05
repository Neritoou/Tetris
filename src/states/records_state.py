import pygame
from typing import TYPE_CHECKING

from src.states.game_state import GameState
from src.states.types import OverlayType
from src.constants import SCREEN_SIZE, MAX_RECORDS
from src.database.types import RulesetName, Record
from src.ui import UIManager, UILabel, UIHintBar
from src.util import get_hint_key

if TYPE_CHECKING:
    from src.core.game import Game


# ── Paleta ─────────────────────────────────────────────────────────────────────
_COLOR_BG         = (23, 23, 23)
_COLOR_TITLE      = (130, 59, 188)
_COLOR_TAB_ACTIVE = (130, 59, 188)
_COLOR_TAB_IDLE   = (90, 90, 90)
_COLOR_HEADER     = (130, 59, 188)
_COLOR_DIVIDER    = (60, 60, 60)
_COLOR_GOLD       = (255, 215, 0)
_COLOR_SILVER     = (192, 192, 192)
_COLOR_BRONZE     = (205, 127, 50)
_COLOR_NORMAL     = (200, 200, 200)
_COLOR_DIM        = (110, 110, 110)
_COLOR_EMPTY      = (90, 90, 90)
_COLOR_HIGHLIGHT  = (40, 30, 55)

# ── Layout ─────────────────────────────────────────────────────────────────────
_ROW_H           = 58
_RECORDS_START_Y = 245

_MARGIN = 60
_COL_DEFS: dict[str, tuple[int, int]] = {   # (x_inicial, ancho)
    "rank":     (_MARGIN,        80),
    "score":    (_MARGIN + 80,  190),
    "lines":    (_MARGIN + 270, 150),
    "level":    (_MARGIN + 420, 150),
    "tetrises": (_MARGIN + 570, 160),
    "date":     (_MARGIN + 730, 174),
}
_HEADERS: dict[str, str] = {
    "rank":     "TOP",
    "score":    "Puntuación",
    "lines":    "Líneas",
    "level":    "Nivel",
    "tetrises": "Tetrises",
    "date":     "Fecha",
}

_Color = tuple[int, int, int]


class RecordsState(GameState):
    """
    Tabla de records organizada por ruleset.

    Muestra hasta MAX_RECORDS entradas sin paginado.
    Navegación: ← / → cambia de ruleset, ESC vuelve al estado anterior.
    """

    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.w, self.h = SCREEN_SIZE

        self._rulesets: list[RulesetName] = list(game.database.rulesets.keys())
        self._ruleset_cursor: int = 0
        self._cached: list[Record] = []

        self._build_fonts()
        self._build_ui()

    # ── GameState ───────────────────────────────────────────────────────────────

    def on_enter(self) -> None:
        self._cache_records()

    def on_exit(self) -> None:
        pass

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        inp = self.game.input

        if inp.is_action_pressed("ui", "left"):
            self._ruleset_cursor = (self._ruleset_cursor - 1) % len(self._rulesets)
            self.game.audio.play_sfx("Scroll")
            self._cache_records()

        elif inp.is_action_pressed("ui", "right"):
            self._ruleset_cursor = (self._ruleset_cursor + 1) % len(self._rulesets)
            self.game.audio.play_sfx("Scroll")
            self._cache_records()

        if inp.is_action_pressed("ui", "back"):
            self.game.audio.play_sfx("Select")
            self.game.state.exit_current()

    def update(self, dt: float) -> None:
        self.ui.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(_COLOR_BG)
        self.ui.render(surface)
        self._draw_tabs(surface)
        self._draw_table(surface)

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.FULLSCREEN

    @property
    def is_transient(self) -> bool:
        return False

    # ── Construcción ────────────────────────────────────────────────────────────

    def _build_fonts(self) -> None:
        get = self.game.resources.get_font
        self.fonts: dict[str, pygame.font.Font] = {
            "title":  get("Estandar", 70),
            "tab":    get("Estandar", 40),
            "header": get("Estandar", 30),
            "record": get("Estandar", 30),
            "hints":  get("Estandar", 25),
            "empty":  get("Estandar", 25),
        }

    def _build_ui(self) -> None:
        ctrl = self.game.controls_config
        self.ui = UIManager()
        self.ui.add_element(
            UILabel("records_title", self.w // 2, 20, "Records", self.fonts["title"], _COLOR_TITLE)
        )
        self.ui.add_element(
            UIHintBar(
                "records_hints",
                self.fonts["hints"],
                [
                    (f"{get_hint_key(ctrl, 'left')} / {get_hint_key(ctrl, 'right')}", "Navegar"),
                    (get_hint_key(ctrl, "back"), "Volver"),
                ],
                midbottom=(self.w // 2, self.h - 5),
            )
        )

    # ── Cache ────────────────────────────────────────────────────────────────────

    def _cache_records(self) -> None:
        """Carga los records del ruleset activo desde la base de datos."""
        self._cached = self.game.database.get_records(self._rulesets[self._ruleset_cursor])

    # ── Dibujo ──────────────────────────────────────────────────────────────────

    def _draw_tabs(self, surface: pygame.Surface) -> None:
        tab_y = 120
        step  = self.w // (len(self._rulesets) + 1)

        for i, ruleset in enumerate(self._rulesets):
            active = i == self._ruleset_cursor
            color  = _COLOR_TAB_ACTIVE if active else _COLOR_TAB_IDLE
            text   = self.fonts["tab"].render(ruleset.value.upper(), True, color)
            tx     = step * (i + 1) - text.get_width() // 2
            surface.blit(text, (tx, tab_y))

            if active:
                line_y = tab_y + text.get_height() + 3
                pygame.draw.line(surface, color, (tx, line_y), (tx + text.get_width(), line_y), 2)

    def _draw_table(self, surface: pygame.Surface) -> None:
        header_y = _RECORDS_START_Y - 50

        # Cabeceras
        for key, label in _HEADERS.items():
            col_x, col_w = _COL_DEFS[key]
            surf = self.fonts["header"].render(label, True, _COLOR_HEADER)
            surface.blit(surf, (col_x + (col_w - surf.get_width()) // 2, header_y))

        pygame.draw.line(surface, _COLOR_DIVIDER, (50, header_y + 38), (self.w - 50, header_y + 38), 1)

        # Sin records
        if not self._cached:
            surf = self.fonts["empty"].render("Sin records todavía.", True, _COLOR_EMPTY)
            ey   = _RECORDS_START_Y + (MAX_RECORDS * _ROW_H) // 2 - surf.get_height() // 2
            surface.blit(surf, (self.w // 2 - surf.get_width() // 2, ey))
            return

        # Filas
        for i, record in enumerate(self._cached):
            rank       = i + 1
            row_y      = _RECORDS_START_Y + i * _ROW_H
            rank_color, row_color = self._rank_colors(rank)

            if rank <= 3:
                hl = pygame.Surface((self.w - 100, _ROW_H - 6), pygame.SRCALPHA)
                hl.fill((*_COLOR_HIGHLIGHT, 180))
                surface.blit(hl, (50, row_y - 2))

            self._blit_col(surface, f"#{rank}",           "record", "rank",     row_y, rank_color)
            self._blit_col(surface, f"{record.score:,}",  "record", "score",    row_y, row_color)
            self._blit_col(surface, str(record.lines),    "record", "lines",    row_y, row_color)
            self._blit_col(surface, str(record.level),    "record", "level",    row_y, row_color)
            self._blit_col(surface, str(record.tetrises), "record", "tetrises", row_y, row_color)
            self._blit_col(surface, record.date,          "record", "date",     row_y, row_color)

    # ── Helpers ─────────────────────────────────────────────────────────────────

    def _rank_colors(self, rank: int) -> tuple[_Color, _Color]:
        if rank == 1: return _COLOR_GOLD,   _COLOR_GOLD
        if rank == 2: return _COLOR_SILVER, _COLOR_SILVER
        if rank == 3: return _COLOR_BRONZE, _COLOR_BRONZE
        return _COLOR_DIM, _COLOR_NORMAL

    def _blit_col(self, surface: pygame.Surface, text: str, font_key: str, col_key: str, y: int, color: _Color) -> None:
        col_x, col_w = _COL_DEFS[col_key]
        surf = self.fonts[font_key].render(text, True, color)
        surface.blit(surf, (col_x + (col_w - surf.get_width()) // 2, y))