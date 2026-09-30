"""
src/core/mover.py
Módulo encargado de ejecutar la transferencia física de archivos (Copiar o Mover)
hacia la subcarpeta /Seleccionadas con validación de existencia y protección anti-sobrescritura.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Any, Union


def get_unique_destination_path(target_file: Path) -> Path:
    """
    Si un archivo ya existe en la carpeta de destino, genera un nombre único
    con sufijo incremental (ej: _MG_7644_1.CR3) para evitar sobrescrituras.

    :param target_file: Ruta de destino deseada.
    :return: Ruta de destino garantizada como no existente.
    """
    if not target_file.exists():
        return target_file

    stem = target_file.stem
    suffix = target_file.suffix
    parent = target_file.parent
    counter = 1

    # Para sidecars dobles como _MG_8009.CR3.xmp, stem daría _MG_8009.CR3
    # Si suffix es .xmp y el stem termina en otro suffix (ej. .CR3), preservamos la estructura
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def process_files(
    source_directory: Union[str, Path],
    files_to_process: List[Path],
    action: str = "copy",
    subfolder_name: str = "Seleccionadas"
) -> Dict[str, Any]:
    """
    Ejecuta la copia o movimiento de los archivos validados.

    :param source_directory: Carpeta de trabajo principal.
    :param files_to_process: Lista de objetos Path validados para procesar.
    :param action: "copy" para copiar o "move" para mover.
    :param subfolder_name: Nombre de la subcarpeta destino (por defecto "Seleccionadas").
    :return: Resumen detallado del resultado de la operación.
    """
    source_dir = Path(source_directory)

    # 1. Validar existencia de la carpeta de trabajo origen
    if not source_dir.is_dir():
        return {
            "success": False,
            "error_message": f"La carpeta de origen no existe: {source_dir}",
            "processed_count": 0,
            "errors": []
        }

    # 2. Comprobar / Crear la subcarpeta destino (ej: /Seleccionadas)
    dest_dir = source_dir / subfolder_name
    dest_dir_existed_before = dest_dir.exists()
    dest_dir.mkdir(parents=True, exist_ok=True)

    action_clean = action.strip().lower()
    processed_files: List[Path] = []
    errors: List[Dict[str, str]] = []

    # 3. Procesar cada archivo
    for src_file in files_to_process:
        if not src_file.exists():
            errors.append({"file": src_file.name, "error": "El archivo origen ya no existe en disco."})
            continue

        # Generar ruta de destino anti-sobrescritura
        target_path = dest_dir / src_file.name
        safe_target_path = get_unique_destination_path(target_path)

        try:
            if action_clean == "copy":
                # shutil.copy2 preserva los metadatos de fechas de captura/modificación
                shutil.copy2(src_file, safe_target_path)
            elif action_clean == "move":
                shutil.move(src_file, safe_target_path)
            else:
                errors.append({"file": src_file.name, "error": f"Acción desconocida '{action}'."})
                continue

            processed_files.append(safe_target_path)
        except Exception as e:
            errors.append({"file": src_file.name, "error": str(e)})

    return {
        "success": len(errors) == 0,
        "action": action_clean,
        "destination_directory": dest_dir,
        "dest_dir_existed_before": dest_dir_existed_before,
        "processed_count": len(processed_files),
        "processed_files": processed_files,
        "errors": errors
    }
