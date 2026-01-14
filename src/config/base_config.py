from typing import Any, Dict
from arcade_machine_sdk import json
from copy import deepcopy

class BaseConfig():
    def __init__(self, *, path: str = "", data: Dict[str, Any] = {}):

        if path: self._data = json.load(path)
        elif data: self._data = data
        else: raise ValueError(f"BaseConfig: no se implementó ninguna estrategia de inicialización")
  
        self._buffer = deepcopy(self._data)  # Buffer temporal
        self._modified_keys = set()  # Claves modificadas

    # --- Acceso seguro al buffer ---
    def get(self, key: Any) -> Any:
        """Devuelve el valor del buffer para la clave dada."""
        return self._buffer.get(key)

    def set(self, key: Any, value: Any) -> None:
        """Modifica el buffer y marca la clave como modificada automáticamente."""
        self._buffer[key] = value
        self._modified_keys.add(key)

    def apply_changes(self):
        """Aplica solo las claves modificadas al data."""
        for key in self._modified_keys:
            self._data[key] = self._buffer[key]
        self._modified_keys.clear()

    def discard_changes(self):
        """Descarta los cambios en el buffer."""
        self._buffer = deepcopy(self._data)
        self._modified_keys.clear()

    def get_data(self) -> Any:
        """ Retorna el diccionario de datos de la Configuración"""
        return self._data