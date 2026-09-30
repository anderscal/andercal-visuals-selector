"""
src/core/validator.py
Módulo encargado de validar la integridad de la selección, detectar archivos faltantes,
ambigüedades (colisiones de nombres) y determinar si la operación es segura.
"""

from pathlib import Path
from typing import Dict, List, Any, Union
from src.core.parser import extract_photo_codes
from src.core.scanner import find_matches_for_codes


def validate_photo_selection(
    directory_path: Union[str, Path],
    raw_text: str,
    selected_extensions: List[str]
) -> Dict[str, Any]:
    """
    Realiza una validación completa de la selección ingresada por el usuario.

    :param directory_path: Carpeta de trabajo.
    :param raw_text: Texto con los nombres o códigos pegados.
    :param selected_extensions: Extensiones activas (ej: ['CR3', 'XMP']).
    :return: Diccionario detallado de diagnóstico:
             {
               'unique_codes': ['7644', '8009'],
               'total_codes': 2,
               'selected_extensions': ['CR3', 'XMP'],
               'found_counts': {'CR3': 2, 'XMP': 1},
               'missing_counts': {'CR3': 0, 'XMP': 1},
               'missing_details': {'8009': ['XMP']},
               'ambiguous_details': {},
               'files_to_process': [Path('_MG_7644.CR3'), Path('_MG_7644.xmp'), Path('IMG_8009.CR3')],
               'is_valid_for_operation': False
             }
    """
    unique_codes = extract_photo_codes(raw_text)
    norm_exts = [ext.strip().lstrip(".").upper() for ext in selected_extensions]

    if not unique_codes or not norm_exts:
        return {
            "unique_codes": [],
            "total_codes": 0,
            "selected_extensions": norm_exts,
            "found_counts": {ext: 0 for ext in norm_exts},
            "missing_counts": {ext: 0 for ext in norm_exts},
            "missing_details": {},
            "ambiguous_details": {},
            "files_to_process": [],
            "is_valid_for_operation": False,
        }

    matches = find_matches_for_codes(directory_path, unique_codes, norm_exts)

    found_counts = {ext: 0 for ext in norm_exts}
    missing_counts = {ext: 0 for ext in norm_exts}
    missing_details: Dict[str, List[str]] = {}
    ambiguous_details: Dict[str, Dict[str, List[Path]]] = {}
    files_to_process: List[Path] = []

    for code in unique_codes:
        code_matches = matches.get(code, {})
        for ext in norm_exts:
            found_paths = code_matches.get(ext, [])
            count = len(found_paths)

            if count == 1:
                found_counts[ext] += 1
                files_to_process.append(found_paths[0])
            elif count == 0:
                missing_counts[ext] += 1
                if code not in missing_details:
                    missing_details[code] = []
                missing_details[code].append(ext)
            else:
                # Ambigüedad / Colisión: Múltiples archivos para la misma extensión y código
                found_counts[ext] += count
                files_to_process.extend(found_paths)
                if code not in ambiguous_details:
                    ambiguous_details[code] = {}
                ambiguous_details[code][ext] = found_paths

    # La operación es válida si NO hay archivos faltantes ni ambigüedades
    is_valid = (len(missing_details) == 0) and (len(ambiguous_details) == 0)

    return {
        "unique_codes": unique_codes,
        "total_codes": len(unique_codes),
        "selected_extensions": norm_exts,
        "found_counts": found_counts,
        "missing_counts": missing_counts,
        "missing_details": missing_details,
        "ambiguous_details": ambiguous_details,
        "files_to_process": files_to_process,
        "is_valid_for_operation": is_valid,
    }
