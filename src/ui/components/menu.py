import pygame
from typing import Tuple, List, Callable, TYPE_CHECKING
from ...ui import UIElement


from ..components import UILabel

class UIMenu(UIElement):
    """
    Representa un menú vertical de opciones.
    Maneja la navegación (arriba/abajo), la selección visual y la ejecución de callbacks.
    """
    def __init__(self, name: str, x: int, y: int,
                 options: List[Tuple[str, Callable[[], None]]],
                 font: pygame.font.Font, *,
                 spacing: int, marker: str = ">", marker_offset: int = 50,
                 center_text: bool = False,
                 normal_color: Tuple[int, int, int] = (255, 255, 255),
                 selected_color: Tuple[int, int, int] = (255, 215, 0),
                 visible: bool = True, enabled: bool = True):
        """
        Args:
            options: Lista de tuplas (texto, callback).
            font: Fuente a utilizar para las opciones de texto.
            spacing: Espacio vertical en píxeles entre cada opción.
            marker: Símbolo indicador de selección (cursor).
            marker_offset: Espacio entre el texto de mayor longitud y el cursor.
            center_text: Opción de centrado de los textos.
            normal_color: Color del texto no seleccionado.
            selected_color: Color del texto seleccionado.
        """
        # Extrae los textos y callbacks
        option_texts = [option[0] for option in options]
        self._callbacks = [option[1] for option in options]

        # Inicializacion de los labels para cada opcion
        self._labels: List[UILabel] = []
        self._spacing = spacing

        # Colores
        self._normal_color = normal_color
        self._selected_color = selected_color

        for i, option_text in enumerate(option_texts):
            label = UILabel(f"{name}_option_{i}", x, (y + i * spacing),
                            option_text, font, normal_color, visible=visible)
            self._labels.append(label)

        # Cursor de seleccion
        self._marker = UILabel(f"{name}_marker", x - marker_offset, y,
                               marker, font, selected_color, visible=visible)

        # Estado interno
        self._selected_index: int = 0
        self._option_count = len(options)

        # Calcula las dimensiones
        max_label_width = max(label.rect.width for label in self._labels)
        marker_space = self._marker.rect.width + 20

        width = marker_space + max_label_width
        height = len(options) * spacing

        # Centrado horizontal de los textos
        if center_text:
            for i, label in enumerate(self._labels):
                label.center_at(x)

            self._marker.center_at(x - max_label_width + marker_offset)

        super().__init__(name, x, y, width, height, visible=visible, enabled=enabled)

        self._update_selection()

    @property
    def selected_index(self) -> int:
        """Índice actual de la opción seleccionada."""
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, value: int) -> None:
        """Permite establecer la selección directamente."""
        if self._option_count > value and value >= 0:
            self._selected_index = value
            self._update_selection()
    
    def move_up(self) -> None:
        """Mueve la selección hacia arriba."""
        if not self.enabled:
            return
        self._selected_index = (self._selected_index - 1) % self._option_count
        self._update_selection()

    def move_down(self) -> None:
        """Mueve la selección hacia abajo."""
        if not self.enabled:
            return
        self._selected_index = (self._selected_index + 1) % self._option_count
        self._update_selection()

    def execute_selected(self) -> None:
        """Ejecuta el callback de la opción seleccionada."""
        if self.enabled and self._callbacks[self._selected_index]:
            self._callbacks[self._selected_index]()
    
    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        for label in self._labels:
            label.visible = self.visible
            label.alpha = self.alpha
            label.update(dt)

        self._marker.visible = self.visible
        self._marker.alpha = self.alpha
        self._marker.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """Renderiza todas las opciones y el cursor."""
        if not self.visible:
            return
        
        for label in self._labels:
            label.render(surface)
        
        self._marker.render(surface)

    def _update_selection(self) -> None:
        """Actualiza colores y posición del cursor según la selección."""
        for i, label in enumerate(self._labels):
            if i == self._selected_index:
                label.set_color(self._selected_color)
            else:
                label.set_color(self._normal_color)
        
        # Mover cursor a la opción seleccionada
        self._marker.rect.y = self._labels[self._selected_index].rect.y
