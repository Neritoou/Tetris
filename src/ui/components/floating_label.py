import pygame
from src.ui.components.label import UILabel
from src.ui.ui_element import ColorValue

class UIFloatingLabel(UILabel):
    """
    Etiqueta flotante animada de uso general.
    
    Al activarse, flota hacia arriba mientras hace fade out.
    """
    def __init__(
            self, name: str, x: int, y: int,
            font: pygame.font.Font, *,
            float_speed: float = 45.0,
            fade_duration: float = 0.5,
            spawn_offset: float = 10.0
    ):
        """
        Args:
            float_speed: Píxeles por segundo que sube el texto.
            fade_duration: Duración en segundos del fade out.
            spawn_offset: Desplazamiento vertical inicial al aparecer (hacia abajo).
        """
        super().__init__(name, x, y, "", font, (255, 255, 255),
                         center=True, visible=False, alpha=0)
        
        self.base_y = y
        self._exact_y = float(y)
        self.float_speed = float_speed
        self.fade_duration = fade_duration
        self.spawn_offset = spawn_offset

    def show(self, text: str, color: ColorValue = (255, 255, 255)) -> None:
        """
        Muestra el label con el texto y color indicados, reiniciando la animación.

        Args:
            text: Texto a mostrar.
            color: Color del texto en formato RGB.
        """
        self.set_text(text)
        self.set_color(color)

        self.visible = True
        self.alpha = 255

        self._exact_y = self.base_y + self.spawn_offset
        self.rect.y = int(self._exact_y)

        self.fade_to(0, self.fade_duration)

    def update(self, dt: float) -> None:
        super().update(dt)

        if self.visible and self.alpha > 0:
            self._exact_y -= self.float_speed * dt
            self.rect.y = int(self._exact_y)
        elif self.alpha <= 0:
            self.visible = False

    def set_position(self, x: int, y: int) -> None:
        """Actualiza la posición base del label, respetando el centrado horizontal."""
        self.base_y = y
        self._exact_y = float(y)
        self.rect.y = y
        self.center_at(x)