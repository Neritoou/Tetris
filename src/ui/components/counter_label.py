from src.ui.components.label import UILabel
from enum import Enum, auto
from typing import Callable
import pygame


class _State(Enum):
    """Estados internos del contador animado."""
    IDLE     = auto()  # Sin animación activa
    WAITING  = auto()  # Esperando el delay inicial antes de contar
    COUNTING = auto()  # Animando el valor hacia el objetivo
    DONE     = auto()  # Animación completada


class UICounterLabel(UILabel):
    """
    Label que anima su valor numérico desde 0 hasta un objetivo en un tiempo fijo.

    Permanece invisible hasta que se llama a set_target. Una vez completada
    la animación queda en estado DONE mostrando el valor final.

    Uso:
        counter = UICounterLabel("score", x, y, font, fmt=lambda v: f"{int(v):,}")
        counter.set_target(7000, duration=0.7, start_delay=0.3)

    Args:
        element_id: Identificador único del elemento.
        x, y:       Posición en pantalla.
        font:       Fuente pygame para renderizar el texto.
        color:      Color del texto en formato RGB.
        fmt:        Función que convierte el valor float al string a mostrar.
                    Por defecto muestra el valor como entero.
    """

    def __init__(
        self,
        element_id: str,
        x: int,
        y: int,
        font: pygame.font.Font,
        color: tuple = (200, 200, 200),
        fmt: Callable[[float], str] = lambda v: str(int(v)),
        center: bool = False
    ):
        super().__init__(element_id, x, y, fmt(0), font, color, center=center, visible=False)
        self._fmt         = fmt
        self._state       = _State.IDLE
        self._target      = 0.0
        self._duration    = 1.0
        self._start_delay = 0.3
        self._delay_timer = 0.0
        self._timer       = 0.0

    def set_target(self, target: float, duration: float = 0.7,
                   start_delay: float = 0.3) -> None:
        """
        Arranca la animación hacia el valor indicado.

        Resetea el contador y lo pone en estado WAITING. Tras el delay
        inicial empieza a contar linealmente hasta llegar al objetivo.

        Args:
            target:      Valor final al que debe llegar.
            duration:    Segundos que tarda en completarse la animación.
            start_delay: Segundos de espera antes de empezar a contar.
        """
        self._target      = target
        self._duration    = max(duration, 0.01)
        self._start_delay = start_delay
        self._delay_timer = 0.0
        self._timer       = 0.0
        self._state       = _State.WAITING
        self.set_text(self._fmt(0))

    @property
    def is_done(self) -> bool:
        """True cuando el contador llegó al valor final."""
        return self._state == _State.DONE

    def update(self, dt: float) -> None:
        """Actualiza el estado interno y el texto mostrado."""
        super().update(dt)

        match self._state:
            case _State.IDLE | _State.DONE:
                return

            case _State.WAITING:
                self._delay_timer += dt
                if self._delay_timer >= self._start_delay:
                    self._state = _State.COUNTING

            case _State.COUNTING:
                self._timer += dt
                t = min(self._timer / self._duration, 1.0)
                self.set_text(self._fmt(self._target * t))
                if t >= 1.0:
                    self._state = _State.DONE