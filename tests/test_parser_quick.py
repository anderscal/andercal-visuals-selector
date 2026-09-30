"""
tests/test_parser_quick.py
Script de verificación rápida para probar la extracción de códigos en src/core/parser.py
"""

import sys
from pathlib import Path

# Añadir la raíz del proyecto al PATH de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.parser import extract_photo_codes

def run_tests():
    print("=" * 60)
    print("  PRUEBA DE EXTRACCIÓN DE CÓDIGOS (src/core/parser.py)")
    print("=" * 60)

    # Caso 1: Nombres de archivo estándar Canon/Nikon/Sony
    texto_1 = "_MG_7644.jpg\n_MG_7647.jpg\n_MG_7654.jpg"
    resultado_1 = extract_photo_codes(texto_1)
    print(f"\nCaso 1 (Nombres estándar):\n  Entrada: {texto_1!r}\n  Extraídos: {resultado_1}")
    assert resultado_1 == ['7644', '7647', '7654'], "Error en Caso 1"

    # Caso 2: Copiado desde Excel con fechas, palabras y duplicados
    texto_2 = "_MG_7644.jpg\tDestacados\t9/28/2026\n_MG_7644.jpg\tDestacados\t9/28/2026\n_MG_8009.CR3"
    resultado_2 = extract_photo_codes(texto_2)
    print(f"\nCaso 2 (Excel sucio + duplicados):\n  Extraídos: {resultado_2}")
    assert resultado_2 == ['7644', '8009'], "Error en Caso 2"

    # Caso 3: Números sueltos o separados por comas
    texto_3 = "7644, 7647, 7654, 8109"
    resultado_3 = extract_photo_codes(texto_3)
    print(f"\nCaso 3 (Números sueltos):\n  Extraídos: {resultado_3}")
    assert resultado_3 == ['7644', '7647', '7654', '8109'], "Error en Caso 3"

    print("\n" + "=" * 60)
    print("  ¡TODAS LAS PRUEBAS DEL PARSER PASARON CORRECTAMENTE!  ")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
