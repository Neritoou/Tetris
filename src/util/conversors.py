import pygame
from typing import Dict


# Diccionario estático global, se calcula una sola vez al importar
PYGAME_KEY_TO_NAME: Dict[int, str] = {
    value: name[2:].lower()
    for name, value in pygame.__dict__.items()
    if name.startswith("K_")
}

def str_to_pygame_key(key_name: str) -> int:
    attr = f"K_{key_name}"
    if not hasattr(pygame, attr):
        raise ValueError(f"Tecla inválida en configuración: '{key_name}'")
    return getattr(pygame, attr)


def pygame_key_to_str(pygame_key: int) -> str:
    try:
        return PYGAME_KEY_TO_NAME[pygame_key]
    except KeyError:
        raise ValueError(f"Tecla Pygame no válida: '{pygame_key}'")

