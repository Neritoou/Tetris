from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.game import Game
    from ..core import OverlayType
    import pygame

class GameState(ABC):
    """
    Clase base abstracta para los diferentes estados del juego.
    Los estados como 'MainMenu', 'Playing', 'Paused', 'GameOver', etc. deben heredar de esta clase.
    """

    def __init__(self, game: "Game") -> None:
        """
        Inicializa el estado del juego con una referencia al objeto Game.

        Args:
            game: El objeto principal del juego, para tener acceso a las propiedades y métodos.
        """
        self.game = game

    @abstractmethod
    def on_enter(self) -> None:
        """
        Método llamado cuando el estado se entra (cuando el juego cambia a este estado).
        Se pueden inicializar recursos o preparar el estado.
        """
        pass

    @abstractmethod
    def on_exit(self) -> None:
        """
        Método llamado cuando el estado se sale (cuando el juego cambia desde este estado).
        Se pueden liberar recursos o realizar limpieza.
        """
        pass

    @abstractmethod
    def handle_input(self, events: "List[pygame.event.Event]") -> None:
        """
        Método para manejar la entrada del usuario. 
        Los eventos de teclas, ratón, etc., deben ser procesados aquí.
        
        Args:
            events: Lista de eventos de pygame capturados en el bucle de juego.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Método que actualiza el estado del juego. 
        Debe actualizar la lógica del juego.

        Args:
            dt: El tiempo transcurrido desde la última actualización en segundos (delta time).
        """
        pass

    @abstractmethod
    def render(self, surface: "pygame.Surface") -> None:
        """
        Método para dibujar en la pantalla. 
        Los estados del juego deben dibujar los elementos en la pantalla en este método.

        Args:
            surface: La superficie sobre la cual se dibuja (por ejemplo, la pantalla del juego).
        """
        pass

    @property
    @abstractmethod
    def overlay_type(self) -> "OverlayType":
        """
        Tipo de overlay del estado.
        - NONE: estado normal
        - SEMITRANSPARENT: overlay que permite renderizar el fondo
        - FULLSCREEN: overlay que bloquea renderizado de fondo
        """
        pass

    @property
    @abstractmethod
    def is_transient(self) -> bool:
        """
        Método que determina si el estado es transitorio (por ejemplo, una animación de introducción).
        Los estados transitorios se eliminan o cambian después de un breve periodo de tiempo.

        Return: True si el estado es transitorio, False si es persistente.
        """
        pass