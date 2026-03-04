import math
from enum import Flag, auto


class ShakeDirection(Flag):
    VERTICAL   = auto()
    HORIZONTAL = auto()
    BOTH       = VERTICAL | HORIZONTAL


class ScreenShake:
    """Calcula un offset amortiguado para simular un tambaleo de pantalla."""

    def __init__(self, intensity: int = 4, duration: float = 0.2) -> None:
        self._intensity = intensity
        self._duration  = duration
        self._timer: float = 0.0
        self._use_x: bool  = False
        self._use_y: bool  = True

    @property
    def is_active(self) -> bool:
        return self._timer > 0.0

    @property
    def offset(self) -> tuple[int, int]:
        if not self.is_active:
            return (0, 0)
        progress = self._timer / self._duration
        value    = int(math.sin(self._timer * 60) * self._intensity * progress)
        return (value if self._use_x else 0, value if self._use_y else 0)

    def trigger(self, direction: ShakeDirection = ShakeDirection.VERTICAL) -> None:
        self._timer = self._duration
        self._use_x = ShakeDirection.HORIZONTAL in direction
        self._use_y = ShakeDirection.VERTICAL   in direction

    def update(self, dt: float) -> None:
        if self.is_active:
            self._timer = max(0.0, self._timer - dt)