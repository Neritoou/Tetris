import pygame
from arcade_machine_sdk import GameBase, GameMeta
from src.resources import ResourceManager
from src.controller import InputManager

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)
        rm = ResourceManager()
        input = InputManager("config/controls.json")
        
    


    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass
        
    def update(self, dt: float) -> None:
        pass
        
    def render(self) -> None:
        pass