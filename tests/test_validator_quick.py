"""
tests/test_validator_quick.py
Script de prueba rápida para verificar el validador (src/core/validator.py).
"""

import sys
import tempfile
from pathlib import Path

# Añadir la raíz del proyecto al PATH de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.validator import validate_photo_selection


def run_validator_tests():
    print("=" * 60)
    print("  PRUEBA DEL VALIDADOR DE DIAGNÓSTICO (src/core/validator.py)")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)

        # Crear archivos para Caso 1 (Todo completo)
        (folder / "_MG_7644.CR3").write_text("dummy")
        (folder / "_MG_7644.xmp").write_text("dummy")
        (folder / "IMG_8009.CR3").write_text("dummy")

        raw_text_1 = "_MG_7644.jpg\nIMG_8009.jpg"
        exts_1 = ["CR3", "XMP"]

        # Escenario 1: Falta XMP de 8009
        report_1 = validate_photo_selection(folder, raw_text_1, exts_1)
        print(f"\nEscenario 1 (Falta XMP de 8009):\n  Válido 100% perfecto: {report_1['is_valid_for_operation']}\n  Procesable por el usuario: {report_1['can_process']}")
        print(f"  Faltantes: {report_1['missing_details']}")
        assert report_1["is_valid_for_operation"] is False
        assert report_1["can_process"] is True
        assert report_1["missing_details"] == {"8009": ["XMP"]}, "Detalle de faltantes incorrecto"


        # Crear XMP faltante para Escenario 2 (Todo completo)
        (folder / "IMG_8009.xmp").write_text("dummy")
        report_2 = validate_photo_selection(folder, raw_text_1, exts_1)
        print(f"\nEscenario 2 (Todo completo):\n  Válido para operar: {report_2['is_valid_for_operation']}")
        print(f"  Archivos a procesar: {[f.name for f in report_2['files_to_process']]}")
        assert report_2["is_valid_for_operation"] is True, "Debe ser verdadero cuando todo coincide"
        assert len(report_2["files_to_process"]) == 4, "Deben procesarse 4 archivos (2 RAW + 2 XMP)"

    print("\n" + "=" * 60)
    print("  ¡TODAS LAS PRUEBAS DEL VALIDADOR PASARON CORRECTAMENTE!  ")
    print("=" * 60)


if __name__ == "__main__":
    run_validator_tests()
