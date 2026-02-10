import sys
from pathlib import Path

# Función para obtener la ruta base del proyecto dependiendo si es un ejecutable o desarrollo
def get_base_path() -> Path:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return Path(base_path)
    
    # game/src/util/paths.py ->  game/
    return Path(__file__).resolve().parents[2]

# Ruta base del proyecto
BASE_PATH = get_base_path()

# Ruta a los assets
ASSETS_ROOT = BASE_PATH / "assets"

def get_asset(*paths: str) -> Path:
    """
    Devuelve la ruta absoluta de un asset como un objeto Path.

    Si una API requiere un string (por ejemplo, pygame), 
    se puede convertir usando str(path).

    Returns:
        Path: Ruta absoluta al asset solicitado.
    """
    path = ASSETS_ROOT.joinpath(*paths)

    if not path.is_file():
        raise FileNotFoundError(f"Paths: Asset {paths[-1]} no encontrado o inválido en la Ruta:\n{path}")
    return path