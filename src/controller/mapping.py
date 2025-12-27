from arcade_machine_sdk import json
from typing import Dict, List, Set, Tuple
from ..util.conversors import pygame_key_to_str, str_to_pygame_key
from .map_config import KeyMapConfig

class KeyMappingManager:
    """Gestiona el mapeo de teclas, carga y guardado."""
    def __init__(self, config_path: str):
        self.config_path = config_path
        # Mapeo: context -> action -> set de teclas (pygame.K_*)
        self._key_map: Dict[str, Dict[str, Set[int]]] = KeyMapConfig.get_key_map()
        # Mapeo Inverso: Pygame -> Lista de (context, action)
        self._key_to_actions: Dict[int, List[Tuple[str, str]]] = KeyMapConfig.get_key_to_actions()
        self.load()

    def get_keys_for_action(self, context: str, action: str) -> List[int]:
        KeyMapConfig.assert_action(context, action)
        return list(self._key_map.get(context, {}).get(action, set()))
    
    # Cargar la variable con los datos del JSON
    def load(self) -> None:
        """Carga el mapeo de teclas desde un archivo JSON."""
        data = json.load(self.config_path)
        controls = data.get("controls")
        if not isinstance(controls, dict):
            raise ValueError("Input Manager: El JSON debe contener una clave inicial 'controls' con un valor Dict")

        for context, actions in controls.items():
            if not isinstance(actions, dict):
                raise ValueError(f"Input Manager: Contexto '{context}' inválido, debe tener un valor Dict")

            for action, keys in actions.items():
                if not isinstance(keys, list):
                    raise ValueError(f"Input Manager: Las teclas de '{action}' en '{context}' deben ser una Lista")

                pygame_keys = [str_to_pygame_key(key_name) for key_name in keys]

                if len(pygame_keys) > 2:
                    raise ValueError(f"Input Manager: La acción '{action}' en el contexto '{context}' no puede tener más de 2 teclas asignadas.")

                # Asocia las teclas convertidas a la acción
                self._bind_keys_to_action(context, action, pygame_keys)

    # Guardar los datos de la variable en el JSON
    def save(self) -> None:
        """Guarda el mapeo de teclas en un archivo JSON sin recrear todo el diccionario."""
        json_data = json.load(self.config_path)

        # Asegurarse de que la clave "controls" exista
        if "controls" not in json_data:
            json_data["controls"] = {}

        # Modificar solo la sección de "controls" y convertir las teclas
        for context, actions in self._key_map.items():
            if context not in json_data["controls"]:
                json_data["controls"][context] = {}
            for action, keys in actions.items():
                # Convertir las teclas de Pygame a nombres legibles
                readable_keys = [pygame_key_to_str(key) for key in keys]
                json_data["controls"][context][action] = readable_keys

        json.save(self.config_path, json_data)


    def _bind_keys_to_action(self, context: str, action: str, keys: List[int]) -> None:
        """Asocia múltiples teclas a una acción dentro de un contexto."""
        # key_map 
        self._key_map.setdefault(context, {})
        self._key_map[context].setdefault(action, set())
        self._key_map[context][action].update(keys)

        # key_to_actions (mapa inverso) 
        for key in keys:
            self._key_to_actions.setdefault(key, [])
            pair = (context, action)
            if pair not in self._key_to_actions[key]:
                self._key_to_actions[key].append(pair)

