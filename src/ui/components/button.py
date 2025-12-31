    import pygame
    from ..ui_element import UIElement
    from typing import Tuple, Optional


    class UIButton(UIElement):
        """
        Un botón interactivo que responde al hover y al click.
        """

        def __init__(
            self,
            name: str,
            surface: pygame.Surface,
            hover_surface: Optional[pygame.Surface],
            position: Tuple[int, int],
            func: Optional[callable] = None,
            scale: float = 1.0,
            visible: bool = True,
            enabled: bool = True,
        ):
            super().__init__(
                name=name,
                surface=surface,
                position=position,
                copy_surface=True,  # Asegura que cada botón tenga su propia copia de la superficie
                scale=scale,
                visible=visible,
                enabled=enabled,
            )

            self._hover_surface = hover_surface
            self._func = func

            # Estados internos
            self._is_hover: bool = False
            self._is_pressed: bool = False

            # Creamos el mask a partir de la superficie original (con transparencia)
            self._mask = pygame.mask.from_surface(self._surface)

        # --- PROPIEDADES PARA ACTUALIZAR ESTADO DESDE EXTERNO ---
        @property
        def is_hover(self) -> bool:
            return self._is_hover

        @is_hover.setter
        def is_hover(self, value: bool):
            self._is_hover = value

        @property
        def is_pressed(self) -> bool:
            return self._is_pressed

        @is_pressed.setter
        def is_pressed(self, value: bool):
            self._is_pressed = value

        # --- MÉTODOS ABSTRACTOS DE UIElement ---
        def update(self, dt: float) -> None:
            """
            Actualiza la superficie mostrada según el estado hover.
            No maneja input directamente.
            """
            if self._hover_surface is None:
                return
            if self._is_hover:
                self._surface = self._hover_surface
            else:
                self._surface = self._base_surface

        # --- MÉTODO PRIVADO ---
        def _on_click(self) -> None:
            """Ejecuta la función callback cuando el botón es presionado."""
            if self._func:
                self._func()

        # --- NUEVO MÉTODO PARA VERIFICAR COLISIÓN CON EL MOUSE ---
        def check_collision(self, mouse_pos: Tuple[int, int]) -> bool:
            """
            Verifica si el mouse está sobre el área no transparente de la imagen.
            
            Args:
                mouse_pos (Tuple[int, int]): La posición actual del mouse.
            
            Returns:
                bool: True si el mouse está sobre una zona no transparente del botón.
            """
            # Calcula la diferencia entre el rect del botón y la posición del mouse
            offset = (mouse_pos[0] - self._rect.x, mouse_pos[1] - self._rect.y)
            
            # Verifica si la posición del mouse está dentro del área no transparente usando el mask
            if self._mask.overlap_area(offset):
                return True
            return False
