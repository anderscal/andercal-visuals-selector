"""
src/core/parser.py -> src/core/scanner.py
Módulo encargado de escanear directorios y mapear archivos fotográficos (RAW y XMP)
asociados a códigos numéricos mediante pathlib.
"""

from pathlib import Path
from typing import Dict, List, Union
from src.core.parser import extract_photo_codes


def scan_directory(
    directory_path: Union[str, Path], selected_extensions: List[str]
) -> Dict[str, List[Path]]:
    """
    Escanea la carpeta indicada y clasifica los archivos existentes
    según las extensiones seleccionadas (insensible a mayúsculas/minúsculas).

    :param directory_path: Ruta del directorio a escanear.
    :param selected_extensions: Lista de extensiones (ej. ['CR3', 'XMP']).
    :return: Diccionario { 'CR3': [Path, Path], 'XMP': [Path] }
    """
    folder = Path(directory_path)
    if not folder.is_dir():
        return {}

    # Normalizar extensiones en mayúsculas sin punto
    target_exts = {ext.strip().lstrip(".").upper() for ext in selected_extensions}

    result: Dict[str, List[Path]] = {ext: [] for ext in target_exts}

    for item in folder.iterdir():
        if item.is_file():
            # Manejo especial para sidecars dobles (ej: _MG_8009.CR3.xmp)
            name_lower = item.name.lower()

            for ext in target_exts:
                ext_lower = f".{ext.lower()}"
                if name_lower.endswith(ext_lower):
                    result[ext].append(item)

    return result


def find_matches_for_codes(
    directory_path: Union[str, Path],
    codes: List[str],
    selected_extensions: List[str]
) -> Dict[str, Dict[str, List[Path]]]:
    """
    Asocia cada código de 4 dígitos con sus archivos físicos encontrados en disco
    para cada extensión seleccionada.

    Maneja tanto sidecars simples (_MG_8009.xmp) como dobles (_MG_8009.CR3.xmp).

    :param directory_path: Carpeta de origen.
    :param codes: Lista de códigos extraídos (ej. ['7644', '8009']).
    :param selected_extensions: Extensiones activas (ej. ['CR3', 'XMP']).
    :return: Diccionario estructurado por código:
             {
               '8009': {
                 'CR3': [Path('_MG_8009.CR3')],
                 'XMP': [Path('_MG_8009.xmp')]
               }
             }
    """
    scanned_files = scan_directory(directory_path, selected_extensions)
    matches: Dict[str, Dict[str, List[Path]]] = {}

    for code in codes:
        matches[code] = {}
        for ext in selected_extensions:
            ext_upper = ext.strip().lstrip(".").upper()
            matches[code][ext_upper] = []

            # Filtrar los archivos escaneados que contengan el código de 4 dígitos
            candidates = scanned_files.get(ext_upper, [])
            for file_path in candidates:
                # Extraer códigos del nombre del archivo para confirmar la coincidencia exacta
                file_codes = extract_photo_codes(file_path.name)
                if code in file_codes:
                    matches[code][ext_upper].append(file_path)

    return matches
