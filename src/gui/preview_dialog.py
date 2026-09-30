"""
src/gui/preview_dialog.py
Ventana modal de vista previa antes de ejecutar la copia o movimiento de archivos.
"""

import customtkinter as ctk
from pathlib import Path
from typing import List, Dict, Any, Callable


class PreviewDialog(ctk.CTkToplevel):
    """
    Ventana emergente modal que solicita confirmación final del usuario
    mostrando el desglose completo de archivos a procesar y los faltantes omitidos.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        source_dir: str,
        dest_dir: str,
        action: str,
        validation_report: Dict[str, Any],
        on_confirm_callback: Callable[[], None]
    ):
        super().__init__(parent)

        self.title("Vista Previa de Operación — andercal.visuals")
        self.geometry("700x550")
        self.resizable(True, True)

        self.on_confirm_callback = on_confirm_callback
        self.report = validation_report
        self.files_to_process = validation_report.get("files_to_process", [])

        # Hacer la ventana modal (bloquea la ventana principal)
        self.transient(parent)
        self.grab_set()

        self._build_ui(source_dir, dest_dir, action)

    def _build_ui(self, source_dir: str, dest_dir: str, action: str):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Encabezado
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 VISTA PREVIA Y CONFIRMACIÓN DE OPERACIÓN",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Información general
        action_str = "COPIAR (Originales se mantienen en la raíz)" if action == "copy" else "MOVER (Originales se trasladan)"

        found_str = ", ".join([f"{count} {ext}" for ext, count in self.report.get("found_counts", {}).items() if count > 0])

        info_text = (
            f"• Acción: {action_str}\n"
            f"• Carpeta de origen: {source_dir}\n"
            f"• Carpeta de destino: {dest_dir}\n"
            f"• Archivos a procesar: {len(self.files_to_process)} encontrados ({found_str})"
        )

        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(fill="x", padx=15, pady=5)

        # Advertencia de faltantes si existen
        missing_details = self.report.get("missing_details", {})
        if missing_details:
            missing_box = ctk.CTkFrame(main_frame, fg_color="#3e2723", corner_radius=6)
            missing_box.pack(fill="x", padx=15, pady=5)

            warn_msg = f"⚠️ ATENCIÓN: Se omitirán los archivos faltantes registrados ({len(missing_details)} códigos tienen formatos ausentes como ACR/XMP)."
            warn_label = ctk.CTkLabel(
                missing_box,
                text=warn_msg,
                text_color="#ffb74d",
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w",
                justify="left"
            )
            warn_label.pack(fill="x", padx=10, pady=6)

        # Lista desglosada de archivos a procesar
        list_label = ctk.CTkLabel(
            main_frame,
            text=f"Listado de archivos físicos que serán procesados ({len(self.files_to_process)}):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        list_label.pack(anchor="w", padx=15, pady=(8, 2))

        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=220)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=5)

        for i, file_path in enumerate(self.files_to_process, start=1):
            file_item = ctk.CTkLabel(
                scroll_frame,
                text=f"{i:03d}.  {file_path.name}",
                anchor="w",
                font=ctk.CTkFont(family="Consolas", size=11)
            )
            file_item.pack(fill="x", padx=5, pady=1)

        # Botones de acción
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=15)

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="CANCELAR",
            fg_color="#cf6679",
            hover_color="#b00020",
            command=self._cancel
        )
        btn_cancel.pack(side="left", padx=10, expand=True, fill="x")

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="✔ CONFIRMAR Y PROCESAR ARCHIVOS ENCONTRADOS",
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm
        )
        btn_confirm.pack(side="right", padx=10, expand=True, fill="x")

    def _confirm(self):
        self.grab_release()
        self.destroy()
        if self.on_confirm_callback:
            self.on_confirm_callback()

    def _cancel(self):
        self.grab_release()
        self.destroy()
