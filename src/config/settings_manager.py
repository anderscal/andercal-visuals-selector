"""
src/config/settings_manager.py
Módulo responsable de la persistencia local de configuraciones (settings.json)
y catálogo de formatos de archivos fotográficos (formats.json).
"""

import json
from pathlib import Path
from typing import Dict, List, Any

# Rutas de los archivos de configuración
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
FORMATS_FILE = CONFIG_DIR / "formats.json"

DEFAULT_SETTINGS = {
    "last_directory": "",
    "selected_extensions": ["CR3", "XMP"],
    "default_action": "copy"
}

DEFAULT_FORMATS = {
    "available_formats": [
        "CR3", "CR2", "NEF", "ARW", "RAF", "DNG",
        "ORF", "RW2", "PEF", "SRW", "RAW", "XMP", "JPG", "JPEG"
    ]
}


def _ensure_config_dir_exists():
    """Crea la carpeta /config si no existe."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_settings() -> Dict[str, Any]:
    """
    Carga las preferencias del usuario desde settings.json.
    Si el archivo no existe o se corrompe, retorna los valores por defecto.
    """
    _ensure_config_dir_exists()
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Combinar con valores por defecto por si falta alguna clave
            settings = DEFAULT_SETTINGS.copy()
            settings.update(data)
            return settings
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Guarda las preferencias del usuario en settings.json.
    """
    _ensure_config_dir_exists()
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def load_formats() -> List[str]:
    """
    Carga la lista de formatos disponibles desde formats.json.
    """
    _ensure_config_dir_exists()
    if not FORMATS_FILE.exists():
        save_formats(DEFAULT_FORMATS["available_formats"])
        return DEFAULT_FORMATS["available_formats"].copy()

    try:
        with open(FORMATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("available_formats", DEFAULT_FORMATS["available_formats"].copy())
    except Exception:
        return DEFAULT_FORMATS["available_formats"].copy()


def save_formats(formats_list: List[str]) -> bool:
    """
    Guarda la lista de formatos disponibles en formats.json.
    """
    _ensure_config_dir_exists()
    try:
        # Normalizar a mayúsculas sin duplicados manteniendo el orden
        clean_formats = []
        seen = set()
        for fmt in formats_list:
            fmt_clean = fmt.strip().lstrip(".").upper()
            if fmt_clean and fmt_clean not in seen:
                seen.add(fmt_clean)
                clean_formats.append(fmt_clean)

        data = {"available_formats": clean_formats}
        with open(FORMATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def add_custom_format(new_format: str) -> List[str]:
    """
    Añade un nuevo formato personalizado (ej: 'PSD') a formats.json.
    """
    formats = load_formats()
    clean_fmt = new_format.strip().lstrip(".").upper()
    if clean_fmt and clean_fmt not in formats:
        formats.append(clean_fmt)
        save_formats(formats)
    return formats
