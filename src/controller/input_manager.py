import pygame
from arcade_machine_sdk import json
from typing import Dict, Set, List, Tuple



# (!) MODIFICAR DONDE SE UBICARÁ LA CARPETA (POSIBLE src/managers)
# (!) AÑADIR METODOS PARA LA MODIFICACION DE TECLAS EN OPCIONES

class InputManager:
    """
    Administra el estado de los controles y mapea teclas a acciones semánticas.
    También permite guardar y cargar configuraciones de teclas desde un archivo JSON.
    """

    # Diccionario inverso estático para convertir pygame keys a nombres
    _pygame_key_to_name: Dict[int, str] = {
        value: name[2:].lower() 
        for name, value in pygame.__dict__.items() 
        if name.startswith("K_")
    }

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path

        # Mapeo: context -> action -> set de teclas (pygame.K_*)
        self.key_map: Dict[str, Dict[str, Set[int]]] = {}

        # Estados de acciones presionadas, mantenidas y liberadas
        self._pressed: Set[Tuple[str, str]] = set()
        self._held: Set[Tuple[str, str]] = set()
        self._released: Set[Tuple[str, str]] = set()

        # Mapeo inverso: tecla pygame -> lista de (context, action)
        self._key_to_actions: Dict[int, List[Tuple[str, str]]] = {}

        self.load_key_mapping()


    # (?) Ver defaultDics para facilitar busquedas
    def update(self, events: List[pygame.event.Event]) -> None:
            """Actualiza los estados de las acciones según los eventos del frame."""
            self._pressed.clear()
            self._released.clear()

            for event in events:
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    key = event.key
                    actions = self._key_to_actions.get(key, [])
                    for context, action in actions:
                        identifier = (context, action)
                        if event.type == pygame.KEYDOWN:
                            if identifier not in self._held:
                                self._pressed.add(identifier)
                            self._held.add(identifier)
                        else:  # KEYUP
                            self._released.add(identifier)
                            self._held.discard(identifier)

    def is_pressed(self, context: str, action: str) -> bool:
        return (context, action) in self._pressed

    def is_held(self, context: str, action: str) -> bool:
        return (context, action) in self._held

    def is_released(self, context: str, action: str) -> bool:
        return (context, action) in self._released

    def get_keys_for_action(self, context: str, action: str) -> List[int]:
        self._assert_action(context,action)
        return list(self.key_map.get(context, {}).get(action, set()))
    
    def load_key_mapping(self) -> None:
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

                pygame_keys = [self._str_to_pygame_key(key_name) for key_name in keys]

                if len(pygame_keys) > 2:
                    raise ValueError(f"Input Manager: La acción '{action}' en el contexto '{context}' no puede tener más de 2 teclas asignadas.")

                # Asocia las teclas convertidas a la acción
                self._bind_keys_to_action(context, action, pygame_keys)

    def save_key_mapping(self) -> None:
        """Guarda el mapeo de teclas en un archivo JSON sin recrear todo el diccionario."""
        json_data = json.load(self.config_path)

        # Asegurarse de que la clave "controls" exista
        if "controls" not in json_data:
            json_data["controls"] = {}

        # Modificar solo la sección de "controls" y convertir las teclas
        for context, actions in self.key_map.items():
            if context not in json_data["controls"]:
                json_data["controls"][context] = {}
            for action, keys in actions.items():
                # Convertir las teclas de Pygame a nombres legibles
                readable_keys = [self._pygame_key_to_str(key) for key in keys]
                json_data["controls"][context][action] = readable_keys

        json.save(self.config_path, json_data)


    # --- HELPERS ---
    def _bind_keys_to_action(self, context: str, action: str, keys: List[int]) -> None:
        """Asocia múltiples teclas a una acción dentro de un contexto."""
        if context not in self.key_map:
            self.key_map[context] = {}

        # Agregar las teclas a la acción correspondiente
        if action not in self.key_map[context]:
            self.key_map[context][action] = set()
        
        # Añadir teclas al conjunto de teclas de la acción
        self.key_map[context][action].update(keys)


    @staticmethod
    def _str_to_pygame_key(key_name: str) -> int:
        """ Convierte una tecla string ("left", "space") a pygame.K_* """
        attr = f"K_{key_name}"
        if not hasattr(pygame, attr):
            raise ValueError(f"Tecla inválida en configuración: '{key_name}'")
        return getattr(pygame, attr)

    @staticmethod
    def _pygame_key_to_str(pygame_key: int) -> str:
        """Convierte una tecla pygame.K_* a string ("left", "space")."""
        try:
            return InputManager._pygame_key_to_name[pygame_key]
        except KeyError:
            raise ValueError(f"Tecla Pygame no válida: '{pygame_key}'")

    def _assert_context(self, context: str) -> None:
        if context not in self.key_map:
            raise ValueError(
                f"Input Manager: El contexto '{context}' no existe. "
                f"Contextos disponibles: {list(self.key_map.keys())}"
            )
        
    def _assert_action(self, context: str, action: str) -> None:
        self._assert_context(context)

        if action not in self.key_map[context]:
            raise ValueError(
                f"InputManager: La acción '{action}' no existe en el contexto '{context}'. "
                f"Acciones disponibles: {list(self.key_map[context].keys())}"
            )

    def __repr__(self):
        return f"<InputManager key_map={self.key_map}>"