"""
tests/test_mover_quick.py
Script de prueba rápida para el módulo gestor de archivos (src/core/mover.py).
"""

import sys
import tempfile
from pathlib import Path

# Añadir la raíz del proyecto al PATH de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.mover import process_files


def run_mover_tests():
    print("=" * 60)
    print("  PRUEBA DEL GESTOR DE ARCHIVOS (src/core/mover.py)")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)

        # Crear archivos de origen
        file_1 = folder / "_MG_7644.CR3"
        file_2 = folder / "_MG_7644.xmp"
        file_1.write_text("dummy CR3 content")
        file_2.write_text("dummy XMP content")

        files_to_process = [file_1, file_2]

        # PRUEBA 1: Copiar archivos a /Seleccionadas (validando creación automática de carpeta)
        res_copy = process_files(folder, files_to_process, action="copy")
        dest_dir = folder / "Seleccionadas"

        print(f"\nPrueba 1 (Copiar a /Seleccionadas):")
        print(f"  Éxito: {res_copy['success']}")
        print(f"  Carpeta destino creada: {dest_dir.is_dir()}")
        print(f"  Procesados: {res_copy['processed_count']} archivos")
        assert res_copy["success"] is True
        assert dest_dir.is_dir() is True
        assert file_1.exists() is True, "En modo copia, el original debe mantenerse"

        # PRUEBA 2: Copiar de nuevo para probar la protección anti-sobrescritura (nombres únicos)
        res_copy_2 = process_files(folder, [file_1], action="copy")
        safe_file = dest_dir / "_MG_7644_1.CR3"
        print(f"\nPrueba 2 (Protección Anti-Sobrescritura):")
        print(f"  Archivo duplicado renombrado a: {safe_file.name}")
        print(f"  Existe archivo seguro en destino: {safe_file.exists()}")
        assert safe_file.exists() is True, "Debe generar el sufijo _1 al haber duplicado"

        # PRUEBA 3: Mover archivos (los originales deben ser eliminados/trasladados de la raíz)
        res_move = process_files(folder, [file_2], action="move")
        print(f"\nPrueba 3 (Mover a /Seleccionadas):")
        print(f"  Éxito al mover: {res_move['success']}")
        print(f"  Original removido de raíz: {not file_2.exists()}")
        assert res_move["success"] is True
        assert not file_2.exists(), "En modo mover, el original debe desaparecer de raíz"

    print("\n" + "=" * 60)
    print("  ¡TODAS LAS PRUEBAS DEL GESTOR DE ARCHIVOS PASARON CORRECTAMENTE!  ")
    print("=" * 60)


if __name__ == "__main__":
    run_mover_tests()
