from typing import TYPE_CHECKING
from src.util import get_asset

if TYPE_CHECKING:
        from src.resources.resource_manager import ResourceManager

def _load_music_paths(rm: "ResourceManager"):
        rm.load_music_path("TitleMusic", str(get_asset("sounds", "title_music.ogg")))
        rm.load_music_path("GameplayMusic", str(get_asset("sounds", "gameplay_music.ogg")))
        rm.load_music_path("HighScore", str(get_asset("sounds", "high_score.ogg")))