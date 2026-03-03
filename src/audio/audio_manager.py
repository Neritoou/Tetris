import pygame
from typing import Dict, TYPE_CHECKING
from src.resources.types import AudioCategory

if TYPE_CHECKING:
    from src.resources import SoundResource

class AudioManager:
    """Gestor global de audio, maneja reproducción y control."""
    
    def __init__(self, frequency: int = 44100, size: int = -16, 
                 channels: int = 2, buffer: int = 512):
        """
        Inicializa el gestor de audio.
        
        Args:
            frequency: Frecuencia de muestreo (Hz)
            size: Tamaño de muestra (-16 = 16-bit signed)
            channels: Canales de audio (1=mono, 2=stereo)
            buffer: Tamaño del buffer
        """
        # Inicializar mixer con configuración personalizada
        pygame.mixer.quit()  # Por si ya estaba inicializado
        pygame.mixer.init(frequency=frequency, size=size, channels=channels, buffer=buffer)
        
        # Estado de música
        self._current_music: str = ""
        self._music_paused: bool = False
        
        # Volúmenes por categoría (0.0 a 1.0)
        self._volumes: Dict[AudioCategory, float] = {
            AudioCategory.MUSIC: 0.7,
            AudioCategory.SFX: 0.8,
        }
        
        # Master volume
        self._master_volume: float = 1.0
        
        # Configuración de canales
        self._max_sound_channels = 16
        pygame.mixer.set_num_channels(self._max_sound_channels)

        self._sound_categories: dict[AudioCategory, dict[str, pygame.mixer.Sound]] = {}

    # MÚSICA (Background Music)
    def play_music(self, music_file: str, loops: int = -1, 
                   start: float = 0.0, fade_ms: int = 0) -> None:
        """
        Reproduce música desde un archivo.
        
        Args:
            music_file: Path al archivo de música (ya resuelto por ResourceManager)
            loops: Número de repeticiones (-1 = infinito)
            start: Tiempo de inicio en segundos
            fade_ms: Tiempo de fade-in en milisegundos
            identifier: Identificador opcional para trackear la música
            
        Returns:
            True si comenzó a reproducir
        """
        try:
            if self._current_music != music_file:
                pygame.mixer.music.load(music_file)
                self._current_music = music_file

            pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
            self._music_paused = False
            self._apply_music_volume()
            
        except pygame.error as e:
            self._current_music = ""
            print(f"Audio Manager: Error reproduciendo música, {e}")

    
    def stop_music(self, fade_ms: int = 0) -> None:
        """
        Detiene la música.
        
        Args:
            fade_ms: Tiempo de fade-out en milisegundos
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        
        self._music_paused = False
    
    def pause_music(self) -> None:
        """Pausa la música."""
        if self.is_music_playing() and not self._music_paused:
            pygame.mixer.music.pause()
            self._music_paused = True
    
    def unpause_music(self) -> None:
        """Reanuda la música."""
        if self._music_paused:
            pygame.mixer.music.unpause()
            self._music_paused = False
    
    def rewind_music(self) -> None:
        """Reinicia la música desde el principio."""
        pygame.mixer.music.rewind()
    
    def set_music_position(self, position: float) -> None:
        """
        Establece la posición de reproducción de la música en segundos.
        
        Note:
            Solo funciona con archivos MP3, OGG, MOD
        """
        try:
            pygame.mixer.music.set_pos(position)
        except pygame.error as e:
            print(f"Audio Manager: No se pudo mover la posición: {e}")
    
    def get_music_position(self) -> float:
        """Obtiene la posición actual en milisegundos."""
        return pygame.mixer.music.get_pos()
    
    def is_music_playing(self) -> bool:
        """Verifica si la música está reproduciéndose."""
        return pygame.mixer.music.get_busy()
    
    def is_music_paused(self) -> bool:
        """Verifica si la música está pausada."""
        return self._music_paused
    
    def get_current_music(self) -> str | None:
        """Obtiene el path de la música actual."""
        return self._current_music
    
    # EFECTOS DE SONIDO
    def register_sounds(self, sounds: "dict[AudioCategory, dict[str, SoundResource]]") -> None:
        """Registra todos los sonidos previamente cargados."""
        for category, sounds_dict in sounds.items():
            for key, resource in sounds_dict.items():
                self.register_sound(key, resource["sound"], category)

    def register_sound(self, key: str, sound: pygame.mixer.Sound, category: AudioCategory) -> None:
        """Registra un nuevo sonido después de la inicialización."""
        if category not in self._sound_categories:
            # Si la categoría no está, se agrega
            self._sound_categories[category] = {}

        # Solo registrar si el sonido no está ya registrado
        if key not in self._sound_categories[category]:
            self._sound_categories[category][key] = sound
            # Ajuste de volumen al registrar
            sound.set_volume(self._get_effective_volume(category))

    def unregister_sound(self, key: str, category: AudioCategory) -> None:
        """Elimina un sonido del registro de AudioManager."""
        if category not in self._sound_categories:
            raise ValueError(f"AudioManager: la categoria '{category}' no está registrada.")
        
        if key not in self._sound_categories[category]:
            raise KeyError(f"AudioManager: el sonido '{key}' no está registrado en la categoría '{category}'.")

        self._sound_categories[category].pop(key)

    def play_sound(self, key: str, category: AudioCategory,
                   loops: int = 0, maxtime: int = 0, 
                   fade_ms: int = 0) -> pygame.mixer.Channel | None:
        """
        Reproduce un efecto de sonido.
        
        Args:
            sound: Objeto Sound (ya cargado por ResourceManager)
            category: Categoría del sonido (para control de volumen)
            loops: Número de repeticiones (0 = una vez)
            maxtime: Tiempo máximo en ms
            fade_ms: Tiempo de fade-in en ms
            
        Returns:
            Canal donde se está reproduciendo o None
        """
        try:
            return self._sound_categories[category][key].play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        except pygame.error as e:
            print(f"AudioManager: Error reproduciendo sonido: {e}")
            return None

    def play_sfx(self, key: str) -> None:
        self.play_sound(key, AudioCategory.SFX)

    def play_voice(self, key: str) -> None:
        self.play_sound(key, AudioCategory.VOICE)
    
    def stop_sound(self, sound: pygame.mixer.Sound) -> None:
        """Detiene todas las instancias de un sonido."""
        sound.stop()
    
    def stop_all_sounds(self) -> None:
        """Detiene todos los efectos de sonido."""
        pygame.mixer.stop()

    def stop_category(self, category: AudioCategory) -> None:
        """Detiene todos los sonidos de una categoría específica."""
        for sound in self._sound_categories.get(category, {}).values():
            sound.stop()

    
    def fadeout_sound(self, sound: pygame.mixer.Sound, fade_ms: int) -> None:
        """
        Hace fade-out de un sonido.
    
        Args:
            sound: Sonido a hacer fadeout
            fade_ms: Duración del fade en milisegundos
        """
        sound.fadeout(fade_ms)
    
    # VOLUMEN
    def set_master_volume(self, volume: float) -> None:
        """
        Establece el volumen master (afecta todo).
        
        Args:
            volume: Volumen de 0.0 a 1.0
        """
        self._master_volume = max(0.0, min(1.0, volume))
        
        # Re-aplicar volúmenes
        self._apply_music_volume()
        self._update_all_sounds_volume()
    
    def get_master_volume(self) -> float:
        """Obtiene el volumen master."""
        return self._master_volume
    
    def set_category_volume(self, category: AudioCategory, volume: float) -> None:
        """
        Establece el volumen de una categoría.
        
        Args:
            category: Categoría de audio
            volume: Volumen de 0.0 a 1.0
        """
        self._volumes[category] = max(0.0, min(1.0, volume))
        
        # Re-aplicar según categoría
        if category == AudioCategory.MUSIC:
            self._apply_music_volume()
        else:
            self._update_sounds_by_category(category)
    
    def get_category_volume(self, category: AudioCategory) -> float:
        """Obtiene el volumen de una categoría."""
        return self._volumes[category]
    
    def _get_effective_volume(self, category: AudioCategory) -> float:
        """Calcula el volumen efectivo (categoría * master)."""
        return self._volumes[category] * self._master_volume
    
    def _apply_music_volume(self) -> None:
        """Aplica el volumen actual a la música."""
        volume = self._get_effective_volume(AudioCategory.MUSIC)
        pygame.mixer.music.set_volume(volume)
    
    def _update_all_sounds_volume(self) -> None:
        """Actualiza el volumen de todos los sonidos registrados."""
        for category, sounds in self._sound_categories.items():
            volume = self._get_effective_volume(category)
            for sound in sounds.values():
                sound.set_volume(volume)
    
    def _update_sounds_by_category(self, category: AudioCategory) -> None:
        """Actualiza el volumen de sonidos de una categoría específica."""
        volume = self._get_effective_volume(category)
        for sound in self._sound_categories[category].values():
            sound.set_volume(volume)

    

    # --- HELPERS ---
    def get_num_channels(self) -> int:
        """Obtiene el número de canales de audio disponibles."""
        return pygame.mixer.get_num_channels()
    
    def get_busy_channels(self) -> int:
        """Obtiene el número de canales ocupados."""
        return len([c for c in range(pygame.mixer.get_num_channels()) 
                   if pygame.mixer.Channel(c).get_busy()])
    
    def get_available_channels(self) -> int:
        """Obtiene el número de canales libres."""
        return self.get_num_channels() - self.get_busy_channels()
    
    def set_num_channels(self, count: int) -> None:
        """Establece el número de canales de audio."""
        self._max_sound_channels = count
        pygame.mixer.set_num_channels(count)
    
    def get_sound_length(self, sound: pygame.mixer.Sound) -> float:
        """Obtiene la duración de un sonido en segundos."""
        return sound.get_length()
    
    def get_music_length(self) -> float:
        """Obtiene la duración de una musica en segundos"""
        try:
            sound = pygame.mixer.Sound(self._current_music)
            return sound.get_length()
        except Exception as e:
            print(f"Audio Manager: Error obteniendo duración: {e}")
            raise RuntimeError("AudioManager: No se pudo obtener la duración de la música.")

    def get_info(self) -> dict:
        """Obtiene información del sistema de audio."""
        init_info = pygame.mixer.get_init()
        
        return {
            "frequency": init_info[0] if init_info else 0,
            "format": init_info[1] if init_info else 0,
            "channels": init_info[2] if init_info else 0,
            "num_channels": self.get_num_channels(),
            "busy_channels": self.get_busy_channels(),
            "available_channels": self.get_available_channels(),
            "music_playing": self.is_music_playing(),
            "music_paused": self.is_music_paused(),
            "current_music": self._current_music,
            "master_volume": self._master_volume,
            "volumes": {cat.value: vol for cat, vol in self._volumes.items()}
        }
    
    def shutdown(self) -> None:
        """Limpia y cierra el sistema de audio."""
        self.stop_music()
        self.stop_all_sounds()
        self._sound_categories.clear()
        pygame.mixer.quit()