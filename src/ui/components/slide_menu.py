import pygame
from typing import Callable, TYPE_CHECKING

from src.ui import UIElement
from src.ui.components.slide_button import UISlideButton

if TYPE_CHECKING:
    from src.ui import ColorValue

class UISlideMenu(UIElement):
    """
    Menú vertical de botones deslizantes.
    Cada botón tiene un UILabel centrado encima.
    """

    def __init__(
        self, name: str, anchor_x: int, y: int,
        options: list[tuple[str, Callable[[], None]]],
        button_surface: pygame.Surface, font: pygame.font.Font,
        text_color: "ColorValue" = (0, 0, 0), *,
        selected_surface: pygame.Surface | None = None,
        content_padding: int = 20, spacing: int = 20, hidden_offset: int = 150,
        lerp_speed: float = 10.0, anchor_left: bool = False,
        icons: list[pygame.Surface] | None = None,
        show_selected_icon: bool = False
    ):
        """
        Args:
            anchor_x: Posición horizontal fija (ancla) de todos los botones.
            y: Posición vertical del primer botón.
            options: Lista de (texto, función_callback).
            button_surface: Surface compartida para todos los botones.
            font: Fuente utilizada para renderizar el texto.
            text_color: Color del texto.
            content_padding: Distancia desde el borde interior del botón al
                        contenido (ícono/texto).
            spacing: Espacio vertical entre botones.
            hidden_offset: Píxeles ocultos cuando no está seleccionado.
            lerp_speed: Velocidad de interpolación (movimiento).
            anchor_left: Si es True, los botones se ancla al borde izquierdo y se
                        desliza hacia la derecha.
            icons: Lista opcional de surfaces para los íconos (None = sin ícono).
            show_selected_icon: Cuando es True muestra el icono solo del boton
                        seleccionado.        
        """
        bw, bh = button_surface.get_size()
        total_height = (bh + spacing) * len(options)

        menu_x = float(anchor_x) if anchor_left else float(anchor_x - bw)

        super().__init__(name, int(menu_x), y, bw, total_height, visible=True)

        self._callbacks: list[Callable[[], None]] = [opt[1] for opt in options]
        self._selected_index: int = 0

        self._buttons: list[UISlideButton] = []

        for i, (text, _) in enumerate(options):
            btn_y = y + i * (bh + spacing)
            icon = icons[i] if icons and i < len(icons) else None

            # Copia la surface para que cada botón tenga la suya
            btn_surface = button_surface.copy()
            sel_surface = selected_surface.copy() if selected_surface else None

            btn = UISlideButton(
                f"{name}_btn_{i}", anchor_x, btn_y, btn_surface, sel_surface,
                text, font, text_color, hidden_offset, lerp_speed, anchor_left,
                icon, show_selected_icon, content_padding
            )
            self._buttons.append(btn)

        if self._buttons:
            self._buttons[0].set_selected(True)
            self._buttons[0].snap()

    

    # --- NAVEGACIÓN Y CONTROL ---
    def move_up(self) -> None:
        self._buttons[self._selected_index].set_selected(False)
        self._selected_index = (self._selected_index - 1) % len(self._buttons)
        self._buttons[self._selected_index].set_selected(True)

    def move_down(self) -> None:
        self._buttons[self._selected_index].set_selected(False)
        self._selected_index = (self._selected_index + 1) % len(self._buttons)
        self._buttons[self._selected_index].set_selected(True)

    def execute_selected(self) -> None:
        if self._callbacks:
            self._callbacks[self._selected_index]()



    # --- Métodos Abstractos de UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        for btn in self._buttons:
            btn.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return

        for btn in self._buttons:
            btn.render(surface)