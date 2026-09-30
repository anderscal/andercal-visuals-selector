"""
tests/test_settings_quick.py
Script de prueba rápida para el gestor de configuración (src/config/settings_manager.py).
"""

import sys
from pathlib import Path

# Añadir la raíz del proyecto al PATH de Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config.settings_manager import (
    load_settings,
    save_settings,
    load_formats,
    add_custom_format
)


def run_settings_tests():
    print("=" * 60)
    print("  PRUEBA DEL GESTOR DE CONFIGURACIÓN (src/config/settings_manager.py)")
    print("=" * 60)

    # 1. Probar carga de configuraciones por defecto
    settings = load_settings()
    print(f"\nConfiguración actual cargada:\n  {settings}")
    assert "last_directory" in settings
    assert "selected_extensions" in settings

    # 2. Probar guardado de preferencias
    test_path = r"C:\Fotografia\Boda_Prueba"
    settings["last_directory"] = test_path
    settings["selected_extensions"] = ["CR3", "XMP", "NEF"]
    save_success = save_settings(settings)
    assert save_success is True

    # Recargar y verificar persistencia
    reloaded_settings = load_settings()
    print(f"\nConfiguración guardada y recargada:\n  {reloaded_settings}")
    assert reloaded_settings["last_directory"] == test_path
    assert "NEF" in reloaded_settings["selected_extensions"]

    # 3. Probar catálogo de formatos y adición de formato personalizado
    formats = load_formats()
    print(f"\nCatálogo de formatos cargado ({len(formats)} formatos):\n  {formats[:5]}...")

    updated_formats = add_custom_format("psd")
    print(f"\nFormato personalizado 'PSD' añadido:\n  Último formato: {updated_formats[-1]}")
    assert "PSD" in updated_formats

    print("\n" + "=" * 60)
    print("  ¡TODAS LAS PRUEBAS DE CONFIGURACIÓN PASARON CORRECTAMENTE!  ")
    print("=" * 60)


if __name__ == "__main__":
    run_settings_tests()
