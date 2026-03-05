from typing import TYPE_CHECKING
from src.util import get_asset
from src.resources.types import AudioCategory

if TYPE_CHECKING:
        from src.resources.resource_manager import ResourceManager

def _load_sounds(rm: "ResourceManager"):
        # MENU SOUNDS
        rm.load_sound("Scroll", AudioCategory.SFX, str(get_asset("sounds", "change_option.ogg")))
        rm.load_sound("Select", AudioCategory.SFX, str(get_asset("sounds", "select.ogg")))

        # GAMEPLAY SOUNDS
        rm.load_sound("DeleteRow", AudioCategory.SFX, str(get_asset("sounds", "delete_row.ogg")))
        rm.load_sound("FourRows", AudioCategory.SFX, str(get_asset("sounds", "four_rows.ogg")))
        rm.load_sound("LockPiece", AudioCategory.SFX, str(get_asset("sounds", "lock_piece.ogg")))
        rm.load_sound("MovePiece", AudioCategory.SFX, str(get_asset("sounds", "move_piece.ogg")))
        rm.load_sound("RotatePiece", AudioCategory.SFX, str(get_asset("sounds", "rotate_piece.ogg")))
        rm.load_sound("GameOver", AudioCategory.SFX, str(get_asset("sounds", "game_over.ogg")))
        rm.load_sound("Countdown", AudioCategory.SFX, str(get_asset("sounds", "countdown.ogg")))