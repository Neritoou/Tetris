class InputMapper:
    """
    Mapea teclas físicas a acciones lógicas.
    """
    def __init__(self, key_map: dict[str, dict[str, set[int]]]):
        """
        Args:
            key_map: Mapeo context → action → {pygame_keys}
        """
        self._key_map = key_map
        self._key_to_actions = self._build_inverse_map()
    
    def _build_inverse_map(self) -> dict[int, list[tuple[str, str]]]:
        """Construye pygame_key → [(context, action), ...]"""
        inverse: dict[int, list[tuple[str, str]]] = {}
        
        for context, actions in self._key_map.items():
            for action, keys in actions.items():
                for key in keys:
                    inverse.setdefault(key, [])
                    pair = (context, action)
                    if pair not in inverse[key]:
                        inverse[key].append(pair)
        
        return inverse
    
    def get_actions_for_key(self, pygame_key: int) -> list[tuple[str, str]]:
        """Obtiene las acciones asociadas a una tecla."""
        return self._key_to_actions.get(pygame_key, [])
    
    def update_mapping(self, key_map: dict[str, dict[str, set[int]]]) -> None:
        """Actualiza el mapeo completo."""
        self._key_map = key_map
        self._key_to_actions = self._build_inverse_map()
    
    def has_action(self, context: str, action: str) -> bool:
        """Verifica si existe una acción en un contexto."""
        return context in self._key_map and action in self._key_map[context]
    
    def assert_action(self, context: str, action: str) -> None:
        """Lanza error si la acción no existe."""
        if context not in self._key_map:
            raise ValueError(
                f"Contexto '{context}' no existe. "
                f"Disponibles: {list(self._key_map.keys())}"
            )
        if action not in self._key_map[context]:
            raise ValueError(
                f"Acción '{action}' no existe en '{context}'. "
                f"Disponibles: {list(self._key_map[context].keys())}"
            )