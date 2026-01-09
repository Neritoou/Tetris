from typing import Dict, Set, List, Tuple

class KeyMap:
    """
    Contenedor GLOBAL del mapeo de teclas.

    Su única responsabilidad es mantener el estado compartido
    del sistema de input en memoria y validar su estructura.
    """
    # Mapa principal:
    # context -> action -> teclas (pygame.K_*)
    _key_map: Dict[str, Dict[str, Set[int]]] = {}

    # Mapa inverso:
    # tecla -> [(context, action)]
    _key_to_actions: Dict[int, List[Tuple[str, str]]] = {}


    # --- GETTERS ---
    @classmethod
    def get_key_map(cls) -> Dict[str, Dict[str, Set[int]]]:
        """Devuelve el mapa global context -> action -> teclas."""
        return cls._key_map
    
    @classmethod
    def get_key_to_actions(cls) -> Dict[int, List[Tuple[str, str]]]:
        """"Devuelve el mapa inverso tecla -> (context, action)."""
        return cls._key_to_actions
    
    # --- SETTERS ---
    @classmethod
    def set_key_map(cls, key_map: Dict[str, Dict[str, Set[int]]]) -> None:
        """Reemplaza completamente el mapa global de teclas."""
        cls._key_map = key_map

    @classmethod
    def set_key_to_actions(cls, key_to_actions) -> None:
        """Reemplaza completamente el mapa inverso."""
        cls._key_to_actions = key_to_actions
    

    # --- VALIDACIÓN ---
    @classmethod
    def assert_context(cls,context: str) -> None:
        """
        Verifica que el contexto exista.
        """
        if context not in cls._key_map:
            raise ValueError(
                f"Input Manager: El contexto '{context}' no existe. "
                f"Contextos disponibles: {list(cls._key_map.keys())}"
            )
            
    @classmethod
    def assert_action(cls, context: str, action: str) -> None:
        """
        Verifica que una acción exista dentro de un contexto.
        """
        cls.assert_context(context)
        if action not in cls._key_map[context]:
            raise ValueError(
                f"InputManager: La acción '{action}' no existe en el contexto '{context}'. "
                f"Acciones disponibles: {list(cls._key_map[context].keys())}"
            )