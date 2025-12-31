from typing import TypedDict
from pygame import Surface
from pygame.font import Font
from pygame.mixer import Sound
from .spritesheet import SpriteSheet

class ImageResource(TypedDict):
    path: str
    surface: Surface 

class FontResource(TypedDict):
    path: str
    font: Font

class SpriteSheetResource(TypedDict):
    path: str
    spritesheet: SpriteSheet

class SoundResource(TypedDict):
    path: str
    sound: Sound



