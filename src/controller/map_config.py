from typing import Dict, Set, List, Tuple

class KeyMapConfig:
    """Clase que contiene el key_map global compartido."""
    _key_map: Dict[str, Dict[str, Set[int]]] = {}
    _key_to_actions: Dict[int, List[Tuple[str, str]]] = {}


    @classmethod
    def get_key_to_actions(cls) -> Dict[int, List[Tuple[str, str]]]:
        return cls._key_to_actions
    
    @classmethod
    def set_key_to_actions(cls, key_to_actions) -> None:
        cls._key_to_actions = key_to_actions

    @classmethod
    def get_key_map(cls) -> Dict[str, Dict[str, Set[int]]]:
        return cls._key_map
    
    @classmethod
    def set_key_map(cls, key_map: Dict[str, Dict[str, Set[int]]]) -> None:
        cls._key_map = key_map

    @classmethod
    def assert_context(cls,context: str) -> None:
        if context not in cls._key_map:
            raise ValueError(
                f"Input Manager: El contexto '{context}' no existe. "
                f"Contextos disponibles: {list(cls._key_map.keys())}"
            )
            
    @classmethod
    def assert_action(cls, context: str, action: str) -> None:
        cls.assert_context(context)
        if action not in cls._key_map[context]:
            raise ValueError(
                f"InputManager: La acción '{action}' no existe en el contexto '{context}'. "
                f"Acciones disponibles: {list(cls._key_map[context].keys())}"
            )
