import pygame
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.config import ControlsConfig


# Diccionario estático global, se calcula una sola vez al importar
PYGAME_KEY_TO_NAME: Dict[int, str] = {
    value: name[2:].lower()
    for name, value in pygame.__dict__.items()
    if name.startswith("K_")
}

# Mapa inverso case-insensitive para leer el JSON
NAME_TO_PYGAME_KEY: Dict[str, int] = {
    name.lower(): key  # "left"→276, "a"→97, "space"→32
    for key, name in PYGAME_KEY_TO_NAME.items()
}

def str_to_pygame_key(key_name: str) -> int:
    result = NAME_TO_PYGAME_KEY.get(key_name.lower())
    if result is None:
        raise ValueError(f"Tecla inválida en configuración: '{key_name}'")
    return result


def pygame_key_to_str(pygame_key: int) -> str:
    try:
        return PYGAME_KEY_TO_NAME[pygame_key]
    except KeyError:
        raise ValueError(f"Tecla Pygame no válida: '{pygame_key}'")
    
def get_hint_key(controller: "ControlsConfig", action: str) -> str:
    keys = controller.get("ui", action)  # set[int]

    key = pygame_key_to_str(min(keys)).upper() if keys else "?"

    if key == "RETURN":
        return "ENTER"
    elif key == "ESCAPE":
        return "ESC"

    return key