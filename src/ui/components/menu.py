import pygame
from typing import Callable, TYPE_CHECKING

from src.ui import UIElement
from src.ui.components import UILabel

if TYPE_CHECKING:
    from src.ui import ColorValue

class UIMenu(UIElement):
    """
    Representa un menú vertical de opciones.
    Maneja la navegación (arriba/abajo), la selección visual y la ejecución de callbacks.
    """
    def __init__(
            self, name: str, x: int, y: int,
            options: list[tuple[str, Callable[[], None]]],
            font: pygame.font.Font, *, spacing: int,
            marker_left: str = ">", marker_right: str = "<",
            marker_offset: int = 20, center_text: bool = False,
            normal_color: "ColorValue" = (255, 255, 255),
            selected_color: "ColorValue" = (255, 215, 0),
            visible: bool = True, alpha: int = 255
            ):
        """
        Args:
            options: Lista de tuplas (texto, callback).
            font: Fuente a utilizar para las opciones de texto.
            spacing: Espacio vertical en píxeles entre cada opción.
            marker_left: Símbolo indicador de selección (cursor) a la izquierda.
            marker_right: Símbolo indicador de selección (cursor) a la derecha.
            marker_offset: Espacio entre el texto de mayor longitud y el cursor.
            center_text: Opción de centrado de los textos.
            normal_color: Color del texto no seleccionado.
            selected_color: Color del texto seleccionado.
        """
        # Extrae los textos y callbacks
        option_texts = [option[0] for option in options]
        self._callbacks = [option[1] for option in options]

        # Inicializacion de los labels para cada opcion
        self._labels: list[UILabel] = []
        self._spacing = spacing
        self._marker_offset = marker_offset

        # Colores
        self._normal_color = normal_color
        self._selected_color = selected_color

        current_y = y
        for i, option_text in enumerate(option_texts):
            label = UILabel(f"{name}_option_{i}", x, current_y, option_text,
                            font, normal_color, center=center_text, alpha=alpha)
            current_y += label.rect.height + spacing
            self._labels.append(label)

        # Estado interno
        self._selected_index: int = 0
        self._option_count = len(options)

        # Estado del parpadeo (Retro Blink Effect)
        self._blink_timer: float = 0.0        # Temporizador (si es > 0, está parpadeando)
        self._blink_duration: float = 0.80    # Duración total
        self._blink_interval: float = 0.08    # Rapidez del titileo

        # Cursor de seleccion
        self._marker_left = UILabel(f"{name}_marker", 0, 0,
                               marker_left, font, selected_color, center=False, alpha=alpha)
        self._marker_right = UILabel(f"{name}_marker", 0, 0,
                               marker_right, font, selected_color, center=False, alpha=alpha)

        max_label_width = max(label.rect.width for label in self._labels) if self._labels else 0
        markers_space = self._marker_left.rect.width + self._marker_right.rect.width + (marker_offset * 2)
        width = markers_space + max_label_width
        height = len(options) * spacing

        super().__init__(name, x, y, width, height, visible=visible, alpha=alpha)

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
        self._selected_index = (self._selected_index - 1) % self._option_count
        self._update_selection()

    def move_down(self) -> None:
        """Mueve la selección hacia abajo."""
        self._selected_index = (self._selected_index + 1) % self._option_count
        self._update_selection()

    def execute_selected(self) -> None:
        """Inicia el efecto de parpadeo antes de ejecutar el callback."""
        if self._blink_timer > 0: return
        
        if self._callbacks[self._selected_index]:
            # Iniciar el estado de parpadeo en lugar de ejecutar inmediatamente
            self._blink_timer = self._blink_duration
    
    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        for label in self._labels:
            label.update(dt)

        self._marker_left.update(dt)
        self._marker_right.update(dt)

        # Lógica del parpadeo simplificada
        if self._blink_timer > 0:
            self._blink_timer -= dt
            if self._blink_timer <= 0: # Cuando el tiempo se acaba, ejecutamos la acción
                self._callbacks[self._selected_index]()

    def render(self, surface: pygame.Surface) -> None:
        """Renderiza todas las opciones y el cursor."""
        if not self.visible:
            return
        
        # Calcula si debe mostrar el texto basándose en el tiempo restante
        is_blinking = self._blink_timer > 0
        show_text = (int(self._blink_timer / self._blink_interval) % 2 != 0) if is_blinking else True
            
        for i, label in enumerate(self._labels):
            if is_blinking and i == self._selected_index and not show_text:
                continue # Salta el renderizado (lo oculta en este frame)
            label.render(surface)
            
        if not is_blinking or show_text:
            self._marker_left.render(surface)
            self._marker_right.render(surface)

    def _update_selection(self) -> None:
        """Actualiza colores y ajusta la posición de los cursores abrazando la opción actual."""
        for i, label in enumerate(self._labels):
            if i == self._selected_index:
                label.set_color(self._selected_color)
            else:
                label.set_color(self._normal_color)
                
        # Mover los cursores para que envuelvan a la opción seleccionada
        if self._labels:
            current_label = self._labels[self._selected_index]
            
            # Marcador Izquierdo
            self._marker_left.rect.right = current_label.rect.left - self._marker_offset
            self._marker_left.rect.centery = current_label.rect.centery
            
            # Marcador Derecho
            self._marker_right.rect.left = current_label.rect.right + self._marker_offset
            self._marker_right.rect.centery = current_label.rect.centery

    def fade_to_all(self, target: int, duration: float) -> None:
        """Aplica fade a todos los labels internos y los cursores."""
        for label in (*self._labels, self._marker_left, self._marker_right):
            label.fade_to(target, duration)