import pygame
from typing import TYPE_CHECKING

from src.states.game_state import GameState
from src.states.types import OverlayType

from src.config import KeybindEditor
from src.constants import SCREEN_SIZE
from src.util.conversors import pygame_key_to_str
from src.ui import UIManager, UILabel, UIButton

if TYPE_CHECKING:
    from ..core.game import Game

class KeybindEditorState(GameState):
    """Estado interactivo para reasignar los controles con scroll por páginas."""
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.w, self.h = SCREEN_SIZE

        self._editor = KeybindEditor(game.controls_config)
        self._max = game.controls_config.max_keys_for_action

        # --- Datos de las acciones ---
        self._contexts = self._editor.get_contexts()
        self._actions: list[tuple[str, str]] = [
            (ctx, act)
            for ctx in self._contexts
            for act in self._editor.get_actions(ctx)
        ]

        self._action_cursor = 0
        self._slot_cursor   = 0
        
        self._slot_buttons: dict[tuple[int, int], UIButton] = {}
        
        # Diccionario para agrupar elementos UI por "página" (contexto)
        self._page_elements: dict[str, list] = {ctx: [] for ctx in self._contexts}

        self._build_fonts()
        self._build_ui()
        self._build_static_surfaces()

        self._sync_ui_state()

    def _current(self) -> tuple[str, str, int]:
        ctx, act = self._actions[self._action_cursor]
        return ctx, act, self._slot_cursor

    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self._sync_ui_state()

        self.ui.update(dt)

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            # --- MODO CAPTURA ---
            if self._editor.is_capturing:
                if event.key == pygame.K_ESCAPE:
                    self.game.audio.play_sfx("Scroll")
                    self._editor.cancel_capture()
                else:
                    self.game.audio.play_sfx("Select")
                    self._editor.assign(event.key)
                return

            # --- MODO NAVEGACIÓN ---
            match event.key:
                case pygame.K_UP:
                    self.game.audio.play_sfx("Scroll")
                    self._action_cursor = (self._action_cursor - 1) % len(self._actions)

                case pygame.K_DOWN:
                    self.game.audio.play_sfx("Scroll")
                    self._action_cursor = (self._action_cursor + 1) % len(self._actions)

                case pygame.K_LEFT:
                    self.game.audio.play_sfx("Scroll")
                    self._slot_cursor = (self._slot_cursor - 1) % self._max

                case pygame.K_RIGHT:
                    self.game.audio.play_sfx("Scroll")
                    self._slot_cursor = (self._slot_cursor + 1) % self._max
                
                case pygame.K_RETURN:
                    self.game.audio.play_sfx("Select")
                    self._slot_buttons[(self._action_cursor, self._slot_cursor)].on_click()
                
                case pygame.K_DELETE:
                    self.game.audio.play_sfx("Scroll")
                    ctx, act, slot = self._current()
                    self._editor.clear_slot(ctx, act, slot)
                
                case pygame.K_s:
                    self.game.audio.play_sfx("Select")
                    self._editor.apply()
                    self.game.input.update_controls(self.game.controls_config.data)
                
                case pygame.K_ESCAPE:
                    self.game.audio.play_sfx("Select")
                    self._editor.discard()
                    self.game.state.exit_current()
                    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((23, 23, 23))
        surface.blit(self._arrows, (850, 270))

        self.ui.render(surface)

        # --- DIBUJAR INDICADORES DE SCROLL ---
        active_ctx = self._actions[self._action_cursor][0]
        ctx_index = self._contexts.index(active_ctx)

        self._draw_hint_bar(surface)

    def _build_fonts(self) -> None:
        self.fonts = {
            "title": self.game.resources.get_font("Estandar", 90),
            "ctx": self.game.resources.get_font("Estandar", 48),
            "act": self.game.resources.get_font("Estandar", 35),
            "small": self.game.resources.get_font("Estandar", 25),
            "hints": self.game.resources.get_font("Estandar", 25)
        }

    def _build_ui(self) -> None:
        self.ui = UIManager()

        self.title = UILabel("keybind_title", self.w // 2, 20, "Controles", self.fonts["title"], (130, 59, 188))
        self.status_label = UILabel("keybind_status", self.w // 2, 140, "", self.fonts["small"], (200, 200, 200))

        self.ui.add_element(self.title)
        self.ui.add_element(self.status_label)

        btn_base = self.game.resources.get_image("ControlsNormalBtn")
        btn_sel = self.game.resources.get_image("ControlsSelBtn")

        # --- Variables de Layout Centrado ---
        col_action_x = 160
        col_slots_x = [460, 665] 

        global_index = 0

        for ctx in self._contexts:
            y = 210 # Reiniciamos la Y para cada página/contexto
            
            # Etiqueta del título de la página
            ctx_label = UILabel(f"ctx_{ctx}", col_action_x - 30, y, f"--- {ctx.upper()} ---", self.fonts["ctx"], (130, 59, 188), center=False)
            self.ui.add_element(ctx_label)
            self._page_elements[ctx].append(ctx_label)
            y += 65

            actions = self._editor.get_actions(ctx)
            for act in actions:
                # Nombre de la acción
                act_label = UILabel(f"act_{act}_{global_index}", col_action_x, y + 5, act.capitalize(), self.fonts["act"], (255, 255, 255), center=False)
                self.ui.add_element(act_label)
                self._page_elements[ctx].append(act_label)

                # Botones de la acción
                for s in range(self._max):
                    btn_lbl = UILabel(f"lbl_{global_index}_{s}", 0, 0, "---", self.fonts["small"], center=True)
                    
                    def start_capture_callback(c=ctx, a=act, slot_idx=s):
                        self._editor.start_capture(c, a, slot_idx)

                    btn = UIButton(
                        f"btn_{global_index}_{s}", col_slots_x[s], y, 
                        start_capture_callback, btn_base.copy(), btn_sel.copy(),
                        text=btn_lbl, text_y=3
                    )
                    
                    self._slot_buttons[(global_index, s)] = btn
                    self.ui.add_element(btn)
                    self._page_elements[ctx].append(btn)

                y += 60
                global_index += 1

    def _build_static_surfaces(self) -> None:
        self._arrows = self.game.resources.get_image("MenuArrows")

        hints = [
            ("Flechas", "Navegar"), ("Enter", "Asignar"), 
            ("Supr", "Borrar"), ("S", "Guardar"), ("Esc", "Salir")
        ]

        self._hint_renders = []
        for k_str, a_str in hints:
            k = self.fonts["hints"].render(f"[{k_str}]", True, (190, 190, 190))
            a = self.fonts["hints"].render(f" {a_str}", True, (150, 150, 150))
            self._hint_renders.append((k, a))

    def _draw_hint_bar(self, surface: pygame.Surface) -> None:
        bar_y = self.h - 50

        gap = 30
        total_w = sum(k.get_width() + a.get_width() for k, a in self._hint_renders) + gap * (len(self._hint_renders) - 1)
        cur_x = (self.w - total_w) // 2
        text_y = bar_y + 11

        for k_surf, a_surf in self._hint_renders:
            surface.blit(k_surf, (cur_x, text_y))
            cur_x += k_surf.get_width()
            surface.blit(a_surf, (cur_x, text_y))
            cur_x += a_surf.get_width() + gap

    def _sync_ui_state(self) -> None:
        # Actualizar textos de estado
        if self._editor.is_capturing:
            self.status_label.set_text("Presiona una tecla...")
            self.status_label.set_color((255, 100, 100))
        elif self._editor.has_changes():
            self.status_label.set_text("Tienes cambios sin guardar. Presiona 'S' para aplicar.")
            self.status_label.set_color((100, 255, 100))
        else:
            self.status_label.set_text("Selecciona una acción para reasignar.")
            self.status_label.set_color((200, 200, 200))

        # Controlar visibilidad de las páginas (Paginación)
        active_ctx = self._actions[self._action_cursor][0]
        
        for ctx, elements in self._page_elements.items():
            is_active_page = (ctx == active_ctx)
            for el in elements:
                el.visible = is_active_page

        # Sincronizar el estado de todos los botones
        for i, (ctx, act) in enumerate(self._actions):
            slots = self._editor.get_slots(ctx, act)
            
            for s in range(self._max):
                btn = self._slot_buttons[(i, s)]
                is_active = (i == self._action_cursor and s == self._slot_cursor)
                
                btn.is_selected = is_active

                try:
                    key_code = slots[s] if s < len(slots) else None
                    label_str = pygame_key_to_str(key_code) if key_code is not None else "---"
                except ValueError:
                    label_str = "???"

                if is_active and self._editor.is_capturing and btn._text:
                    btn.set_text("...")
                    btn._text.set_color((255, 100, 100))
                elif btn._text:
                    btn.set_text(label_str)
                    btn._text.set_color((255, 255, 255) if is_active else (200, 200, 200))



    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.FULLSCREEN

    @property
    def is_transient(self) -> bool:
        return False