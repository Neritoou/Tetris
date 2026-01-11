from abc import ABC, abstractmethod
from typing import Tuple, Union
import pygame

class UIElement(ABC):
    """Clase base abstracta para todos los elementos de la interfaz de usuario."""
    def __init__(
            self, name: str, x: int, y: int, width: int, height: int, *,
            visible: bool, enabled: bool, alpha: int = 255, scale: float = 1.0,
            angle: int = 0):
        """
        Inicializa las propiedades comunes de los elementos UI.
        
        Args:
            name: Nombre del elemento UI.
            x: Posición horizontal inicial.
            y: Posición vertical inical.
            width: Ancho en píxeles.
            height: Alto en píxeles.
            visible: Si el elemento es visible en pantalla.
            enabled: Si el elemento está habilitado para interacción.
            alpha: Transparencia de la imagen.
            scale: Escala (tamaño) de la imagen.
            angle: Ángulo de la imagen.
        """
        self.name = name

        # Posición y dimensiones
        self.rect = pygame.Rect(x, y, width, height)

        # Estados de visibilidad y accesibilidad
        self.visible = visible
        self.enabled = enabled

        # Transformaciones
        self.alpha: float = float(alpha)
        self.scale = scale
        self.angle = angle

        self.target_alpha: float = self.alpha
        self.fade_speed: float = 0.0

        # Atributos privados
        self._is_fading: bool = False

    @property
    def position(self) -> Tuple[int, int]:
        """Obtiene la posición del elemento UI (esquina superior izquierda)."""
        return self.rect.topleft

    @position.setter
    def position(self, pos: Tuple[int, int]) -> None:
        self.rect.topleft = pos

    @property
    def is_fading(self) -> bool:
        """Devuelve True si el elemento está actualmente en una transición de alpha."""
        return self._is_fading

    def center_on_screen(self, screen_width: int, screen_height: int) -> None:
        """Centra el elemento en las dimensiones de pantalla proporcionadas."""
        self.rect.center = (screen_width // 2, screen_height // 2)

    def fade_to(self, target: int, duration: float) -> None:
        """
        Cambia la transparencia de la imagen, calculando el tiempo en que se
        debe aplicar el cambio.

        Args:
            target_alpha: Transparencia objetivo.
            duration: Duración en la que se desea aplicar la transparencia.
        
        Raises:
            ValueError: Si el valor de target_alpha no entra en el rango 0-255.
        """
        # Verifica que el valor del target_alpha sea adecuado
        if target < 0 or target > 255:
            raise ValueError(f"UIElement {self.name}: Alpha fuera de rango (0-255)")
        
        self.target_alpha = float(target)

        # Si no hay duración (duration == 0), el cambio se hace de inmediato.
        if duration <= 0:
            self.alpha = target
            self._is_fading = False
            return

        # Calcula la diferencia entre el target_alpha y el alpha original.
        diff = abs(self.alpha - self.target_alpha)

        # Calcula cuanto debe ir sumandole al alpha actual
        # para determinar la velocidad en el que se hace el cambio.
        if diff > 1:
            self.fade_speed = diff / duration
            self._is_fading = True
        else:
            self._is_fading = False



    # --- MÉTODOS ABSTRACTOS ---
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Renderiza el elemento en la superficie destino."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Método abstracto para actualizar los elementos, 
        todas las clases hijas deben implementarlo.
        
        Por defecto tiene la lógica para hacer un cambio progresivo del alpha,
        y aquellos elementos que tengan transparencia deben hacer un 'super().update'.
        """
        # Lógica para el fading
        if self.is_fading:
            # Si el target_alpha es mayor, se suma
            if self.alpha < self.target_alpha:
                self.alpha += self.fade_speed * dt
                # Si se excede el valor objetivo, se fija
                if self.alpha >= self.target_alpha:
                    self.alpha = self.target_alpha
                    self._is_fading = False
            
            # Si el target_alpha es menor, se resta
            else:
                self.alpha -= self.fade_speed * dt

                # Si se excede el valor objetivo, se fija
                if self.alpha <= self.target_alpha:
                    self.alpha = self.target_alpha   
                    self._is_fading = False     