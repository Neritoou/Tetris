from typing import cast, Any, Hashable, TypeVar, Generic
from arcade_machine_sdk import json
from copy import deepcopy

T = TypeVar('T')

class BaseConfig(Generic[T]):
    """
    Clase base para manejar configuraciones.
    
    Permite modificar configuraciones sin alterar los datos originales
    hasta que se apliquen explícitamente.
    """
    def __init__(self, *, path: str = "", data: T | None = None):
        """
        Inicializa la configuración desde un archivo JSON o un diccionario.
        
        Args:
            path: Ruta al archivo JSON (mutuamente excluyente con data)
            data: Diccionario con los datos (mutuamente excluyente con path)
        """
        if path and data is not None:
            raise ValueError("BaseConfig: no puedes proporcionar 'path' y 'data' simultáneamente")
        if path:
            self._data: T = cast(T, json.load(path))
        elif data is not None:
            self._data: T = deepcopy(data) # Evita modificar el diccionario original
        else:
            raise ValueError("BaseConfig: debes proporcionar 'path' o 'data'")
  
        self._buffer: T = deepcopy(self._data)  # Buffer temporal
        self._modified_keys: set[tuple[Hashable, ...]]= set()  # Claves modificadas

    def _navigate_to_parent(self, data: Any, keys: tuple[Hashable, ...]) -> Any:
        """
        Navega hasta el contenedor padre (penúltimo nivel).
        
        Ejemplo:
            keys = ("general", "starting_level")
            
            Para GET: 
                parent = _navigate_to_parent(data, keys)
                value = parent[keys[-1]] 
            
            Para SET:
                parent = _navigate_to_parent(data, keys)
                parent[keys[-1]] = new_value
        """
        if not keys:
            raise ValueError("BaseConfig: 'keys' debe proporcionar al menos una Key")
        
        current = data
        
        for key in keys[:-1]:
            if not isinstance(current, dict):
                raise TypeError(f"BaseConfig: valor intermedio no es un diccionario")
            if key not in current:
                raise KeyError(f"BaseConfig: clave '{key}' no existe")
            current = current[key]
        
        # Verificar que el contenedor final es un dict
        if not isinstance(current, dict):
            raise TypeError(f"BaseConfig: el contenedor padre no es un diccionario")
        
        return current

    def get(self, *keys: Hashable) -> Any:
        """Obtiene un valor anidado del buffer."""
        parent = self._navigate_to_parent(self._buffer, keys)
        
        # Verificar que la clave final existe
        if keys[-1] not in parent:
            raise KeyError(f"BaseConfig: la clave '{keys[-1]}' no existe")
        
        return parent[keys[-1]]

    def set(self, value: Any, *keys: Hashable) -> None:
        """Establece un valor anidado en el buffer."""
        parent = self._navigate_to_parent(self._buffer, keys)

        if keys[-1] not in parent:
            raise KeyError(f"BaseConfig: la clave '{keys[-1]}' no existe en la config original")
        
        # Aplicar en buffer y guardar en las keys modificadas
        parent[keys[-1]] = value
        self._modified_keys.add(keys)
        
    def apply_changes(self) -> None:
        """
        Aplica los cambios del buffer a los datos originales.
        Solo aplica las claves que fueron modificadas.
        """
        if not self._modified_keys:
            return
            
        for keys in self._modified_keys:
            # Navegar a los padres usando la función existente
            parent_buffer = self._navigate_to_parent(self._buffer, keys)
            parent_data = self._navigate_to_parent(self._data, keys)
            
            # Copiar el valor
            final_key = keys[-1]
            parent_data[final_key] = deepcopy(parent_buffer[final_key])
        
        self._modified_keys.clear()

    def has_changes(self) -> bool:
        """Verifica si hay cambios pendientes."""
        return True if self._modified_keys else False
    
    def discard_changes(self) -> None:
        """Descarta todos los cambios pendientes, restaurando desde los datos originales."""
        self._buffer = deepcopy(self._data)
        self._modified_keys.clear()

    def save(self, path: str) -> None:
        """Guarda los datos originales (con cambios aplicados) en un archivo JSON."""
        if not path:
            raise ValueError("BaseConfig: no hay ruta de archivo disponible para guardar")
        
        json.save(path, cast(dict[str,Any], self._data))

    # (?) VER SI SE MODIFICA ESTA FORMA DE ACCESO
    @property
    def data(self) -> T:
        """Retorna los datos originales."""
        return self._data
    
    @property
    def buffer(self) -> T:
        """Retorna el buffer actual."""
        return self._buffer
    