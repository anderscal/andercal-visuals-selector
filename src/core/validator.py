"""
src/core/validator.py
Módulo encargado de validar la integridad de la selección, detectar archivos faltantes,
ambigüedades (colisiones de nombres) y estructurar el reporte para decisión del usuario.
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
    :param selected_extensions: Extensiones activas (ej: ['CR3', 'XMP', 'ACR']).
    :return: Diccionario detallado de diagnóstico.
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
            "has_missing": False,
            "has_ambiguous": False,
            "is_valid_for_operation": False,
            "can_process": False
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

    has_missing = len(missing_details) > 0
    has_ambiguous = len(ambiguous_details) > 0

    # is_valid_for_operation: True si está 100% perfecto sin faltantes
    is_perfect = (not has_missing) and (not has_ambiguous)

    # can_process: True si hay al menos un archivo encontrado para procesar
    can_process = len(files_to_process) > 0

    return {
        "unique_codes": unique_codes,
        "total_codes": len(unique_codes),
        "selected_extensions": norm_exts,
        "found_counts": found_counts,
        "missing_counts": missing_counts,
        "missing_details": missing_details,
        "ambiguous_details": ambiguous_details,
        "files_to_process": files_to_process,
        "has_missing": has_missing,
        "has_ambiguous": has_ambiguous,
        "is_valid_for_operation": is_perfect,
        "can_process": can_process
    }
