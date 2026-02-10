import pygame
from typing import TypeVar, TYPE_CHECKING
from .spritesheet import SpriteSheet
from .piece_library import PieceLibrary
from .loaders import *
from .types import *

if TYPE_CHECKING:
    import numpy as np
    from ..core import PieceSurfaces, PieceData
    from .types import AudioCategory

T = TypeVar("T")
K = TypeVar("K")

class ResourceManager:
    """Gestor de recursos del juego: imágenes, sonidos, fuentes, spritesheets y piezas."""
    def __init__(self):
        """Inicializa los contenedores de recursos vacíos."""
        self._images: dict[str, ImageResource] = {}
        self._fonts: dict[str, FontResource] = {}
        self._sounds: dict[AudioCategory, dict[str, SoundResource]] = {}
        self._musics: dict[str, MusicResource] = {}
        self._spritesheets: dict[str, SpriteSheetResource] = {}
        self._piece_library: PieceLibrary = PieceLibrary()

        self._loaded_paths: dict[str, str] = {}

       


    # --- GETTERS ---
    def get_image(self, key: str) -> pygame.Surface:
        """Obtiene una imagen cargada."""
        resource = self._get_resource(self._images, key, "Image")
        return resource["surface"]
    
    def get_images(self) -> dict[str, ImageResource]:
        return self._images

    def get_sound(self, key: str, category: AudioCategory) -> pygame.mixer.Sound:
        """Obtiene un sonido cargado."""
        resource = self._get_resource(self._sounds, category, "Sound")
        if key not in resource:
            raise ValueError(f"ResourceManager: sound {key} no está cargada en la categoria {category}")
        return resource[key]["sound"]

    def get_sounds(self) -> dict[AudioCategory, dict[str, SoundResource]]:
        return self._sounds

    def get_font(self, key: str, size: int) -> pygame.font.Font:
        """Obtiene una fuente cargada."""
        resource = self._get_resource(self._fonts, key, "Font")
        if size not in resource["font"]:
            raise ValueError(f"ResourceManager: font {key} de tamaño {size} no está cargada")
        return resource["font"][size]
    
    def get_fonts(self) -> dict[str, FontResource]:
        return self._fonts

    def get_spritesheet(self, key: str) -> SpriteSheet:
        """Obtiene una hoja de sprites cargada."""
        resource = self._get_resource(self._spritesheets, key, "SpriteSheet")
        return resource["spritesheet"]
    
    def get_spritesheets(self) -> dict[str, SpriteSheetResource]:
        return self._spritesheets
    
    def get_music_path(self, key: str) -> str:
        resource = self._get_resource(self._musics,key, "Music")
        return resource["path"]
    
    def get_music_paths(self) -> dict[str, MusicResource]:
        return self._musics
    
    def get_piece(self, key: str) -> "PieceData":
        """Obtiene una pieza registrada en la biblioteca."""
        return self._piece_library.get_piece(key)
    
    def get_pieces(self) -> "dict[str, PieceData]":
        return self._piece_library.pieces
    
    

   # --- LOADERS ---
    def load_image(self, key: str, path: str) -> None:
        """Carga y almacena una imagen."""
        # Si el recurso ya existe, no se crea nuevamente
        if key in self._images:
            if self._images[key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Image '{key}' ya tiene asociado un path distinto: '{self._images[key]['path']}'")
        self._assert_path_unused(path)
        img = pygame.image.load(path)
        self._images[key] = {"path": path, "surface": img.convert_alpha() if img.get_alpha() else img.convert()}
        self._loaded_paths[path] = key
        
    def load_sound(self, key: str, category: AudioCategory, path: str) -> None:
        """Carga y almacena un sonido."""
        # Si la categoria no se ha añadido, se añade
        if category not in self._sounds:
            self._sounds[category] = {}

        # Si el recurso ya existe, no se crea nuevamente
        if key in self._sounds[category]:
            if key in self._sounds[category][key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Sound '{category}' '{key}' ya tiene asociado un path distinto: '{self._sounds[category][key]['path']}'")
        
        self._assert_path_unused(path)
        self._sounds[category][key] = {"path": path, "sound": pygame.mixer.Sound(path)}
        self._loaded_paths[path] = key

    def load_music_path(self, key: str, path: str):
        if key in self._musics:
            if self._musics[key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Music '{key}' ya tiene asociado un path distinto: '{self._musics[key]['path']}'")
        self._assert_path_unused(path)
        self._musics[key] = {"path": path}
        self._loaded_paths[path] = key

    def load_font(self, key: str, path: str, sizes: set[int]) -> None:
        """
        Carga y almacena una fuente.

        Si ya existe un font con el mismo nombre (key) y tiene
        asociado el mismo path, se ignora (no lo carga).
        """
        if key in self._fonts:
            if self._fonts[key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Font '{key}' ya tiene asociado un path distinto: '{self._fonts[key]['path']}'")

        self._assert_path_unused(path)   
        self._fonts[key] = {"path": path, "font": {s: pygame.font.Font(path, s) for s in sizes}}
        self._loaded_paths[path] = key

    def load_spritesheet(self, key: str, path: str, frame_size: tuple[int,int], padding: tuple[int,int] = (0,0)) -> None:
        """Carga un spritesheet desde disco."""
        # Si el recurso ya existe, no se crea nuevamente
        if key in self._spritesheets:
            if self._spritesheets[key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: SpriteSheet '{key}' ya tiene asociado un path distinto: '{self._spritesheets[key]['path']}'")
        
        self._assert_path_unused(path)
        image = pygame.image.load(path).convert_alpha()
        self._spritesheets[key] = {"path": path, "spritesheet": SpriteSheet(image,frame_size,padding)}
        self._loaded_paths[path] = key

    def load_piece(self, key: str, base_matrix: "np.ndarray", blocks: "PieceSurfaces", type: int) -> None:
        """Registra una pieza en la biblioteca interna."""
        self._piece_library.register_piece(key, base_matrix,blocks,type)



     # --- UNLOADERS ---
    def unload_image(self, key: str) -> None:
        """Elimina una imagen del Diccionario"""
        if key not in self._images:
            return
        self._loaded_paths.pop(self._images[key]["path"], None)
        self._images.pop(key)

    def unload_sound(self, key: str, category: AudioCategory) -> None:
        """Elimina un sonido del Diccionario"""
        if category not in self._sounds:
            raise ValueError(f"ResourceManager: sound {key} no está cargada en la categoria {category}")

        if key not in self._sounds[category]:
            return
        self._loaded_paths.pop(self._sounds[category][key]["path"], None)
        self._sounds[category].pop(key)

    def unload_music_path(self, key: str) -> None:
        if key not in self._musics:
            return
        self._loaded_paths.pop(self._musics[key]["path"], None)
        self._musics.pop(key)

    def unload_font(self, key: str) -> None:
        """Elimina una fuente del Diccionario"""
        if key not in self._fonts:
            return
        self._loaded_paths.pop(self._fonts[key]["path"], None)
        self._fonts.pop(key)

    def unload_spritesheet(self, key: str) -> None:
        """Elimina una imagen del Diccionario"""
        if key not in self._spritesheets:
            return
        self._loaded_paths.pop(self._spritesheets[key]["path"], None)
        self._spritesheets.pop(key)
        

   
    # --- CARGA GLOBAL DE RECURSOS ---
    def load(self):
        """Carga todos los recursos y piezas del juego."""
        _load_spritesheets(self)
        _load_images(self)
        _load_fonts(self)
        _load_sounds(self)
        _load_music_paths(self)
        _load_pieces(self)



    # --- HELPERS ---
    def _get_resource(self, container: dict[K, T], key: K, resource_type: str) -> T:
        """Obtiene un recurso de un diccionario, lanzando KeyError si no existe."""
        if key not in container:
            raise KeyError(f"Resource Manager: {resource_type} '{key}' no está cargado")
        return container[key]
    
    def _assert_path_unused(self, path: str) -> None:
        if path in self._loaded_paths:
            raise ValueError(f"Resource Manager: El path '{path}' ya está asociado a la key '{self._loaded_paths[path]}'")