import pygame
from arcade_machine_sdk import GameBase, GameMeta
from src.resources import ResourceManager
from src.controller import InputManager
from src.states import StateManager, PlayState

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)

        self.resource_manager = ResourceManager()
        self.input_manager = InputManager("config/controls.json")
        self.state_manager = StateManager(self)
        # Estado inicial
        self.state_manager.change(PlayState, self)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.input_manager.update(events)
        self.state_manager.handle_input(events)

    def update(self, dt: float) -> None:
        self.state_manager.update(dt)

    def render(self) -> None:
        self.surface.fill((0, 0, 0))
        self.state_manager.render(self.surface)

