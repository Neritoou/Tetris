from abc import ABC, abstractmethod
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config.gameplay import ExponentialGravityType, FixedGravityType, ForLevelsGravityType

class GravityStrategy(ABC):
    def __init__(self, name: str, gravity_config: Dict[str, Any]):
        self._gravity_config = gravity_config
        self._name: str = name

    @abstractmethod
    def get_fall_delay(self, level: int) -> float:
        pass
    
    @property
    def name(self) -> str:
        """Nombre de la estrategia utilizada"""
        return self._name

class ExponentialGravity(GravityStrategy):
    def __init__(self, name: str, gravity_config: Dict[str,Any]):
        super().__init__(name, gravity_config)
        self._gravity_config: "ExponentialGravityType" = self._gravity_config
        self._min_delay: float = self._gravity_config["min_delay"]
        self._base_fall_delay: float = self._gravity_config["base_fall_delay"]
        self._multiplier: float = self._gravity_config["multiplier"]
    
    def get_fall_delay(self, level: int) -> float:
        return max(self._min_delay, self._base_fall_delay * (self._multiplier ** (level - 1)))


class FixedGravity(GravityStrategy):
    def __init__(self, name: str, gravity_config: Dict[str,Any]):
        super().__init__(name, gravity_config)
        self._gravity_config: "FixedGravityType" = self._gravity_config
        self._fall_delay: float = self._gravity_config["fall_delay"]
    
    def get_fall_delay(self, level: int = 1) -> float:
        return self._fall_delay
    

class ForLevelsGravity(GravityStrategy):
    def __init__(self, name: str, gravity_config: Dict[str,Any]):
        super().__init__(name, gravity_config)
        self._gravity_config: "ForLevelsGravityType" = self._gravity_config
        self.levels = sorted((int(lvl), delay) for lvl, delay in gravity_config["levels"].items())
        
    def get_fall_delay(self, level: int) -> float:
        last_delay = self.levels[0][1]
        for lvl, delay in self.levels:
            if level < lvl:
                break
            last_delay = delay
        return last_delay
    

