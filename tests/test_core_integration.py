"""
tests/test_core_integration.py
Suite unificada de pruebas de integración para el motor central de andercal.visuals — Selector.
Diseñado para ejecutarse automáticamente mediante pytest.
"""

import tempfile
from pathlib import Path

from src.core.parser import extract_photo_codes
from src.core.scanner import find_matches_for_codes
from src.core.validator import validate_photo_selection
from src.core.mover import process_files


def test_parser_extraction_and_date_filter():
    raw_text = "_MG_7644.jpg\tDestacados\t9/28/2026\n_MG_7644.jpg\n_MG_8009.CR3"
    codes = extract_photo_codes(raw_text)
    assert codes == ["7644", "8009"]


def test_scanner_sidecars_simple_and_double():
    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)
        (folder / "_MG_7644.CR3").write_text("data")
        (folder / "_MG_7644.xmp").write_text("data")
        (folder / "IMG_8009.CR3").write_text("data")
        (folder / "IMG_8009.CR3.xmp").write_text("data")

        matches = find_matches_for_codes(folder, ["7644", "8009"], ["CR3", "XMP"])

        assert len(matches["7644"]["CR3"]) == 1
        assert len(matches["7644"]["XMP"]) == 1
        assert len(matches["8009"]["CR3"]) == 1
        assert len(matches["8009"]["XMP"]) == 1


def test_validator_detects_missing_xmp():
    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)
        (folder / "_MG_7644.CR3").write_text("data")
        # No creamos el XMP para 7644

        report = validate_photo_selection(folder, "_MG_7644.jpg", ["CR3", "XMP"])
        assert report["is_valid_for_operation"] is False
        assert report["can_process"] is True  # Aunque falta XMP, aún se puede procesar el RAW si el usuario lo confirma
        assert report["missing_details"] == {"7644": ["XMP"]}



def test_full_pipeline_end_to_end():
    """
    Prueba el flujo completo: Texto raw -> Parser -> Scanner -> Validator -> Mover
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)

        # 1. Crear entorno de origen simulado
        (folder / "_MG_7644.CR3").write_text("RAW content")
        (folder / "_MG_7644.xmp").write_text("XMP content")
        (folder / "_MG_8009.CR3").write_text("RAW content 2")
        (folder / "_MG_8009.xmp").write_text("XMP content 2")

        raw_input = "_MG_7644.jpg  Destacados  9/28/2026\n_MG_8009.jpg"
        selected_exts = ["CR3", "XMP"]

        # 2. Ejecutar validación
        report = validate_photo_selection(folder, raw_input, selected_exts)
        assert report["is_valid_for_operation"] is True
        assert len(report["files_to_process"]) == 4

        # 3. Ejecutar copia hacia /Seleccionadas
        move_result = process_files(folder, report["files_to_process"], action="copy")
        assert move_result["success"] is True
        assert move_result["processed_count"] == 4

        dest_folder = folder / "Seleccionadas"
        assert (dest_folder / "_MG_7644.CR3").exists()
        assert (dest_folder / "_MG_7644.xmp").exists()
        assert (dest_folder / "_MG_8009.CR3").exists()
        assert (dest_folder / "_MG_8009.xmp").exists()
