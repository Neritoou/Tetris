from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config.gameplay import AutoLockType, ColissionDelayLockType, FixedLockType, ResettableLockType
    
class LockStrategy(ABC):
    def __init__(self, name: str, lock_config: dict[str, Any]):
        self.delay: float = lock_config.get("lock_delay", 0.8)
        self.timer: float = 0.0
        self._name: str = name
        self._lock_config = lock_config

    @property
    def name(self) -> str:
        """Nombre de la estrategia"""
        return self._name
    
    def reset_timer(self) -> None:
        """ Establece el contador de bloqueo en 0.0"""
        self.timer = 0.0
    
    @abstractmethod
    def update(self, dt: float, is_colliding: bool) -> None:
        """Actualiza el temporizador según la estrategia"""
        pass

    @abstractmethod
    def on_move(self) -> None:
        """Se llama cuando la pieza se mueve o rota, para reiniciar el temporizador si aplica"""
        pass

    @abstractmethod
    def is_locked(self) -> bool:
        """Devuelve True si la pieza debe bloquearse"""
        pass

class AutoLock(LockStrategy):
    """Lock instantáneo"""
    def __init__(self, name: str, lock_config: dict[str, Any]):
        super().__init__(name, lock_config)
        self._lock_config: "AutoLockType" = self._lock_config
    def update(self, dt: float, is_colliding: bool) -> None:
        self.timer = self.delay if is_colliding else 0.0

    def on_move(self) -> None:
        pass  # no hay reseteos, bloqueo instantáneo

    def is_locked(self) -> bool:
        return True


class FixedLock(LockStrategy):
    """Lock clásico, con lock_delay"""
    def __init__(self, name: str, lock_config: dict[str, Any]):
        super().__init__(name, lock_config)
        self._lock_config: "FixedLockType" = self._lock_config

    def update(self, dt: float, is_colliding: bool) -> None:
        if is_colliding:
            self.timer += dt
        else:
            self.timer = 0.0

    def on_move(self) -> None:
        pass  # no se reinicia el temporizador

    def is_locked(self) -> bool:
        return self.timer >= self.delay


# (!) VER ESTA
class ResettableLock(LockStrategy):
    """Lock que permite reinicios mientras la pieza se mueve o rota"""
    def __init__(self, name: str, lock_config: dict[str, Any]):
        super().__init__(name, lock_config)
        self._lock_config: "ResettableLockType" = self._lock_config
        self._max_moves: int = self._lock_config["max_moves"]
        self._moves: int = 0

    def update(self, dt: float, is_colliding: bool) -> None:
        if is_colliding:
            self.timer += dt
        else:
            self.timer = 0.0
            self._moves = 0

    def on_move(self) -> None:
        if self._moves < self._max_moves:
            self.timer = 0.0
            self._moves += 1

    def is_locked(self) -> bool:
        return self.timer >= self.delay or self._moves >= self._max_moves
    

class CollisionDelayLock(LockStrategy):
    """Lock que solo cuenta el temporizador mientras la pieza colisiona"""
    def __init__(self, name: str, lock_config: dict[str, Any]):
        super().__init__(name, lock_config)
        self._lock_config: "ColissionDelayLockType" = self._lock_config

    def update(self, dt: float, is_colliding: bool) -> None:
        if is_colliding:
            self.timer += dt
        else:
            self.timer = 0.0

    def on_move(self) -> None:
        pass  # no se reinicia con movimientos, solo depende de la colisión

    def is_locked(self) -> bool:
        return self.timer >= self.delay
    

