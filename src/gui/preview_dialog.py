"""
src/gui/preview_dialog.py
Ventana modal de vista previa antes de ejecutar la copia o movimiento de archivos.
"""

import customtkinter as ctk
from pathlib import Path
from typing import List, Callable


class PreviewDialog(ctk.CTkToplevel):
    """
    Ventana emergente modal que solicita confirmación final del usuario
    mostrando el desglose completo de archivos a procesar.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        source_dir: str,
        dest_dir: str,
        action: str,
        files_to_process: List[Path],
        on_confirm_callback: Callable[[], None]
    ):
        super().__init__(parent)

        self.title("Vista Previa de Operación — andercal.visuals")
        self.geometry("650x500")
        self.resizable(True, True)

        self.on_confirm_callback = on_confirm_callback
        self.files_to_process = files_to_process

        # Hacer la ventana modal (bloquea la ventana principal)
        self.transient(parent)
        self.grab_set()

        self._build_ui(source_dir, dest_dir, action)

    def _build_ui(self, source_dir: str, dest_dir: str, action: str):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Encabezado
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 VISTA PREVIA DE LA OPERACIÓN",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Información general
        action_str = "COPIAR (Los originales se mantendrán)" if action == "copy" else "MOVER (Los originales se trasladarán)"

        info_text = (
            f"• Acción: {action_str}\n"
            f"• Carpeta de trabajo: {source_dir}\n"
            f"• Carpeta de destino: {dest_dir}\n"
            f"• Total de archivos a procesar: {len(self.files_to_process)} archivos"
        )

        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        info_label.pack(fill="x", padx=15, pady=5)

        # Lista desglosada de archivos
        list_label = ctk.CTkLabel(
            main_frame,
            text="Archivos incluidos en esta operación:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        list_label.pack(anchor="w", padx=15, pady=(10, 5))

        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=5)

        for i, file_path in enumerate(self.files_to_process, start=1):
            file_item = ctk.CTkLabel(
                scroll_frame,
                text=f"{i:02d}.  {file_path.name}",
                anchor="w",
                font=ctk.CTkFont(family="Consolas", size=12)
            )
            file_item.pack(fill="x", padx=5, pady=2)

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
            text="✔ CONFIRMAR Y PROCESAR",
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            font=ctk.CTkFont(size=14, weight="bold"),
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
