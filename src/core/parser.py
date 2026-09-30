"""
src/core/parser.py
Módulo encargado de la extracción y normalización de códigos numéricos de fotografía.
"""

import re
from typing import List


def extract_photo_codes(raw_text: str) -> List[str]:
    """
    Extrae códigos de 4 dígitos numéricos desde cualquier texto sucio,
    eliminando duplicados y manteniendo el orden de aparición.

    Ejemplos de entradas soportadas:
      - "_MG_7644.jpg  Destacados  9/28/2026"  -> ['7644']
      - "IMG_8009.CR3\nDSC_8010.NEF"            -> ['8009', '8010']
      - "7644, 7647, 7654"                       -> ['7644', '7647', '7654']

    :param raw_text: Cadena de texto de entrada con nombres, tablas o números.
    :return: Lista de cadenas de 4 dígitos únicos.
    """
    if not raw_text or not isinstance(raw_text, str):
        return []

    # 1. Limpiar patrones de fechas (ej: 9/28/2026, 2026-09-28, 28.09.2026) para no confundir años con códigos
    date_pattern = r"\b\d{1,4}[/.-]\d{1,2}[/.-]\d{1,4}\b"
    text_cleaned = re.sub(date_pattern, " ", raw_text)

    # 2. Expresión regular: busca exactamente 4 dígitos rodeados por caracteres no numéricos
    pattern = r"(?<!\d)\d{4}(?!\d)"
    matches = re.findall(pattern, text_cleaned)

    # 3. Eliminar duplicados conservando el orden de aparición
    seen = set()
    unique_codes = []
    for code in matches:
        if code not in seen:
            seen.add(code)
            unique_codes.append(code)

    return unique_codes

