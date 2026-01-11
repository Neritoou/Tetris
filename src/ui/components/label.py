import pygame
from typing import Tuple, Union
from ...ui import UIElement

ColorValue = Union[pygame.Color, Tuple[int, int, int], str]

class UILabel(UIElement):
    """Representa una etiquetaa de texto en la interzas de usuario."""
    def __init__(self, name: str, x: int, y: int,
                 text: str, font: pygame.font.Font,
                 color: ColorValue = (255, 255, 255), *,
                 visible: bool = True, alpha: int = 255, scale: float = 1.0,
                 angle: int = 0):
        """
        Inicializa las propiedades de las etiquetas.
        
        Args:
            text: Texto de la etiqueta.
            font: Fuente del texto.
            color: Color del texto.
        """
        # Datos del texto
        self.font = font
        self.text = text
        self.color = pygame.Color(color)

        # Superficie inicial
        self.text_surface = font.render(self.text, True, self.color)
        width, height = self.text_surface.get_size()

        super().__init__(name, x, y, width, height, visible=visible,
                         enabled=False, alpha=alpha, scale=scale, angle=angle)

    def set_text(self, new_text: str) -> None:
        """Actualiza el contenido del texto y ajusta el área de colisión."""
        if self.text != new_text:
            self.text = new_text
            self.text_surface = self.font.render(self.text, True, self.color)

            pos = self.rect.topleft
            self.rect = self.text_surface.get_rect(topleft=pos)

    def set_color(self, new_color: ColorValue) -> None:
        """Cambia el color del texto y regenera la superficie."""
        temp_color = pygame.Color(new_color)

        if self.color != temp_color:
            self.color = temp_color
            self.text_surface = self.font.render(self.text, True, self.color)

    def set_font(self, new_font: pygame.font.Font) -> None:
        """Cambia la fuente del texto y recalcula el tamaño del Rect."""
        self.font = new_font
        self.text_surface = self.font.render(self.text, True, self.color)

        pos = self.rect.topleft
        self.rect = self.text_surface.get_rect(topleft=pos)

    def center_at(self, x: int, y: int) -> None:
        """Posiciona el texto centrándolo en las coordenadas dadas."""
        self.rect.center = (x, y)



    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def render(self, surface: pygame.Surface) -> None:
        self.text_surface.set_alpha(int(self.alpha))
        
        # Se dibuja el elemento estático sobre la superficie de la pantalla
        surface.blit(self.text_surface, self.rect)

    def update(self, dt: float) -> None:
        super().update(dt)