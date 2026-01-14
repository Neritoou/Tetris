from arcade_machine_sdk import json
from typing import Dict, List, Set, Tuple, Any
from ..util.conversors import pygame_key_to_str, str_to_pygame_key
from ..controller.map_config import KeyMap
from .base_config import BaseConfig

class ControlsConfig(BaseConfig):
    """
    Manager responsable de:
    - Cargar el mapeo de teclas desde JSON
    - Guardar el estado actual en JSON
    - Convertir entre nombres legibles y pygame.K_*

    IMPORTANTE:
    Esta clase NO es dueña del estado.
    El estado real vive en KeyMapConfig (singleton lógico).
    """
    def __init__(self, *, path: str):
        """
        Inicializa el manager y sincroniza el estado desde el JSON.

        :param config_path: Ruta al archivo controls.json
        """
        self.config_path = path
        # Mapeo: context -> action -> set de teclas (pygame.K_*)
        self._key_map: Dict[str, Dict[str, Set[int]]] = KeyMap.get_key_map()
        # Mapeo Inverso: Pygame -> Lista de (context, action)
        self._key_to_actions: Dict[int, List[Tuple[str, str]]] = KeyMap.get_key_to_actions()
        # Sincroniza memoria ← JSON
        self.load()

        super().__init__(data = self._key_map)
        self._data: Dict[str, Dict[str, Set[int]]] = self._data

    def get_data(self):
        return self._data
    
    def get_keys_for_action(self, context: str, action: str) -> List[int]:
        """
        Devuelve las teclas asignadas a una acción.

        :return: Lista de pygame.K_*
        """
        KeyMap.assert_action(context, action)
        return list(self._key_map.get(context, {}).get(action, set()))
    
    # Cargar la variable con los datos del JSON
    def load(self) -> None:
        """
        Carga el mapeo de teclas desde el JSON.

        Flujo: 
        
        JSON -> validación -> conversión -> estado global
        """
        data = json.load(self.config_path)
        for context, actions in data.items():
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

    def apply_changes(self):
        super().apply_changes()
        self.save()

    # Guardar los datos de la variable en el JSON
    def save(self) -> None:
        """
        Guarda el estado actual del mapeo en el JSON.

        Flujo:
        
        estado global -> conversión -> JSON
        """
        json_data: Dict[str, Any] = {}

        # Modificar solo la sección de "controls" y convertir las teclas
        for context, actions in self._key_map.items():
            if context not in json_data:
                json_data[context] = {}
            for action, keys in actions.items():
                # Convertir las teclas de Pygame a nombres legibles
                readable_keys = [pygame_key_to_str(key) for key in keys]
                json_data[context][action] = readable_keys
        json.save(self.config_path, json_data)


    def _bind_keys_to_action(self, context: str, action: str, keys: List[int]) -> None:
        """Asocia múltiples teclas a una acción dentro de un contexto.

        Este método se utiliza únicamente al cargar los datos del JSON"""
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