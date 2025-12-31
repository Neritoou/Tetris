import pygame
from typing import Dict, Tuple, TypeVar, TYPE_CHECKING
from .spritesheet import SpriteSheet
from .piece_library import PieceLibrary
from .loaders import *
from .types import *

if TYPE_CHECKING:
    import numpy as np
    from ..core import PieceSurfaces, PieceData

T = TypeVar("T")
K = TypeVar("K")

class ResourceManager:
    """Gestor de recursos del juego: imágenes, sonidos, fuentes, spritesheets y piezas."""


    def __init__(self):
        """Inicializa los contenedores de recursos vacíos."""
        self._images: dict[str, ImageResource] = {}
        self._fonts: dict[tuple[str,int], FontResource] = {}
        self._sounds: dict[str, SoundResource] = {}
        self._spritesheets: dict[str, SpriteSheetResource] = {}
        self._piece_library: PieceLibrary = PieceLibrary()

        self._loaded_paths: Dict[str, str] = {}



    # --- GETTERS ---
    def get_image(self, key: str) -> pygame.Surface:
        """Obtiene una imagen cargada."""
        resource = self._get_resource(self._images, key, "Image")
        return resource["surface"]

    def get_sound(self, key: str) -> pygame.mixer.Sound:
        """Obtiene un sonido cargado."""
        resource = self._get_resource(self._sounds, key, "Sound")
        return resource["sound"]

    def get_font(self, key: str, size: int) -> pygame.font.Font:
        """Obtiene una fuente cargada."""
        resource = self._get_resource(self._fonts, (key, size), "Font")
        return resource["font"]
    
    def get_spritesheet(self, key: str) -> SpriteSheet:
        """Obtiene una hoja de sprites cargada."""
        resource = self._get_resource(self._spritesheets, key, "SpriteSheet")
        return resource["spritesheet"]
    
    def get_piece(self, key: str) -> "PieceData":
        """Obtiene una pieza registrada en la biblioteca."""
        return self._piece_library.get_piece(key)



    # --- LOADERS ---
    def load_image(self, key: str, path: str) -> None:
        """Carga y almacena una imagen."""
        # Si el recurso ya existe, no se crea nuevamente
        if key in self._images:
            if self._images[key]["path"] == path:
                print(" YA SE CARGÓ")
                return
            raise ValueError(f"Resource Manager: Image '{key}' ya tiene asociado un path distinto: '{self._images[key]['path']}'")
        
        self._assert_path_unused(path)
        img = pygame.image.load(path)
        self._images[key] = {"path": path, "surface": img.convert_alpha() if img.get_alpha() else img.convert()}
        self._loaded_paths[path] = key
        
    def load_sound(self, key: str, path: str) -> None:
        """Carga y almacena un sonido."""
        # Si el recurso ya existe, no se crea nuevamente
        if key in self._sounds:
            if self._sounds[key]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Sound '{key}' ya tiene asociado un path distinto: '{self._sounds[key]['path']}'")
        
        self._assert_path_unused(path)
        self._sounds[key] = {"path": path, "sound": pygame.mixer.Sound(path)}
        self._loaded_paths[path] = key

    def load_font(self, key: str, path: str, size: int) -> None:
        """Carga y almacena una fuente."""
        # Si el recurso ya existe, no se crea nuevamente
        if (key,size) in self._fonts:
            if self._fonts[(key,size)]["path"] == path:
                return
            raise ValueError(f"Resource Manager: Font '{key}' ya tiene asociado un path distinto: '{self._fonts[(key,size)]['path']}'")
        
        self._assert_path_unused(path)   
        self._fonts[(key,size)] = {"path": path, "font": pygame.font.Font(path, size)}
        self._loaded_paths[path] = key

    def load_spritesheet(self, key: str, path: str, frame_size: Tuple[int,int], padding: Tuple[int,int] = (0,0)) -> None:
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

    def load_piece(self, key: str, base_matrix: "np.ndarray", blocks: "PieceSurfaces") -> None:
        """Registra una pieza en la biblioteca interna."""
        self._piece_library.register_piece(key, base_matrix,blocks)



    # --- UNLOADERS ---
    def unload_image(self, key: str) -> None:
        """Elimina una imagen del Diccionario"""
        if key not in self._images:
            return
        self._loaded_paths.pop(self._images[key]["path"], None)
        self._images.pop(key)

    def unload_sound(self, key: str) -> None:
        """Elimina un sonido del Diccionario"""
        if key not in self._sounds:
            return
        self._loaded_paths.pop(self._sounds[key]["path"], None)
        self._sounds.pop(key)

    def unload_font(self, key: str, size: int) -> None:
        """Elimina una fuente del Diccionario"""
        if (key,size) not in self._fonts:
            return
        self._loaded_paths.pop(self._fonts[(key,size)]["path"], None)
        self._fonts.pop((key,size))

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
        _load_pieces(self)



    # --- HELPERS ---
    def _get_resource(self, container: Dict[K, T], key: K, resource_type: str) -> T:
        """Obtiene un recurso de un diccionario, lanzando KeyError si no existe."""
        if key not in container:
            raise KeyError(f"Resource Manager: {resource_type} '{key}' no está cargado")
        return container[key]
    
    def _assert_path_unused(self, path: str) -> None:
        if path in self._loaded_paths:
            raise ValueError(f"Resource Manager: El path '{path}' ya está asociado a la key '{self._loaded_paths[path]}'")
