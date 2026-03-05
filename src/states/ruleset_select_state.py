import pygame
from typing import TYPE_CHECKING

from src.states.game_state import GameState
from src.states.types import StateID, OverlayType

from src.constants import SCREEN_CENTER_W, SCREEN_H
from src.ui import UIManager, UILabel, UIButtonMenu
from src.util import get_hint_key

if TYPE_CHECKING:
    from src.core.game import Game

GRAVITY_DESCRIPTIONS = {
    "exponential": "Aumento suave y progresivo por nivel.",
    "for_levels":  "Aceleración clásica por niveles.",
    "fixed":       "Velocidad constante sin importar el nivel."
}

LOCK_DESCRIPTIONS = {
    "auto":            "Bloqueo inmediato al tocar el suelo.",
    "fixed":           "Breve pausa antes de bloquear.",
    "resettable":      "Mover o rotar la pieza retrasa el bloqueo.",
    "collision_delay": "El tiempo avanza solo mientras choca abajo."
}

class RulesetSelectState(GameState):
    def __init__(self, game: "Game"):
        super().__init__(game)

        self._config     = game.gameplay_config.data
        self._rulesets   = list(self._config["rulesets"].items())
        self._selected   = 0

        self._build_fonts()
        self._build_ui()
        self._update_details()

    def on_exit(self) -> None:
        pass

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if self.game.input.is_action_pressed("ui", "back"):
            self.game.state.change(StateID.MENU)
            return

        if self.game.input.is_action_pressed("ui", "left"):
            self._menu.move_up()
            self._selected = self._menu.selected_index
            self._update_details()

        if self.game.input.is_action_pressed("ui", "right"):
            self._menu.move_down()
            self._selected = self._menu.selected_index
            self._update_details()

        if self.game.input.is_action_pressed("ui", "select"):
            self._menu.execute_selected()

    def update(self, dt: float) -> None:
        self.ui.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((23, 23, 23))
        self.ui.render(surface)
        pygame.draw.rect(surface, (60, 60, 60), self._separator)
    
    def _build_fonts(self) -> None:
        self.fonts = {
            "title": self.game.resources.get_font("Estandar", 70),
            "btn": self.game.resources.get_font("Estandar", 48),
            "normal": self.game.resources.get_font("Estandar", 35),
            "small": self.game.resources.get_font("Estandar", 30)
        }
    
    def _build_ui(self) -> None:
        btn_base = self.game.resources.get_image("RulesetNormalBtn")
        btn_sel = self.game.resources.get_image("RulesetSelBtn")

        options = [
            (data["display_name"], self._make_select_callback(i))
            for i, (_, data) in enumerate(self._rulesets)
        ]

        self._title = UILabel(
            "rs_title", SCREEN_CENTER_W, 70,
            "SELECCIONA UN MODO", self.fonts["title"], (50, 205, 50)
        )

        self._menu = UIButtonMenu(
            "rs_menu", SCREEN_CENTER_W, 190,
            options, btn_base, btn_sel,
            self.fonts["btn"], text_color=(255, 255, 255), text_y=1,
            spacing=30, center_x=True, horizontal=True
        )

        hint_key = get_hint_key(self.game.controls_config, "back")

        self._hint = UILabel(
            "rs_hint", SCREEN_CENTER_W, SCREEN_H - 55,
            f"Presiona [{hint_key}] para volver al menu", self.fonts["small"], (100, 100, 100)
        )

        self._separator = pygame.Rect(SCREEN_CENTER_W - 268, 310, 500, 2)
    
        DETAIL_START_Y = 360
        DETAIL_SPACING = 60

        self._lbl_desc = UILabel("rs_desc", SCREEN_CENTER_W, DETAIL_START_Y, "", self.fonts["normal"], (180, 180, 180))
        self._lbl_gravity = UILabel("rs_gravity", 250, DETAIL_START_Y + DETAIL_SPACING + 40, "", self.fonts["small"], (255, 255, 255), center=False)
        self._lbl_lock = UILabel("rs_lock", 250, DETAIL_START_Y + 40 + DETAIL_SPACING * 2, "", self.fonts["small"], (255, 255, 255), center=False)
        self._lbl_hold = UILabel("rs_hold", 250, DETAIL_START_Y + 40 + DETAIL_SPACING * 3, "", self.fonts["small"], (255, 255, 255), center=False)

        self.ui = UIManager()
        self.ui.add_element(self._title)
        self.ui.add_element(self._menu)
        self.ui.add_element(self._lbl_desc)
        self.ui.add_element(self._lbl_gravity)
        self.ui.add_element(self._lbl_lock)
        self.ui.add_element(self._lbl_hold)
        self.ui.add_element(self._hint)
    
    def _make_select_callback(self, index: int):
        def callback():
            self._launch(index)
        return callback

    def _update_details(self) -> None:
        ruleset = self._rulesets[self._selected][1]

        gravity_type = ruleset["gravity_type"]
        lock_type    = ruleset["lock_type"]
        
        grav_desc = GRAVITY_DESCRIPTIONS.get(gravity_type, "")
        lock_desc = LOCK_DESCRIPTIONS.get(lock_type, "")

        hold_label = "Sí." if ruleset["hold"] else "No."

        self._lbl_desc.set_text(ruleset["description"])
    
        self._lbl_gravity.set_text(f"Gravedad: {grav_desc}")
        self._lbl_lock.set_text(f"Lock: {lock_desc}")
        self._lbl_hold.set_text(f"Hold: {hold_label}")
    
    def _launch(self, index: int) -> None:
            self.game.state.change(
            StateID.PLAY,
            session_data=self._config,
            ruleset=self._rulesets[index][1],
            ruleset_name=self._rulesets[index][0]
        )

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False