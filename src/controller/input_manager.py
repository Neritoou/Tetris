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

        # Estados de teclas
        self._key_pressed: Set[Tuple[str, str]] = set()
        self._key_held: Set[Tuple[str, str]] = set()
        self._key_released: Set[Tuple[str, str]] = set()

        # Estados de botones del mouse
        self._mouse_pressed: Set[int] = set() 
        self._mouse_held: Set[int] = set()  
        self._mouse_released: Set[int] = set()  

        # Mapeo inverso: tecla pygame -> lista de (context, action)
        self._key_to_actions: Dict[int, List[Tuple[str, str]]] = {}

        self.load_key_mapping()

    # --- 
    def is_key_pressed(self, context: str, action: str) -> bool:
        """Verifica si la acción está presionada en el contexto."""
        self._assert_action(context, action)
        return (context, action) in self._key_pressed

    def is_key_held(self, context: str, action: str) -> bool:
        """Verifica si la acción está mantenida en el contexto."""
        self._assert_action(context, action)
        return (context, action) in self._key_held

    def is_key_released(self, context: str, action: str) -> bool:
        """Verifica si la acción ha sido liberada en el contexto."""
        self._assert_action(context, action)
        return (context, action) in self._key_released
    
    def is_mouse_pressed(self, button: int) -> bool:
        """Verifica si el botón del mouse está presionado."""
        return button in self._mouse_pressed

    def is_mouse_held(self, button: int) -> bool:
        """Verifica si el botón del mouse está mantenido."""
        return button in self._mouse_held

    def is_mouse_released(self, button: int) -> bool:
        """Verifica si el botón del mouse ha sido liberado."""
        return button in self._mouse_released

    def get_mouse_pos(self) -> Tuple[int, int]:
        """Obtiene la posición actual del mouse."""
        return pygame.mouse.get_pos()   
    
    # --- DETECCIÓN DE INPUT ---
    def update(self, events: List[pygame.event.Event]) -> None:
        """Actualiza los estados de las acciones según los eventos del frame."""
        # Limpiar estados previos
        self._key_pressed.clear()
        self._key_released.clear()
        self._mouse_released.clear()

        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self._handle_key_event(event)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self._handle_mouse_event(event)

    # Detectar input del Teclado
    def _handle_key_event(self, event: pygame.event.Event) -> None:
        """Maneja los eventos de teclas (KEYDOWN, KEYUP)."""
        key = event.key
        # Se obtienen todas las acciones relacionadas a la key
        actions = self._key_to_actions.get(key, [])
                
        for context, action in actions:
            identifier = (context, action)

            if event.type == pygame.KEYDOWN:
                # Si es la primera vez que se presiona, añadir a _pressed
                if identifier not in self._key_held:
                    self._key_pressed.add(identifier)  
                self._key_held.add(identifier) # Siempre se marca como "held"
                    
            elif event.type == pygame.KEYUP:
                self._key_released.add(identifier)  # Marcar como liberado
                self._key_held.discard(identifier)  # Eliminar de los mantenidos   

    # Detectar input del Mouse
    def _handle_mouse_event(self, event: pygame.event.Event) -> None:
        """Maneja los eventos de mouse (MOUSEBUTTONDOWN, MOUSEBUTTONUP)."""
        button = event.button
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si es la primera vez que se presiona, añadir a _pressed
            if button not in self._mouse_held:
                self._mouse_pressed.add(button)
            self._mouse_held.add(button) # Siempre se marca como "held"

        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_released.add(button) # Marcar como liberado
            self._mouse_held.discard(button) # Eliminar de los mantenidos 

    
    # --- CARGA Y ACTUAALIZACIÓN DEL JSON ---
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
    def get_keys_for_action(self, context: str, action: str) -> List[int]:
        self._assert_action(context,action)
        return list(self.key_map.get(context, {}).get(action, set()))
    
    def _bind_keys_to_action(self, context: str, action: str, keys: List[int]) -> None:
        """Asocia múltiples teclas a una acción dentro de un contexto."""
        # key_map 
        self.key_map.setdefault(context, {})
        self.key_map[context].setdefault(action, set())
        self.key_map[context][action].update(keys)

        # key_to_actions (mapa inverso) 
        for key in keys:
            self._key_to_actions.setdefault(key, [])
            pair = (context, action)
            if pair not in self._key_to_actions[key]:
                self._key_to_actions[key].append(pair)

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