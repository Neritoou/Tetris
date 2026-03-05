from typing import TYPE_CHECKING
from src.util import get_asset

if TYPE_CHECKING:
    from src.resources.resource_manager import ResourceManager

def _load_images(rm: "ResourceManager") -> None:
        # BOARD BASE
        rm.load_image("Title", str(get_asset("images", "tetris_title.png")))
        rm.load_image("Background", str(get_asset("images", "background.png")))

        rm.load_image("Board", str(get_asset("images", "board.png")))
        rm.load_image("MenuArrows", str(get_asset("images", "menu_arrows.png")))

        rm.load_image("RulesetNormalBtn", str(get_asset("images", "ruleset_normal_btn.png")))
        rm.load_image("RulesetSelBtn", str(get_asset("images", "ruleset_sel_btn.png")))

        rm.load_image("ControlsNormalBtn", str(get_asset("images", "controls_normal_btn.png")))
        rm.load_image("ControlsSelBtn", str(get_asset("images", "controls_sel_btn.png")))