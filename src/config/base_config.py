from typing import Dict, Any
from arcade_machine_sdk import json
from copy import deepcopy

class BaseConfig():
    def __init__(self, *, path: str = "", data: Dict[Any, Any]= {}):

        if path: self.data = json.load(path)
        elif data: self.data = data
        else: raise ValueError(f"BaseConfig: no se implementó ninguna estrategia de inicialización")
  
        self._buffer = deepcopy(self.data)  # Buffer temporal
        self._modified_keys = set()  # Claves modificadas

    # --- Acceso seguro al buffer ---
    def get(self, key: str) -> Any:
        """Devuelve el valor del buffer para la clave dada."""
        return self._buffer.get(key)

    def set(self, key: str, value: Any) -> None:
        """Modifica el buffer y marca la clave como modificada automáticamente."""
        self._buffer[key] = value
        self._modified_keys.add(key)

    def apply_changes(self):
        """Aplica solo las claves modificadas al data."""
        for key in self._modified_keys:
            self.data[key] = self._buffer[key]
        self._modified_keys.clear()

    def discard_changes(self):
        """Descarta los cambios en el buffer."""
        self._buffer = deepcopy(self.data)
        self._modified_keys.clear()