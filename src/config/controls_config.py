from arcade_machine_sdk import json
from ..util.conversors import pygame_key_to_str, str_to_pygame_key
from .base_config import BaseConfig

# Formato interno: {"play": {"move_left": {97, 276}}}
ControlsConfigType = dict[str, dict[str, set[int]]]

class ControlsConfig(BaseConfig[ControlsConfigType]):

    """
    Gestiona la configuración de controles del juego.
    
    Responsabilidades:
    1. Cargar JSON (strings) -> Convertir a pygame.K_* (ints)
    2. Guardar pygame.K_* (ints) -> JSON (strings)
    3. Gestionar buffer de cambios (heredado de BaseConfig)
    """
    
    def __init__(self, *, path: str, max_keys_for_action: int = 2):
        """
        Args:
            path: Ruta al archivo controls.json
        """
        self.path = path
        self.max_keys_for_action = max_keys_for_action
        
        # Cargar JSON y convertir
        raw = json.load(path)
        converted = self._convert_from_json(raw)
        
        # Inicializar BaseConfig
        super().__init__(data=converted)
    
    # --- CONVERSIÓN JSON ↔ INTERNO ---
    
    def _convert_from_json(self, raw: dict) -> ControlsConfigType:
        """
        JSON -> Interno
        {"play": {"move_left": ["a", "LEFT"]}} -> {"play": {"move_left": {97, 276}}}
        """
        result: ControlsConfigType = {}
        
        for context, actions in raw.items():
            result[context] = {}
            
            for action, key_names in actions.items():

                if len(key_names) > self.max_keys_for_action:
                    raise ValueError(f"Controls Config: Se sobrepasó el limite asignado de keys en '{context}.{action}'")

                # Convertir lista de strings a set de ints
                pygame_keys = {str_to_pygame_key(name) for name in key_names}
                result[context][action] = pygame_keys
        
        return result
    
    def _convert_to_json(self) -> dict:
        """
        Interno → JSON
        {"play": {"move_left": {97, 276}}} → {"play": {"move_left": ["a", "LEFT"]}}
        """
        result = {}
        
        for context, actions in self._data.items():
            result[context] = {}
            
            for action, pygame_keys in actions.items():

                if len(pygame_keys) > self.max_keys_for_action:
                    raise ValueError(f"Controls Config: Se sobrepasó el limite asignado de keys en '{context}.{action}'")

                # Convertir set de ints a lista de strings
                key_names = [pygame_key_to_str(k) for k in pygame_keys]
                result[context][action] = key_names
        
        return result
    
    # --- OPERACIONES PRINCIPALES ---
    
    def apply_changes(self) -> None:
        """Aplica cambios y guarda al JSON."""
        super().apply_changes()
        json.save(self.path, self._convert_to_json())
    
    def reload(self) -> None:
        """Recarga desde el archivo, descartando cambios no guardados."""
        raw = json.load(self.path)
        self._data = self._convert_from_json(raw)
        self._buffer = self._data.copy()
        self._modified = False
