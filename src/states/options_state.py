import pygame
from typing import TYPE_CHECKING

from src.states.types import StateID, OverlayType
from src.states.game_state import GameState

from src.constants import SCREEN_CENTER_W, SCREEN_CENTER_H, SCREEN_SIZE
from src.util.conversors import get_hint_key
from src.ui import UIManager, UIMenu, UILabel, UIButtonMenu

if TYPE_CHECKING:
    from src.core.game import Game

class OptionsState(GameState):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        self.font_title = self.game.resources.get_font("Estandar", 100)
        self.font_menu = self.game.resources.get_font("Estandar", 48)
        self.font_small = self.game.resources.get_font("Estandar", 30)

        self._dark_overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self._dark_overlay.fill((0, 0, 0, 200))

        self._panel_rect = pygame.Rect(0, 0, 750, 310)
        self._panel_rect.center = (SCREEN_CENTER_W, SCREEN_CENTER_H)

        self._build_ui()
        self._build_confirm_panel()
        self._build_volume_panel()
        
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self.ui.update(dt)
        self.confirm_ui.update(dt)
        self.volume_ui.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.game.background, (0, 0))

        self.ui.render(surface)

        if self.is_confirming:
            # Oscurecer aún más el fondo
            surface.blit(self._dark_overlay, (0, 0))

            # Dibujar el panel de la ventana flotante
            pygame.draw.rect(surface, (33, 31, 31), self._panel_rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), self._panel_rect, width=5, border_radius=8)

            # Renderizar los textos y botones de confirmación
            self.confirm_ui.render(surface)

        if self.is_volume:
            surface.blit(self._dark_overlay, (0, 0))
            pygame.draw.rect(surface, (213, 176, 191), self._panel_rect, border_radius=25)
            pygame.draw.rect(surface, (255, 255, 255), self._panel_rect, width=5, border_radius=25)
            self.volume_value.set_text(self._volume_text())
            self.volume_ui.render(surface)


    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if self.is_volume:
            if self.game.input.is_action_pressed("ui", "left"):
                #self.game.audio.play_sfx("scroll")
                self._change_volume(-0.1)
            elif self.game.input.is_action_pressed("ui","right"):
                #self.game.audio.play_sfx("scroll")
                self._change_volume(0.1)
            elif self.game.input.is_action_pressed("ui", "pause"):
                #self.game.audio.play_sfx("select")
                self.is_volume = False
        elif self.is_confirming:
            if self.game.input.is_action_pressed("ui", "left"):
                #self.game.audio.play_sfx("scroll")
                self.confirm_menu.move_up()
            elif self.game.input.is_action_pressed("ui", "right"):
                #self.game.audio.play_sfx("scroll")
                self.confirm_menu.move_down()
            elif self.game.input.is_action_pressed("ui", "select"):
                #self.game.audio.play_sfx("select")
                self.confirm_menu.execute_selected()
            elif self.game.input.is_action_pressed("ui", "pause"):
                self._on_confirm_no()
        else:
            if self.game.input.is_action_pressed("ui", "up"):
                #self.game.audio.play_sfx("scroll")
                self.menu.move_up()
            elif self.game.input.is_action_pressed("ui", "down"):
                #self.game.audio.play_sfx("scroll")
                self.menu.move_down()
            elif self.game.input.is_action_pressed("ui", "select"):
                #self.game.audio.play_sfx("select")
                self.menu.execute_selected()
            elif self.game.input.is_action_pressed("ui", "pause"): # ESC para volver
                #self.game.audio.play_sfx("select")
                self._on_back()

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.FULLSCREEN

    @property
    def is_transient(self) -> bool:
        return False
    
    def _build_ui(self) -> None:
        options_list = [
            ("VOLUMEN", self._on_volume),
            ("CONTROLES", self._on_controls),
            ("BORRAR DATOS", self._show_confirmation),
            ("VOLVER", self._on_back)
        ]

        # Título del menú de opciones
        self.title = UILabel("options_title", SCREEN_CENTER_W, 150, 
                             "Opciones", self.font_title, (130, 59, 188))

        self.menu = UIMenu(
            "options_menu", SCREEN_CENTER_W, 330, options_list, self.font_menu,
           spacing=20, center_text=True
        )
        
        self.ui: UIManager = UIManager()
        self.ui.add_element(self.title)
        self.ui.add_element(self.menu)

    def _build_confirm_panel(self) -> None:
        self.is_confirming = False
        
        self.confirm_label = UILabel(
            "confirm_label", SCREEN_CENTER_W, 280, "¿Borrar TODOS los records?",
            self.font_menu, (204, 35, 35)
            )
        self.confirm_sub = UILabel(
            "confirm_sub", SCREEN_CENTER_W, 340, "Esta acción no se puede deshacer.",
            self.font_small, (130, 130, 130)
            )

        confirm_options = [
            ("NO, CANCELAR", self._on_confirm_no),
            ("SÍ, BORRAR TODO", self._on_confirm_yes)
        ]

        c_btn_surf = pygame.Surface((270, 60), pygame.SRCALPHA)
        pygame.draw.rect(c_btn_surf, (41, 38, 38, 230), c_btn_surf.get_rect(), border_radius=8)

        c_sel_surf = pygame.Surface((270, 60), pygame.SRCALPHA)
        pygame.draw.rect(c_sel_surf, (200, 50, 50, 255), c_sel_surf.get_rect(), border_radius=8)
        pygame.draw.rect(c_sel_surf, (255, 255, 255), c_sel_surf.get_rect(), width=5, border_radius=8)

        self.confirm_menu = UIButtonMenu(
            "confirm_menu", SCREEN_CENTER_W, 430,
            confirm_options, c_btn_surf, c_sel_surf, self.font_small, 
            center_x=True, horizontal=True, spacing=20
        )

        self.confirm_ui = UIManager()
        self.confirm_ui.add_element(self.confirm_label)
        self.confirm_ui.add_element(self.confirm_sub)
        self.confirm_ui.add_element(self.confirm_menu)

    def _build_volume_panel(self) -> None:
        self.is_volume = False
        cx = SCREEN_CENTER_W

        self.volume_title = UILabel(
            "volume_title", cx, 260, "Volumen",
            self.font_menu, (60, 40, 40)
        )
        self.volume_value = UILabel(
            "volume_value", cx, 330, self._volume_text(),
            self.font_menu, (60, 40, 40)
        )

        left = get_hint_key(self.game.controls_config,"left")
        right = get_hint_key(self.game.controls_config,"right")
        esc = get_hint_key(self.game.controls_config,"pause")
        self.volume_hint = UILabel(
            "volume_hint", cx, 430, f"[{left}] / [{right}] para ajustar     |     [{esc}] para volver",
            self.font_small, (0, 0, 0)
        )

        self.volume_ui = UIManager()
        self.volume_ui.add_element(self.volume_title)
        self.volume_ui.add_element(self.volume_value)
        self.volume_ui.add_element(self.volume_hint)

    def _volume_text(self) -> str:
        vol = round(self.game.audio.get_master_volume() * 10)
        return f"{vol} / 10"

    def _change_volume(self, delta: float) -> None:
        current = self.game.audio.get_master_volume()
        self.game.audio.set_master_volume(max(0.0, min(1.0, current + delta)))



    # --- Callbacks ---
    def _on_controls(self):
        self.game.state.change(StateID.KEYBIND_EDITOR)

    def _show_confirmation(self):
        self.is_confirming = True
    
    def _on_back(self):
        self.game.state.exit_current()

    def _on_volume(self):

        self.is_volume = True

    def _on_confirm_yes(self):
        self.game.database.reset_all_records()
        self.is_confirming = False

    def _on_confirm_no(self):
        self.is_confirming = False