import pygame
from typing import Optional

from src.ui import UIElement, ColorValue
from src.ui.components.label import UILabel

class UISlideButton(UIElement):
    """Botón que se desliza horizontalmente según su estado de selección."""
    def __init__(
        self, name: str, anchor_x: int, y: int, btn_surface: pygame.Surface,
        selected_surface: pygame.Surface | None = None, text: str = "",
        font: Optional[pygame.font.Font] = None,
        text_color: ColorValue = (0, 0, 0), hidden_offset: int = 150,
        lerp_speed: float = 10.0, anchor_left: bool = False,
        icon: Optional[pygame.Surface] = None, show_selected_icon: bool = False,
        content_padding: int = 12
    ):
        """
        Args:
            anchor_x: Posición horizontal fija (ancla) de todos los botones.
            y: Posición vertical del primer botón.
            surface: Surface del botón.
            text: Texto que va dentro del botón.
            font: Fuente utilizada para renderizar el texto.
            text_color: Color del texto de los labels.
            hidden_offset: Píxeles ocultos cuando no está seleccionado.
            lerp_speed: Velocidad de interpolación.
            anchor_left: Si es True, los botones se ancla al borde izquierdo y se
                        desliza hacia la derecha.
            icon: Surface de un ícono opcional para el botón.
            show_selected_icon: Cuando es True muestra el icono solo del boton
                        seleccionado.
            content_padding: Distancia desde el borde interior del botón al
                        contenido (ícono/texto).
        
        """
        w, h = btn_surface.get_size()
        
        # Lógica de posiciones según el borde de anclaje
        if anchor_left:
            # El botón se pega al borde izquierdo y se oculta hacia la derecha
            self._selected_x = float(anchor_x)
            self._rest_x = float(anchor_x + hidden_offset)
        else:
            # El botón se pega al borde derecho y se oculta hacia la izquierda
            self._selected_x = float(anchor_x - w)
            self._rest_x = (anchor_x - w - hidden_offset)
        
        super().__init__(name, int(self._rest_x), y, w, h, visible=True)

        self.btn_surface = btn_surface
        self.selected_surface = selected_surface
        self._lerp_speed = lerp_speed
        self._anchor_left = anchor_left
        self._show_selected_icon = show_selected_icon

        self._current_x: float = self._rest_x
        self._is_selected: bool = False

        self._icon = pygame.transform.smoothscale(icon, (h-20, h-20)) if icon else None
        self._icon_offset_x = 0
        self._icon_offset_y = 0
        
        self._label = UILabel(
            f"{name}_label", 0, 0, text, font, text_color, 
            center=False, visible=True
        ) if font and text else None

        self._label_offset_x = 0
        self._label_offset_y = 0

        # Determinamos dónde va el contenido basándonos en el anclaje direccional
        if self._anchor_left:
            # Contenido pegado a la izquierda (para que no se oculte al salir a la derecha)
            current_x_offset = content_padding
            
            if self._icon:
                self._icon_offset_x = current_x_offset
                self._icon_offset_y = (h - self._icon.get_height()) // 2
                current_x_offset += self._icon.get_width() + content_padding
                
            if self._label:
                self._label_offset_x = current_x_offset
                self._label_offset_y = (h - self._label.rect.height) // 2

        else:
            # Contenido pegado a la derecha (para que no se oculte al salir a la izquierda)
            current_x_offset = w - content_padding
            
            if self._icon:
                current_x_offset -= self._icon.get_width()
                self._icon_offset_x = current_x_offset
                self._icon_offset_y = (h - self._icon.get_height()) // 2

            if self._label:
                current_x_offset -= self._label.rect.width + content_padding // 2 if self._icon else self._label.rect.width
                self._label_offset_x = current_x_offset
                self._label_offset_y = (h - self._label.rect.height) // 2
                current_x_offset -= content_padding

        self._sync_positions()

    def set_selected(self, selected: bool) -> None:
        self._is_selected = selected

    def snap(self) -> None:
        """Coloca el botón instantáneamente en su posición objetivo."""
        self._current_x = self._selected_x if self._is_selected else self._rest_x
        self._sync_positions()

    def _sync_positions(self) -> None:
        """Aplica la posición principal y los offsets pre-calculados a los hijos."""
        self.rect.x = int(self._current_x)
        
        if self._label:
            self._label.rect.x = self.rect.x + self._label_offset_x
            self._label.rect.y = self.rect.y + self._label_offset_y
            # Sincronizamos el alpha con el UILabel si hay fading
            self._label.alpha = self.alpha



    # --- Métodos Abstractos de UIElement ---
    def update(self, dt: float) -> None:  
        super().update(dt)

        target = self._selected_x if self._is_selected else self._rest_x
        
        if abs(target - self._current_x) > 0.1:
            diff = target - self._current_x
            self._current_x += diff * self._lerp_speed * dt
            self._sync_positions()
        elif self._current_x != target:
            self._current_x = target
            self._sync_positions()

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        
        if self._is_selected and self.selected_surface:
            current_btn_surface = self.selected_surface
        else:
            current_btn_surface = self.btn_surface

        surface.blit(current_btn_surface, self.rect)

        if self._icon and (not self._show_selected_icon or self._is_selected):
            surface.blit(self._icon, (self.rect.x + self._icon_offset_x, self.rect.y + self._icon_offset_y))

        if self._label:
            self._label.render(surface)
        