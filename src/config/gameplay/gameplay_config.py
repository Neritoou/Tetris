from typing import Dict, Any, TYPE_CHECKING
from ..base_config import BaseConfig

if TYPE_CHECKING:
    from .general_types import GameplayConfigType

class GameplayConfig(BaseConfig):
    def __init__(self, *, path: str = "", data: Dict[str, Any] = {}):
        super().__init__(path=path, data = data)
        self._data: "GameplayConfigType" = self._data
        
    def get_data(self) -> "GameplayConfigType":
        """ Retorna el diccionario de datos de la Configuración"""
        return self._data