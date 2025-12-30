import pygame
from arcade_machine_sdk import GameBase, GameMeta
from ..resources import ResourceManager
from ..controller import InputManager
from ..states import *

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)
        self.resources: ResourceManager = ResourceManager()
        self.input: InputManager = InputManager("config/controls.json")
        self.state: StateManager = StateManager(self)

    def start(self, surface: pygame.Surface):
        super().start(surface)
        # Cargar Recursos 
        self.resources.load()
        # Estado inicial       
        self.state.change(StateID.PLAY)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.input.update(events)
        self.state.handle_input(events)

    def update(self, dt: float) -> None:
        self.state.update(dt)

    def render(self) -> None:
        self.surface.fill((0, 0, 0))
        self.state.render(self.surface)