"""
tests/test_scanner_quick.py
Script de prueba rápida para verificar el escáner de carpetas (src/core/scanner.py).
"""

import sys
import tempfile
from pathlib import Path

# Añadir la raíz del proyecto al PATH de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.scanner import find_matches_for_codes


def run_scanner_tests():
    print("=" * 60)
    print("  PRUEBA DEL ESCÁNER DE ARCHIVOS (src/core/scanner.py)")
    print("=" * 60)

    # Crear una carpeta temporal aislada para la prueba
    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)

        # Crear archivos simulados de prueba
        (folder / "_MG_7644.CR3").write_text("dummy content")
        (folder / "_MG_7644.xmp").write_text("dummy content")          # XMP simple
        (folder / "IMG_8009.CR3").write_text("dummy content")
        (folder / "IMG_8009.CR3.xmp").write_text("dummy content")      # XMP doble

        codes = ["7644", "8009"]
        exts = ["CR3", "XMP"]

        results = find_matches_for_codes(folder, codes, exts)

        print(f"\nResultados encontrados en la carpeta temporal:\n")
        for code, ext_map in results.items():
            print(f"  Código [{code}]:")
            for ext, files in ext_map.items():
                filenames = [f.name for f in files]
                print(f"    - Extension {ext}: {filenames}")

        # Verificaciones (Assertions)
        assert len(results["7644"]["CR3"]) == 1, "Fallo al encontrar _MG_7644.CR3"
        assert len(results["7644"]["XMP"]) == 1, "Fallo al encontrar _MG_7644.xmp (simple)"
        assert len(results["8009"]["CR3"]) == 1, "Fallo al encontrar IMG_8009.CR3"
        assert len(results["8009"]["XMP"]) == 1, "Fallo al encontrar IMG_8009.CR3.xmp (doble)"

    print("\n" + "=" * 60)
    print("  ¡TODAS LAS PRUEBAS DEL ESCÁNER PASARON CORRECTAMENTE!  ")
    print("=" * 60)


if __name__ == "__main__":
    run_scanner_tests()
