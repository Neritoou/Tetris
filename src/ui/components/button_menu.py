import pygame
from typing import Callable, TYPE_CHECKING

from src.ui import UIElement
from src.ui.components.button import UIButton
from src.ui.components.label import UILabel

if TYPE_CHECKING:
    from src.ui import ColorValue

class UIButtonMenu(UIElement):
    """
    Menú vertical compuesto por botones (UIButton) controlable por teclado.
    Reutiliza la lógica del botón: el estado 'seleccionado' del teclado se
    mapea al estado 'hover' visual del botón.
    """
    def __init__(
            self, name: str, x: int, y: int,
            options: list[tuple[str, Callable[[], None]]],
            base_surface: pygame.Surface, selected_surface: pygame.Surface,
            font: pygame.font.Font, text_color: "ColorValue" = (255, 255, 255),
            spacing: int = 20, center_x: bool = False, horizontal: bool = False,
            visible: bool = True, alpha: int = 255
    ):
        """
        Args:
            options: Lista de tuplas (texto, callback).
            base_button: Imagen del botón en estado normal.
            selected_button: Imagen del botón seleccionado.
            font: Fuente a utilizar para las opciones de texto.
            text_color: Color del texto
            spacing: Espacio vertical en píxeles entre cada opción.
            center_x: Centrado horizontal del botón.
            horizontal: Si se desea hacer el menu horizontal
        """
        # Calcular dimensiones
        btn_w, btn_h = base_surface.get_size()
        self._options_count = len(options)

        if horizontal:
            total_width = (btn_w  + spacing) * self._options_count - spacing
            total_height = btn_h

            start_x = (x - total_width // 2) if center_x else x
        else:
            total_width = btn_w
            total_height = (btn_h + spacing) * self._options_count - spacing

            start_x = (x - btn_w // 2) if center_x else x

        self._buttons: list[UIButton] = []
        self._selected_index: int = 0
        self._horizontal = horizontal

        # Crear cada botón
        for i, (text, callback) in enumerate(options):
            if self._horizontal:
                btn_x = start_x + i * (btn_w + spacing)
                btn_y = y
            else:
                btn_x = start_x
                btn_y = y + i * (btn_h + spacing)
            
            # Label centrado para el botón
            btn_label = UILabel(f"{name}_lbl_{i}", 0, 0, text, font, text_color, center=True, alpha=alpha)
            
            btn = UIButton(
                f"{name}_btn_{i}", int(btn_x), int(btn_y), callback,
                base_surface.copy(), selected_surface.copy(),
                text=btn_label, visible=visible, alpha=alpha
            )
            self._buttons.append(btn)
        
        super().__init__(name, int(start_x), y, btn_w, total_height, visible=visible, alpha=alpha)

        self._update_selection()

    @property
    def selected_index(self) -> int:
        """Índice actual de la opción seleccionada."""
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, value: int) -> None:
        """Permite establecer la selección directamente."""
        if self._options_count > value and value >= 0:
            self._selected_index = value
            self._update_selection()

    def move_up(self) -> None:
        """Mueve la selección hacia arriba."""
        self._selected_index = (self._selected_index - 1) % len(self._buttons)
        self._update_selection()

    def move_down(self) -> None:
        """Mueve la selección hacia abajo."""
        self._selected_index = (self._selected_index + 1) % len(self._buttons)
        self._update_selection()

    def execute_selected(self) -> None:
        """Ejecuta el callback del botón actualmente seleccionado."""
        if self._buttons:
            self._buttons[self._selected_index].on_click()

    def _update_selection(self) -> None:
        """Actualiza el estado de los botones (simula el hover en el seleccionado)."""
        for i, btn in enumerate(self._buttons):
            btn.is_selected = (i == self._selected_index)
            
    # --- Métodos Abstractos de UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        for btn in self._buttons:
            btn.visible = self.visible
            btn.alpha = self.alpha
            btn.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        
        for btn in self._buttons:
            btn.render(surface)